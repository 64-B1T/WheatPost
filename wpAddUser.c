#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if(argc != 3) {
        printf("Please enter two arguments: username and password\n");
        exit(1);
    }

    // Add new user
    char buffer[120];
    snprintf(buffer, 120, "useradd %s", argv[1]);

    setuid(0);
    clearenv();
    int result = 0;
    result = system(buffer);

    if (result < 0) {
        exit(1);
    }

    // Clear buffer
    memset(buffer, 0, 120);

    // Change password
    snprintf(buffer, 120, "echo %s:%s | chpasswd", argv[1], argv[2]);

    setuid(0);
    clearenv();
    system(buffer);

    // Clear buffer
    memset(buffer, 0, 120);

    // Change password
    snprintf(buffer, 120, "usermod -d /home/pi %s", argv[1]);

    setuid(0);
    clearenv();
    system(buffer);

    // Clear buffer
    memset(buffer, 0, 120);

    // Add samba user
    snprintf(buffer, 120, "(echo %s; sleep 1; echo %s ) | sudo smbpasswd -s -a %s", argv[1], argv[2], argv[1]);

    setuid(0);
    clearenv();
    system(buffer);
}
