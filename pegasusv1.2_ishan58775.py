#!/usr/bin/env python3
# Modified by: ishan58775
# Pegasus v1.2 - ADB Utility (no license)

import os
import subprocess
import sys
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    print(Fore.CYAN + Style.BRIGHT + "========================================")
    print(Fore.GREEN + Style.BRIGHT + " Pegasus v1.2 — ADB Utility Toolkit")
    print(Fore.CYAN + Style.BRIGHT + " Modified by: ishan58775")
    print(Fore.CYAN + Style.BRIGHT + "========================================\n")

def run_cmd(cmd, capture=True):
    try:
        if capture:
            p = subprocess.run(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return p.stdout.strip(), p.stderr.strip()
        else:
            subprocess.run(cmd, shell=False)
            return "", ""
    except Exception as e:
        return "", str(e)

def adb_devices():
    out, err = run_cmd(["adb", "devices", "-l"])
    print(Fore.GREEN + "[adb devices]")
    print(out or "(no devices)")
    if err:
        print(Fore.RED + err)

def show_device_info():
    model, _ = run_cmd(["adb", "shell", "getprop", "ro.product.model"])
    ver, _ = run_cmd(["adb", "shell", "getprop", "ro.build.version.release"])
    battery_raw, _ = run_cmd(["adb", "shell", "dumpsys", "battery"])
    print(Fore.CYAN + f"Model: {model or 'Unknown'}")
    print(Fore.CYAN + f"Android: {ver or 'Unknown'}")
    # show battery lines only
    print(Fore.CYAN + "Battery info:")
    for line in (battery_raw or "").splitlines():
        if "level" in line or "status" in line or "AC powered" in line:
            print("  " + line)

def connect_wifi():
    ip = input("Enter device IP (e.g. 192.168.1.42): ").strip()
    if not ip:
        print("No IP provided.")
        return
    print("Enabling adb tcpip 5555 (requires prior USB auth).")
    out, err = run_cmd(["adb", "tcpip", "5555"])
    if err:
        print(Fore.YELLOW + err)
    out, err = run_cmd(["adb", "connect", f"{ip}:5555"])
    if out:
        print(out)
    if err:
        print(Fore.RED + err)

def disconnect_all():
    out, err = run_cmd(["adb", "disconnect"])
    print(out or "Disconnected.")
    if err:
        print(Fore.RED + err)

def take_screenshot():
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    default = f"screen_{now}.png"
    local = input(f"Local filename (default: {default}): ").strip() or default
    remote = f"/sdcard/{local}"
    print("Capturing screenshot...")
    run_cmd(["adb", "shell", "screencap", "-p", remote])
    out, err = run_cmd(["adb", "pull", remote, local])
    if err:
        print(Fore.RED + err)
    else:
        print(Fore.GREEN + f"Saved {local}")

def record_screen():
    dur = input("Duration seconds (default 10): ").strip()
    try:
        secs = int(dur) if dur else 10
    except:
        secs = 10
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    local = f"record_{now}.mp4"
    remote = f"/sdcard/{local}"
    print(f"Recording {secs}s...")
    run_cmd(["adb", "shell", "screenrecord", "--time-limit", str(secs), remote])
    out, err = run_cmd(["adb", "pull", remote, local])
    if err:
        print(Fore.RED + err)
    else:
        print(Fore.GREEN + f"Saved {local}")

def mirror_screen():
    print("Launching scrcpy (if installed). Ctrl+C to return.")
    try:
        subprocess.run(["scrcpy"])
    except FileNotFoundError:
        print(Fore.RED + "scrcpy not installed or not in PATH.")

def list_apks():
    out, err = run_cmd(["adb", "shell", "pm", "list", "packages", "-f"])
    if out:
        print(out)
        if input("Save to apk_list.txt? (y/N): ").strip().lower() == "y":
            with open("apk_list.txt", "w", encoding="utf-8") as f:
                f.write(out)
            print("Saved apk_list.txt")
    if err:
        print(Fore.RED + err)

def main():
    banner()
    while True:
        print(Style.BRIGHT + Fore.YELLOW + "1) Check devices")
        print("2) Device info")
        print("3) Connect (Wi‑Fi adb)")
        print("4) Disconnect all")
        print("5) Take screenshot")
        print("6) Record screen")
        print("7) Mirror screen (scrcpy)")
        print("8) List APKs")
        print("0) Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            adb_devices()
        elif choice == "2":
            show_device_info()
        elif choice == "3":
            connect_wifi()
        elif choice == "4":
            disconnect_all()
        elif choice == "5":
            take_screenshot()
        elif choice == "6":
            record_screen()
        elif choice == "7":
            mirror_screen()
        elif choice == "8":
            list_apks()
        elif choice == "0":
            print("Exiting.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    # quick check for adb
    from shutil import which
    if not which("adb"):
        print(Fore.RED + "ADB not found. Please install Android Platform Tools and ensure 'adb' is in PATH.")
    main()