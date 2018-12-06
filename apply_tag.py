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


    # Apply the tag for each system in file
    systems_updated = 0
    for this_system in this_file:
        epo_system = this_system.rstrip('\n')
        if verbose:
            print("Applying tag: {} to system: {}".format(set_tag, epo_system))
        mc.system.applyTag(epo_system, set_tag)
        systems_updated += 1

    print("Successfully added tag: {} to {} systems".format(set_tag, systems_updated))

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
