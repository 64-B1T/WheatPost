import sys
import time
import select
import paramiko
import cryptography
import warnings
import os
warnings.simplefilter("ignore", cryptography.utils.CryptographyDeprecationWarning)

host = '10.0.1.2'

def login(username, password):
    i = 1

    # Try to connect to the host.
    # Retry a few times if it fails.
    while True:
        print("Trying to connect to %s (%i/30)" % (host, i))

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username=username, password=password)
            print("Connected to %s" % host)
            return ("Login successful", ssh)
        except paramiko.AuthenticationException:
            print("Authentication failed when connecting to %s" % host)
            return ("Authentication failed", None)
        except:
            print("Could not SSH to %s, waiting for it to start" % host)
            i += 1
            time.sleep(2)

        # If we could not connect within time limit
        if i == 30:
            print("Could not connect to %s. Giving up" % host)
            return ("Could not connect to device", None)

def close(ssh):
    print("Closed connection to %s" % host)
    ssh.close()

def create_user(ssh, username, password):
    # Potential temporary ssh client
    temp = None

    if not ssh:
        temp = login("guest", "guest")[1]
        if not temp:
            return 1

    command = "/usr/local/bin/wpAddUser \"%s\" \"%s\"" % (username, password)
    result = ""
    if temp:
        result, other = send_command(temp, command)
    else:
        result, other = send_command(ssh, command)
    print("create_user result:")
    print(result)

    if result:
        # User could not be created
        print("Giving up\n")
        return 1
    else:
        # User was created
        # Create a user folder for them
        temp_ssh = login(username, password)[1]
        send_command(temp_ssh, "mkdir \"/home/pi/Wheatpaste/%s\"" % username)
        send_command(temp_ssh, "chmod 750 \"%s\"" % username)
        close(temp_ssh)
        return 0

def send_command(ssh, command):
    # Send the command (non-blocking)
    stdin, stdout, stderr = ssh.exec_command(command)

    err = stderr.readlines()
    stripped_err = [e.rstrip() for e in err]
    out = stdout.readlines()
    stripped_out = [o.rstrip() for o in out]

    return (stripped_err, stripped_out)

def mount(username, password, folder):
    print("Attempting to mount")

    # Connect to shared drive
    os.system("mount.py %s %s %s" % (username, password, folder))

    return("Check if directory is mounted")

def get_users(ssh):
    print("Getting user list")

    other, users = send_command(ssh, "cat /home/pi/Wheatpaste/UserList.txt")
    print(users)
    return users

def send_file(ssh, file_path, remote_path):
    # Send the file
    ftp_client = ssh.open_sftp()
    attributes = ftp_client.put(file_path, remote_path)

    # Check if file transferred properly
    if attributes:
        print("File transfer successful\n")
        return 0
    else:
        print("File transfer failed\n")
        return 1
