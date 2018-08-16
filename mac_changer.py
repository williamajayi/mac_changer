#!/usr/bin/env python

import subprocess
import optparse
import re

def get_current_mac(interface):
    if_result = subprocess.check_output(["ifconfig", interface])
    check_macaddress = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", if_result)
    if check_macaddress:
        return check_macaddress.group(0)
    else:
        print("[-] Could not get MAC address")

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC address, use --help for more info.")
    return options

def change_macaddress(interface, new_mac):
    current_mac = get_current_mac(interface)
    if current_mac:
        print("[+] Changing the Mac Address for interface " +interface+ " from " +current_mac+ " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    print("[+] Done")

options = get_arguments()
change_macaddress(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address was not successfully changed!")
