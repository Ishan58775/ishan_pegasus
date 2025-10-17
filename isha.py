import paramiko
import subprocess
import sys

def connect_ios(ip, username, password, command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(command)
        print(stdout.read().decode())
        client.close()
    except Exception as e:
        print(f"Error connecting to iOS phone: {e}")

def connect_android(ip, command):
    try:
        subprocess.run(["adb", "connect", ip], check=True)
        subprocess.run(["adb", "shell", command], check=True)
    except Exception as e:
        print(f"Error connecting to Android phone: {e}")

def main():
    ip = input("Enter phone IP address: ")
    os = input("Enter phone OS (ios/android): ")
    if os.lower() == "ios":
        username = input("Enter username: ")
        password = input("Enter password: ")
        command = input("Enter command to execute: ")
        connect_ios(ip, username, password, command)
    elif os.lower() == "android":
        command = input("Enter command to execute: ")
        connect_android(ip, command)
    else:
        print("Invalid phone OS")

if __name__ == "__main__":
    main()