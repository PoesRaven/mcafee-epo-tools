"""
Description: apply_tag.py is used to update a list of systems with a specified ePO tag. ePO has some limitations as
to the number of discreet "or" rules placed inside of tagging logic. As such, if you need to create a list longer
than about 50 systems, you may have to perform the exercise in batches. This program will take an entire list of
systems as long as you like and update all of them with the tag selected.

usage: apply_tag.py [-h] --host HOST [--port PORT] --un UN --pw PW --file FILE
                    --tag TAG [-v]

Update systems in ePO with given tag

optional arguments:
  -h, --help   show this help message and exit
  --host HOST  ePO FQDN or IP Address
  --port PORT  ePO port
  --un UN      ePO username with authorization to access API. This must be a
               superuser
  --pw PW      ePO password
  --file FILE  The file containing the system names to be updated
  --tag TAG    The new tag you'd like to add to the systems. This tag must
               already exist in the tag catalog
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


def main(epo_host, epo_port, epo_un, epo_pw, set_tag, system_file, verbose):
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
            print("Applying tag: {} to system: {}".format(set_tag, epo_system))

        change_result = mc.system.applyTag(epo_system, set_tag)

        if change_result == 1:
            if verbose:
                print("Applying tag: {} to system: {}".format(set_tag, epo_system))
            systems_updated += 1
        else:
            print("Failed to apply tag: {} to system: {}".format(set_tag, epo_system))
            print("Perhaps the system already has the tag or the system was not found in ePO")

        system_count += 1

    print("Successfully added tag: {} to {}/{} systems".format(set_tag, systems_updated, system_count))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Update systems in ePO with a given tag')
    parser.add_argument("--host", help="ePO FQDN or IP Address", required=True)
    parser.add_argument("--port", help="ePO port", default="8443", required=False)
    parser.add_argument("--un", help="ePO username with authorization to access API. This must be a superuser",
                        required=True)
    parser.add_argument("--pw", help="ePO password", required=True)
    parser.add_argument("--file", help="The file containing the system names to be updated", required=True)
    parser.add_argument("--tag", help="The new tag you'd like to add to the systems. This tag must already exist in "
                                      "the tag catalog", required=True)
    parser.add_argument("-v", action='store_true', help="Verbose output. This will notify you of every system which is "
                                                        "being updated.")

    args = parser.parse_args()

    main(args.host, args.port, args.un, args.pw, args.tag, args.file, args.v)
