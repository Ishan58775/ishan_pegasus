#!/usr/bin/env python3
# Modified by: ishan58775
# Pegasus v1.1 - ADB Utility (no license)

import os
import subprocess
import sys
from colorama import init, Fore, Style

init(autoreset=True)

def check_requirements():
    missing = []
    for cmd in ("adb",):
        if not shutil_which(cmd):
            missing.append(cmd)
    if missing:
        print(Fore.RED + "Missing required tools: " + ", ".join(missing))
        print("Install ADB and ensure it's in PATH.")
        sys.exit(1)

def shutil_which(cmd):
    # local helper to avoid importing shutil at top-level for minimal deps
    from shutil import which
    return which(cmd)

def run_cmd(cmd, capture=True):
    try:
        if capture:
            p = subprocess.run(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return p.stdout.strip(), p.stderr.strip()
        else:
            subprocess.run(cmd, shell=False)
            return "", ""
    except FileNotFoundError as e:
        return "", str(e)
    except Exception as e:
        return "", str(e)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    print(Fore.CYAN + Style.BRIGHT + "===============================")
    print(Fore.GREEN + Style.BRIGHT + " Pegasus v1.1 — ADB Utility")
    print(Fore.CYAN + Style.BRIGHT + " Modified by: ishan58775")
    print(Fore.CYAN + Style.BRIGHT + "===============================\n")

def adb_devices():
    out, err = run_cmd(["adb", "devices", "-l"])
    print(Fore.GREEN + "[adb devices]")
    print(out if out else "(no output)")
    if err:
        print(Fore.RED + err)

def device_info():
    model, _ = run_cmd(["adb", "shell", "getprop", "ro.product.model"])
    version, _ = run_cmd(["adb", "shell", "getprop", "ro.build.version.release"])
    batt, _ = run_cmd(["adb", "shell", "dumpsys", "battery", "|", "grep", "level"])  # grep may not work in this construct
    # safer: fetch battery via dumpsys and display raw
    batt_raw, _ = run_cmd(["adb", "shell", "dumpsys", "battery"])
    print(Fore.CYAN + "Model: " + (model or "Unknown"))
    print(Fore.CYAN + "Android Version: " + (version or "Unknown"))
    print(Fore.CYAN + "Battery (dumpsys output snippet):")
    for line in (batt_raw or "").splitlines()[:10]:
        print("  " + line)

def connect_wifi():
    ip = input("Enter device IP (e.g. 192.168.1.42): ").strip()
    if not ip:
        print("No IP provided.")
        return
    print("Putting device into tcpip mode (requires USB authorization once).")
    out, err = run_cmd(["adb", "tcpip", "5555"])
    if err:
        print(Fore.YELLOW + "Note: tcpip command returned stderr:")
        print(Fore.RED + err)
    out, err = run_cmd(["adb", "connect", f"{ip}:5555"])
    print(out if out else "(no output)")
    if err:
        print(Fore.RED + err)

def disconnect_all():
    out, err = run_cmd(["adb", "disconnect"])
    print(out if out else "Disconnected (no output).")
    if err:
        print(Fore.RED + err)

def take_screenshot():
    local = input("Local filename (default: screen.png): ").strip() or "screen.png"
    remote = f"/sdcard/{local}"
    print("Taking screenshot...")
    out, err = run_cmd(["adb", "shell", "screencap", "-p", remote])
    if err:
        print(Fore.RED + err)
    out, err = run_cmd(["adb", "pull", remote, local])
    if err:
        print(Fore.RED + err)
    else:
        print(Fore.GREEN + f"Screenshot saved to {local}")

def record_screen():
    dur = input("Duration seconds (default 10): ").strip()
    try:
        secs = int(dur) if dur else 10
    except:
        secs = 10
    remote = "/sdcard/record.mp4"
    print(f"Recording {secs}s...")
    out, err = run_cmd(["adb", "shell", "screenrecord", "--time-limit", str(secs), remote])
    if err:
        print(Fore.RED + err)
    out, err = run_cmd(["adb", "pull", remote, "record.mp4"])
    if err:
        print(Fore.RED + err)
    else:
        print(Fore.GREEN + "Saved record.mp4")

def mirror_screen():
    print("Starting scrcpy (must be installed). Press Ctrl+C to exit.")
    try:
        subprocess.run(["scrcpy"])
    except FileNotFoundError:
        print(Fore.RED + "scrcpy not found. Install scrcpy to use mirroring.")
    except KeyboardInterrupt:
        print("Stopped scrcpy.")

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
        print(Style.BRIGHT + Fore.YELLOW + "\nMenu:")
        print("1) Check ADB devices")
        print("2) Device info")
        print("3) Connect device over Wi‑Fi (adb tcpip)")
        print("4) Disconnect all")
        print("5) Take screenshot")
        print("6) Record screen")
        print("7) Mirror screen (scrcpy)")
        print("8) List installed APKs")
        print("0) Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            adb_devices()
        elif choice == "2":
            device_info()
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
            print("Bye.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    # quick check for adb tool
    try:
        from shutil import which
        if not which("adb"):
            print(Fore.RED + "ADB not found in PATH. Install Android Platform Tools and ensure 'adb' is available.")
            # do not exit, user might still want to see menu
    except Exception:
        pass
    main()