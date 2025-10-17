import subprocess
import sys

def connect_android(ip, command):
    try:
        subprocess.run(["adb", "connect", ip], check=True)
        subprocess.run(["adb", "shell", command], check=True)
    except Exception as e:
        print(f"Error connecting to Android phone: {e}")

def main():
    ip = input("Enter phone IP address: ")
    command = input("Enter command to execute: ")
    connect_android(ip, command)

if __name__ == "__main__":
    main()