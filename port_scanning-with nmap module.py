#!/bin/python3

import os
import sys
import socket
import concurrent.futures
import time
import nmap

# Check for sudo permissions
if os.geteuid() != 0:
    print("Please run the script with sudo privileges.")
    sys.exit()

# Function to resolve URL to IPv4 address
def resolve_url(url):
    try:
        ipv4_address = socket.gethostbyname(url)
        return ipv4_address
    except socket.gaierror:
        print("Hostname could not be resolved.")
        sys.exit()

# Define our target
if len(sys.argv) == 2:
    target = resolve_url(sys.argv[1])  # Resolve URL to IPv4
else:
    print("Invalid amount of arguments.")
    print("Syntax: python3 scanner.py <target>")
    sys.exit()

# Metasploit-like animation frames
animation_frames = [
    "    _____           __  __ ______    ______      ________ _____",
    "   / ____|   /\\    |  \\/  |  ____|  / __ \\ \\    / /  ____|  __ \\",
    "  | |  __   /  \\   | \\  / | |__    | |  | \\ \\  / /| |__  | |__) |",
    "  | | |_ | / /\\ \\  | |\\/| |  __|   | |  | |\\ \\/ / |  __| |  _  /",
    "  | |__| |/ ____ \\ | |  | | |____  | |__| | \  /  | |____| | \ \ ",
    "   \\_____/_/    \\_\\|_|  |_|______|  \\____/   \\/   |______|_|  \\_\\",
]

def show_animation():
    for frame in animation_frames:
        print(frame)
        time.sleep(0.1)
        
    print ("\n")

# Add a pretty banner
print("-" * 50)
print("Welcome to PortEye....")
print("-" * 50)
print("PortEye - Your Ultimate Port Scanner.")

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.2)  # Adjust the timeout as needed for faster scanning
    result = s.connect_ex((target, port))  # returns an error indicator - if port is open it throws a 0, otherwise 1
    if result == 0:
        open_port = f"\033[92mPort {port} is open\033[0m"
        print(open_port)

        # Attempt to grab the banner or service version
        try:
            service = grab_service(target, port)
            if service:
                print(f"\033[94mService for Port {port}:\033[0m {service}")

        except Exception as e:
            print(f"Error while grabbing service for Port {port}: {e}")

    s.close()

def grab_service(ip, port, timeout=2):
    nm = nmap.PortScanner()
    nm.scan(ip, str(port), arguments='-sV')
    if nm[ip]['tcp'][port]['product']:
        return f"{nm[ip]['tcp'][port]['product']} {nm[ip]['tcp'][port]['version']}"
    else:
        return "Unknown Service"

try:
    show_animation()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for port in range(0, 1000):  # Extended port range
            executor.submit(scan_port, port)

except KeyboardInterrupt:
    print("\nExiting program.")
    sys.exit()

except socket.error as e:
    print(f"Error: {e}")
    sys.exit()

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit()

finally:
    print("\n\n" + "-" * 50)
    print("Game Over")
    print("-" * 50)
    print("\nScan results displayed on the console.")

