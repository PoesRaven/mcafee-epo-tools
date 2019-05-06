# mcafee-epo-tools

## apply_tag.py
apply_tag.py is used to update a list of systems with a specified ePO tag. ePO has some limitations as
to the number of discreet "or" rules placed inside of tagging logic. As such, if you need to create a list longer
than about 50 systems, you may have to perform the exercise in batches. This program will take an entire list of
systems as long as you like and update all of them with the tag selected.

Usage: `python apply_tag.py [-h] --host HOST [--port PORT] --un UN --pw PW --file FILE
                    --tag TAG [-v]`

Update systems in ePO with given tag

Arguments:
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
               
### Installation
- Ensure you have python v2.7
- Download mcafee.py, urlquote.py (if the urlquote library is not installed), and apply_tag.py to the same directory
- Ensure you have a working "systems" file that correlate to the systems in epo
- Run apply_tag.py

## system_info.py
system_info.py is used to pull system information about an asset within ePO

Usage: `python system_info.py [-h] --host HOST [--port PORT] --un UN --pw PW --file FILE
                    [-v]`

Display information about a given system

Arguments:
   -h, --help   show this help message and exit
  --host HOST  ePO FQDN or IP Address
  --port PORT  ePO port
  --un UN      ePO username with authorization to access API. This must be a
               superuser
  --pw PW      ePO password
  --file FILE  The file containing the system names to be found
  -v           Verbose output. This will notify you of every system which is
               being updated.
               
### Installation
- Ensure you have python v2.7
- Download mcafee.py, urlquote.py (if the urlquote library is not installed), and apply_tag.py to the same directory
- Ensure you have a working "systems" file that correlate to the systems in epo
- Run system_info.py