from selenium import webdriver
import time
import argparse

sample_expert_rule = {
    'name': 'test8',
    'severity': '1',  # 1: Informational, 2: Low, 3: Medium, 4: High
    'action': ['Block', 'Report'],  # 'Block' or 'Report', both, or empty list for no action
    'rule_type': 'ENS_Files',  # 'Buffer_Overflow', 'Illegal_API_Use', 'ENS_Files', 'Services', 'ENS_Registry',
    # 'ENS_Process' are options
    'rule_content': """
    Rule {
	Process {
		Include OBJECT_NAME { -v cmd.exe  }
	}
	Target {
		Match FILE {
			Include OBJECT_NAME { 
				-v "c:\\temp\\*test.txt"
			}
   Include -access "CREATE"
		}
	}
}
        """,
    'notes': 'This is a test expert rule for automation.'
}


def add_expert_rule(epo_url, epo_un, epo_pw, policy, expert_rule, debug=False):
    # Google Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1400x1000')

    driver = webdriver.Chrome(executable_path="./chromedriver",
                          options=options)
    # ------------------------------
    # The actual test scenario: Test the codepad.org code execution service.

    print("Connecting to the ePO")
    driver.get(epo_url)

    if debug: driver.save_screenshot("login.png")
    time.sleep(1)
    # Enter some text!

    print("Logging into ePO")
    username = driver.find_element_by_xpath('//*[@id="name"]')
    username.send_keys(epo_un)

    # Enter some text!
    password = driver.find_element_by_xpath('//*[@id="password"]')
    password.send_keys(epo_pw)

    # Submit the form!
    login_button = driver.find_element_by_xpath('//*[@id="login.button"]')
    login_button.click()

    time.sleep(1)

    print("Navigating to Policy Catalog")
    if debug: driver.save_screenshot("dashboard.png")

    menu = driver.find_element_by_xpath('//*[@id="mfsLauncher"]')
    menu.click()


    policycatalog = driver.find_element_by_xpath('//*[@title="Policy Catalog"]')
    policycatalog.click()
    if debug: driver.save_screenshot("policycatalog.png")

    time.sleep(1)

    print("Opening the ENS Threat Prevention Policies")
    policySettingOption = driver.find_element_by_xpath('//*[@id="osID_Products"]/option[@title="Endpoint Security Threat '
                                                   'Prevention "]')
    policySettingOption.click()
    driver.execute_script("fnReloadCatalogPage();")

    if debug: driver.save_screenshot("policycatalog2.png")
    time.sleep(1)

    print("Opening {} Exploit Prevention policy".format(policy))
    policySelect = driver.find_element_by_xpath('//div[text()="Exploit Prevention"]/../../td[1]/div/span/a[text()'
                                                '="{}"]'.format(policy))
    policySelect.click()
    if debug: driver.save_screenshot("ep.png")
    time.sleep(1)

    print("Showing Advanced options")
    showAdvanced = driver.find_element_by_xpath('//*[@id="buttonID_pageState"]')

    if showAdvanced.get_attribute('value') == "Show Advanced":
        showAdvanced.click()

    if debug: driver.save_screenshot("ep_adv.png")
    time.sleep(1)

    print("Adding expert rule")
    addExpertRule = driver.find_element_by_xpath('//*[@id="addExpertRules"]')
    addExpertRule.click()

    if debug: driver.save_screenshot("add_er.png")
    time.sleep(1)


    print("Adding name to the Expert Rule")
    input_name = driver.find_element_by_xpath('//*[@id="textboxID_ExpertRuleName"]')
    input_name.send_keys(expert_rule['name'])

    print("Setting the severity for the Expert Rule")
    input_severity = driver.find_element_by_xpath('//*[@id="selectID_Severity"]/option[@value={}]'.format(
        expert_rule['severity']))
    input_severity.click()

    print("Setting the Action for the Expert Rule")

    try:
        action
    except NameError:
        action = None

    if type(action) is list:
        for action in expert_rule['action']:
            print(action)
            if str(action).strip() == "Block":
                input_block = driver.find_element_by_xpath('//*[@id="hidden_expertRuleBlock"]')
                input_block.click()

            if str(action).strip() == "Report":
                input_report = driver.find_element_by_xpath('//*[@id="hidden_expertRuleReport"]')
                input_report.click()

    print("Setting the rule type for the Expert Rule")
    input_rule_type = driver.find_element_by_xpath('//*[@id="selectID_RuleClassTemplate"]/option[@value="{}"]'.format(
        expert_rule['rule_type']))
    input_rule_type.click()

    print("Setting the signature content for the Expert Rule")
    driver.execute_script("""
        _editor = document.querySelectorAll('div.CodeMirror')[0].CodeMirror;
        _editor.setValue('{}');
    """.format(expert_rule['rule_content'].replace('\r', '\\r').replace('\n', '\\n')))


    if expert_rule['notes']:
        print("Setting the notes for the Expert Rule")
        input_notes = driver.find_element_by_xpath('//*[@id="txtNotes"]')
        input_notes.click()  # We need to click
        input_notes.send_keys(expert_rule['notes'])

    if debug: driver.save_screenshot('er_unsaved.png')

    print("Saving the Expert Rule")
    save_button = driver.find_element_by_xpath('//*[@id="saveButton"]')
    save_button.click()

    if debug: driver.save_screenshot('er_saved.png')

    time.sleep(10)
    print("Saving the Exploit Prevention policy")
    save_button = driver.find_element_by_xpath('//*[@id="obID_Apply"]')
    save_button.click()
    if debug: driver.save_screenshot('ep_saved.png')


    time.sleep(5)
    if debug: driver.save_screenshot("finished.png")

    print("Closing the browser")
    # Close the browser!
    driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dynamically add an expert rule to a specified policy.')
    parser.add_argument('--epo', help='The url of the epo: https://eposerver.epo:8443', required=True)
    parser.add_argument('--user', help='Username to log into ePO', required=True)
    parser.add_argument('--password', help='Password for the ePO account', required=True)
    parser.add_argument('--policy', help='The policy to which you want to add the Expert Rule', required=True)
    parser.add_argument('--name', help='Name of the expert rule', required=True)
    parser.add_argument('--sev', default=1, type=int, help='Severity of the expert rule', choices=[1, 2, 3, 4])
    parser.add_argument('--action', help='When triggered, should it block or report',
                        choices=['Block', 'Report'], nargs='+')
    parser.add_argument('--rule_type', help='What kind of rule is this?', choices=['Buffer_Overflow', 'Illegal_API_Use', 'ENS_Files', 'Services', 'ENS_Registry', 'ENS_Process'], required=True)
    parser.add_argument('--rule', help='The Expert Rule', required=True)
    parser.add_argument('--notes', help='Any additional notes you want to add to the rule')
    parser.add_argument('--debug', action='store_true', help='print debug messages to stderr')

    args = parser.parse_args()

    if isinstance(args.action, str):
        action = [args.action]
    else:
        action = args.action

    expert_rule = {
        'name': args.name,
        'severity': args.sev,  # 1: Informational, 2: Low, 3: Medium, 4: High
        'action': args.action,  # 'Block' or 'Report', both, or empty list for no action
        'rule_type': args.rule_type,  # 'Buffer_Overflow', 'Illegal_API_Use', 'ENS_Files', 'Services', 'ENS_Registry',
                                      # 'ENS_Process' are options
        'rule_content': args.rule,
        'notes': args.notes
    }

    add_expert_rule(args.epo,
                    args.user,
                    args.password,
                    args.policy,
                    expert_rule,
                    debug=args.debug)
