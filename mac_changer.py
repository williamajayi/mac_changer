#!/usr/bin/env python

import subprocess
import argparse
import re, platform

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    check_macaddress = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode())
    if check_macaddress:
        return check_macaddress.group(0)
    else:
        print("[-] Could not get MAC address")

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_argument("-m", "--mac", dest="new_mac", help="New MAC address")
    options = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC address, use --help for more info.")
    return options

def get_system_platform():
    os = platform.platform()
    if "Linux" in os:
        return True

def change_macaddress(interface, new_mac):
    current_mac = get_current_mac(interface)
    if current_mac:
        print("[+] Changing the Mac Address for interface " +interface+ " from " +current_mac+ " to " + new_mac)

    if get_system_platform():
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
        subprocess.call(["ifconfig", interface, "up"])
    else:
        subprocess.call(["ifconfig", interface, "ether", new_mac])

    print("[+] Done")

options = get_arguments()
change_macaddress(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address was not successfully changed!")
