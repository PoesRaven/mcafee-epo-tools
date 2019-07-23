# mcafee-epo-tools

## apply_tag.py
apply_tag.py is used to update a list of systems with a specified ePO tag. ePO has some limitations as
to the number of discreet "or" rules placed inside of tagging logic. As such, if you need to create a list longer
than about 50 systems, you may have to perform the exercise in batches. This program will take an entire list of
systems as long as you like and update all of them with the tag selected.

Usage: `python apply_tag.py [-h] --host HOST [--port PORT] --un UN --pw PW --file FILE
                    --tag TAG [-v]`

Update systems in ePO with given tag
```
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
```               
### Installation
- Ensure you have python v2.7
- Download mcafee.py, urlquote.py (if the urlquote library is not installed), and apply_tag.py to the same directory
- Ensure you have a working "systems" file that correlate to the systems in epo
- Run apply_tag.py

## ens_ep.py
ens_ep.py is used to dynamically add an Expert Rule to an Exploit Prevention policy of your choosing. This is not a 
capability of the McAfee ePO. Therefore, this script uses Selenium web scraping to achieve this task.

usage: `ens_ep.py [-h] --epo EPO --user USER --password PASSWORD --policy
                 POLICY --name NAME [--sev {1,2,3,4}]
                 [--action {Block,Report} [{Block,Report} ...]] --rule_type
                 {Buffer_Overflow,Illegal_API_Use,ENS_Files,Services,ENS_Registry,ENS_Process}
                 --rule RULE [--notes NOTES] [--debug]`

Dynamically add an expert rule to a specified policy.
```
optional arguments:
  -h, --help            show this help message and exit
  --epo EPO             The url of the epo: https://eposerver.epo:8443
  --user USER           Username to log into ePO
  --password PASSWORD   Password for the ePO account
  --policy POLICY       The policy to which you want to add the Expert Rule
  --name NAME           Name of the expert rule
  --sev {1,2,3,4}       Severity of the expert rule
  --action {Block,Report} [{Block,Report} ...]
                        When triggered, should it block or report
  --rule_type {Buffer_Overflow,Illegal_API_Use,ENS_Files,Services,ENS_Registry,ENS_Process}
                        What kind of rule is this?
  --rule RULE           The Expert Rule
  --notes NOTES         Any additional notes you want to add to the rule
  --debug               print debug messages to stderr
```
### Installation
- Ensure you have python v3.5+
- Download ens_ep.py
- SUPPORTS ePO 5.9 ONLY!
- Download chromedriver as a headless driver for the webkit
- pip3 install selenium
- Run ens_ep.py

### Example
```
python3 ens_ep.py --epo "https://win2016-epo.jnetzlab.loc:8443" --user "epadd" --pass "abcd1234" --policy "My Default" --name "Stop CMD" --sev 3 --rule_type ENS_Files --rule '    Rule {
Process {
Include OBJECT_NAME { -v cmd.exe  }
}
Target {
Match FILE {
Include OBJECT_NAME {
-v "c:\\temp\\*test.txt"
}
   Include -access "CREATE"
}}' --notes "this is a note" --debug
-------

Connecting to the ePO
Logging into ePO
Navigating to Policy Catalog
Opening the ENS Threat Prevention Policies
Opening My Default Exploit Prevention policy
Showing Advanced options
Adding expert rule
Adding name to the Expert Rule
Setting the severity for the Expert Rule
Setting the Action for the Expert Rule
Setting the rule type for the Expert Rule
Setting the signature content for the Expert Rule
Setting the notes for the Expert Rule
Saving the Expert Rule
Saving the Exploit Prevention policy
Closing the browser
```

## system_info.py
system_info.py is used to pull system information about an asset within ePO

Usage: `python system_info.py [-h] --host HOST [--port PORT] --un UN --pw PW --file FILE
                    [-v]`

Display information about a given system
```
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
```      
### Installation
- Ensure you have python v2.7
- Download mcafee.py, urlquote.py (if the urlquote library is not installed), and system_info.py to the same directory
- Ensure you have a working "systems" file that correlate to the systems in epo
- Run system_info.py