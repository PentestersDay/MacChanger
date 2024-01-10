#!usr/bin/env python
import subprocess
import argparse
import re


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Please enter interface")
    parser.add_argument("-m", "--mac", dest="new_mac", help="Please enter new mac address")
    options = parser.parse_args()

    if not options.interface:
        return parser.error("Please specify an interface, use '--help' for more info")
    elif not options.new_mac:
        return parser.error("Please specify an new mac address, use '--help' for more info")

    return options


def mac_changer(interface, new_mac):
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])


def result_mac(interface):
    ifconfig_result = str(subprocess.check_output(['ifconfig', interface]))
    mac_change_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_change_result:
        return mac_change_result.group(0)
    else:
        print("Not find mac address value")


options = get_arguments()
old_mac_show = result_mac(options.interface)
mac_changer(options.interface, options.new_mac)
new_mac_show = result_mac(options.interface)

if new_mac_show == options.new_mac:
    print(" Change your mac address: "+str(old_mac_show) + " => " + str(new_mac_show))
else:
    print("Error")
