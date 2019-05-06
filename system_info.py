"""
Description: system_info.py is used to pull system information about an asset within ePO

usage: system_info.py [-h] --host HOST [--port PORT] --un UN --pw PW [--file FILE]

Display information about a given system

optional arguments:
  -h, --help   show this help message and exit
  --host HOST  ePO FQDN or IP Address
  --port PORT  ePO port
  --un UN      ePO username with authorization to access API. This must be a
               superuser
  --pw PW      ePO password
  --file FILE  The file containing the system names to be found
  -v           Verbose output. This will notify you of every system which is
               being updated.

"""
__author__ = "Jesse Netz"
__copyright__ = "Copyright 2018, The Open McAfee Project"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jesse Netz"
__email__ = "jesse.netz@icloud.com"

import mcafee
import argparse


def main(epo_host, epo_port, epo_un, epo_pw, system_file, verbose):
    try:
        # Create an ePO client object
        mc = mcafee.client(epo_host, epo_port, epo_un, epo_pw)
    except e:
        print("Failed to authenticate to ePO. Please ensure the username and password are correct, and that the "
              "account is a superuser.")
        exit()

    try:
        # Get file for reading operations
        this_file = open(system_file, 'r')
    except e:
        print("Failed to read system file. Perhaps the location or file name is incorrect?")
        exit()


    # Apply the tag for each system in file
    systems_updated = 0
    system_count = 0
    for this_system in this_file:
        epo_system = this_system.rstrip('\n')
        if verbose:
            print("Searching for system: {}".format(epo_system))

        find_result = mc.system.find(epo_system)

        print find_result
        if find_result:
            if verbose:
                print("Found the system: {}".format(epo_system))
            systems_updated += 1
        else:
            print("Failed to find the system: {}".format(epo_system))
            print("Perhaps the system already has the tag or the system was not found in ePO")

        system_count += 1

    print("Successfully found system: {}".format(epo_system))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Update systems in ePO with a given tag')
    parser.add_argument("--host", help="ePO FQDN or IP Address", required=True)
    parser.add_argument("--port", help="ePO port", default="8443", required=False)
    parser.add_argument("--un", help="ePO username with authorization to access API. This must be a superuser",
                        required=True)
    parser.add_argument("--pw", help="ePO password", required=True)
    parser.add_argument("--file", help="The file containing the system names to be updated", required=True)
    parser.add_argument("-v", action='store_true', help="Verbose output. This will notify you of every system which is "
                                                        "being updated.")

    args = parser.parse_args()

    main(args.host, args.port, args.un, args.pw, args.file, args.v)
