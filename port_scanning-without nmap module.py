#!/bin/python3

import os
import sys
import socket
import concurrent.futures
import time
from datetime import datetime

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

# Add a pretty banner
print("-" * 50)
print("Welcome to PortEye Port Scanner")
print("-" * 50)
print("PortEye - Your Ultimate Port Scanner")
print("\n")

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.2)  # Adjust the timeout as needed for faster scanning
    result = s.connect_ex((target, port))  # returns an error indicator - if port is open it throws a 0, otherwise 1
    if result == 0:
        open_port = f"\033[92m{port}/tcp   open\033[0m"
        print(open_port)
    
        # Attempt to detect the service on the open port
        try:
            service = detect_service(s)
            if service:
                print(f"Service for {port}/tcp: {service}")

        except Exception as e:
            print(f"Error while detecting service for {port}/tcp: {e}")
            print(f"Service for {port}/tcp: Unknown Service")
    
    s.close()

def detect_service(s):
    s.send(b'')  # Send an empty byte to prompt a response
    response = s.recv(1024).decode('utf-8')  # Adjust the buffer size as needed
    
    # Analyze the response to determine the service
    if "HTTP" in response:
        return "HTTP Service"
    elif "SSH" in response:
        return "SSH Service"
    elif "FTP" in response:
        return "FTP Service"
    # Add more conditions for other services as needed
    
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
    print("Scan results displayed on the console.")

