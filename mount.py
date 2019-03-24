# Shared drive path: \\10.0.1.2\Wheatpaste
# Username: pi
# Password: raspberry
import subprocess as sp
import ctypes, sys

print(sys.argv[3])
print(r'rmdir %s' % sys.argv[3])
print(r'net use \\10.0.1.2\Wheatpaste /user:%s %s' % (sys.argv[1], sys.argv[2]))
print(r'mklink /d "%s" "\\10.0.1.2\Wheatpaste"' % sys.argv[3])

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    folder = sys.argv[3]

    # Disconnect anything
    p = sp.Popen(r'rmdir %s' % folder, shell=True)

    # Connect to shared drive
    p = sp.Popen(r'net use \\10.0.1.2\Wheatpaste /user:%s %s' % (sys.argv[1], sys.argv[2]), shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()

    # Link to folder
    command = r'mklink /d "%s" "\\10.0.1.2\Wheatpaste"' % folder
    p = sp.Popen(command, shell=True)
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
