import re
import requests
from requests.auth import HTTPBasicAuth
import json
import random
import string

'''
SentintelByte
Date: 26 Aug 2024
'''

def get_creds():
    '''This function manage all necessary credentials.
    Use your own Vualt (AWS Secret Manager/ Akeyless/ CyberArk) to retrieve these keys securly.
    This Function do not receive any arguments. Just fetch keys from a secret manager.
    Finally it return an array of creds necessary for other functions to run.
        kb_user = Kibana endpoint username
        kb_pwd = Kibana endpointpassword
        es_key = Elastic token
        es_url = Base url for yourr elastic endpoint
        detection_endpoint = API endpoint for elastic connectors (to be able to set actions)
    '''
    ## KIBANA USER
    kb_user = ''

    ## KIBANA PASSWORD
    kb_pwd = ''

    ## ELASTIC TOKEN
    es_key = ''

    ## ELASTIC URL
    es_url = ''

    ## KIBANA DETECTION POST URL
    kb_url = ''
    detection_endpoint = "/api/actions/connectors"  # ENDPOINT PATH
    connector_url = f'{kb_url}{detection_endpoint}'  # FULL API URL

    # QUERY PARAMS
    headers = {
        'Content-Type': 'application/json',
        'kbn-xsrf': 'true'  # REQUIRED FOR KNB REQUESTS
    }

    # JSON WITH CREDS
    creds = {
        'kb_user': kb_user,
        'kb_pass': kb_pwd,
        'es_key': es_key,
        'connectors_url': connector_url,
        'headers': headers,
        'es_url':es_url
    }

    return creds


# GET KIBANA CONNECTOR NAMES & IDs
''' API - GET kbn:/api/actions/connectors '''


def kb_get(kb_url, headers, kb_user, kb_pass):
    connectors = []
    # Used this methid to fetch all indices for example
    response = requests.get(kb_url,
                            headers=headers,
                            auth=HTTPBasicAuth(kb_user, kb_pass))

    if response.status_code == 200:
        data = response.json()
        for connector in data:
            connectors.append(f"{connector['name']}:{connector['id']}")
    else:
        print(
            f"Failed to retrieve data:\n{response.status_code}-{response.text}")

    return connectors


def construct_connectors(kb_url=creds['connectors_url'], headers=creds['headers'], kb_user=creds['kb_user'], kb_pass=creds['kb_pass']):
    # CONSTRUCT CONNECTOR LIST FOR USER REFERENCE
    get_connector_list = kb_get(kb_url, headers, kb_user, kb_pass)
    num = 0
    final_conn_list = []
    while len(get_connector_list) > num:
        for object in get_connector_list:
            final_conn_list.append(f'{num} - {get_connector_list[num]}')
            num += 1

    return final_conn_list


# REGEX CHECK FOR TAGS
def input_with_commas(tags):
    '''This function checks if custom tags are seperated as needed for an array [] construction'''
    # pattern = r'^([a-z0-9*]+)(?:,([a-z0-9*]+))*$'
    pattern = r'^([a-z0-9_*]+)(?:,([a-z0-9_*]+))*$'

    return bool(re.match(pattern, tags))


def syntax_check(data, datatype):
    '''This function get data source (tags/index).
    Chceck syntax based on a specific criteria mention in KB API'''
    while input_with_commas(data) == False:
        print("Syntax isn't correct")
        data = input(
            f"[+] Insert {datatype} Seperated by commas (,)\nexample,*aa*,bbb,111*\n > ")
    else:
        data_list = [word.strip() for word in data.split(',')]
        return data_list


## CHECK RULE NAME FOR FILE NAME SYNTAX
def check_unsupported_characters(unsupported_chars, rulename):
    '''This function receives the rule name the user insert
    And check for pre defined unsupported characters.
    This is based on a Unix/Windows FS specifications'''
    unsupported_chars = re.findall(unsupported_chars, rulename)

    if unsupported_chars:
        return True, list(set(unsupported_chars))
    else:
        return False, []


## GENERATE RANDOM RULE ID
def generate_random_string():
    '''This function uses the random() lib to create a 32 bit long rule ID'''
    segment_lengths = [8, 4, 4, 4, 12]
    segments = []

    for length in segment_lengths:
        segment = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        segments.append(segment)

    return '-'.join(segments)


# INPUT FROM USER, SYNTAX CHECKS & ARRAY CONSTRUCTION
def data(conn_list):
    '''
    1. This function Recieves:
        - conn_list = connector list from Kibana
        - User inputs
    2. Check user input syntax.
    3. Construct connector IDs.
    4. Construct JSON for rule creation.
    ** Note! this function can get more params for rule creation. refer to: 
        https://www.elastic.co/guide/en/security/current/rule-api-overview.html
    '''
    ## PLATFORM
    '''Logs data source. e.g. azure/aws/windows/etc.'''
    platform = input(
        '[+] Enter Platform name\ne.g. Azure, AWS, OKTA, etc.\n> ')

    ## RULE NAME
    unsupported_chars = r'[\\/:*?"<>|]'
    while True:
        rulename = input("[+] Choose Rule Name\n> ")
        has_unsupported, chars = check_unsupported_characters(
            unsupported_chars,  rulename)
        if has_unsupported:
            print(f"[NOTE] Unsupported characters found: {chars}")
        else:
            print(f"[OK] {rulename} is Valid. Pls Continue.")
            break

    ## RULE INDEX
    indices = input(
        "[+] Insert a single Index - e.g. *test*\n> ")
    index_list = syntax_check(indices, 'Indices')

    ## KUERY + SYNTAX CHECK
    detection_query = input(
        "[+] Insert Your Query (Kuery Syntax)\ne.g. '_index:example_index AND _id:example_id'\n> ")
    '''Uncomment the following lines if a syntax check is necessary'''
    # try:
    #     boolean = validate_query.main(index_list, detection_query)
    #     while boolean == False:
    #         detection_query = input(
    #             "[NOTE] Query or Index are NOT valid\nTry again or contact team lead for further help.\nSee examples below:\n\tINDEX:*test*\n\tQUERY:'_index:aws AND _id:jS_QAJEB67nTnoI_wr7r'\nEnter new Query\n> ")
    #         indices = input("[+] Make sure U enter the right index pattern.\nValidate index in Kibana GUI.\nEnter new valid index> ")
    #         index_list = syntax_check(indices, 'Indices')
    #         boolean = validate_query.main(index_list, detection_query)

    #         if detection_query == True:
    #             print("Query Validation Result:", boolean)
    #             break
    #         else:
    #             continue

    # except Exception as e:
    #     print(f"[NOTE] Error - {e}")
    #     print("Please try again or contact team lead for further help.")


    ## RULE DESCRIPTION
    description = ''
    while len(description) == 0:
        description = input("[+] Rule Description\n> ")

    ## TAGS (MATURITY, PLATFORM, RISK, USER_APPROACH, AUTO_REM, TECTIC)
    '''Tags can be cahnged base on your needs
    Make sure to remove any unnecessary tags and insert those you want.
    Finally make sure U append anything to "tags".
    Note that "tags" is an array list'''
    tags = []
    print("[+] Mendatory Tags:\n ")
    tags.append(f"platform:{platform.lower()}")  ## PLATFORM TAG

    maturity = input(
        "[+] Choose maturity level\n\t(1) Staging\n\t(2) Production\n> ")  ## MATURITY TAG
    if int(maturity) == 1:
        tags.append("maturity:staging")
    elif int(maturity) == 2:
        tags.append("maturity:production")

    risk_tag = input(
        "[+] Choose Risk (Choose No.)\n\t(1) Incident\n\t(2) Misconfiguration\n\t(3) Compliance\n\t(4) Monitoring\n> ")  ## RISK TAGS
    if int(risk_tag) == 1:
        tags.append("risk:incident")
        tactics = {'1': 'initial access',
                   '2': 'execution',
                   '3': 'persistence',
                   '4': 'privilege escalation',
                   '5': 'defense evasion',
                   '6': 'credential access',
                   '7': 'discovery',
                   '8': 'lateral movement',
                   '9': 'collection',
                   '10': 'exfiltration',
                   '11': 'command and control',
                   '12': 'impact'
                   }  # TACTICS

        tactic_num = input("[+] Choose Attack Tactic (Choose No.):\n\t(1) initial access\n\t(2) execution\n\t(3) persistence\n\t(4) privilege escalation\n\t(5) defense evasion\n\t(6) credential access\n\t(7) discovery\n\t(8) lateral movement\n\t(9) collection\n\t(10) exfiltration\n\t(11) command & control\n\t(11) impact\n> ")
        tactic_choosen = tactics[f'{tactic_num}']
        tags.append(f"tactic:{tactic_choosen}")

    elif int(risk_tag) == 2:
        tags.append("risk: misconfiguration")
    elif int(risk_tag) == 3:
        tags.append("risk: compliance")
    elif int(risk_tag) == 4:
        tags.append("risk: monitoring")

    user_approach = input(
        "[+] Does User Approach?\n\t(1) False\n\t(2) True\n> ")  # USER APPROACH
    if int(user_approach) == 1:
        tags.append("user approach: false")
    elif int(user_approach) == 2:
        tags.append("user approach: true")

    auto_remediation = input(
        "[+] Does auto remediation exists?\n\t(1) False\n\t(2) True\n> ")  # AUTO REMEDIATION
    if int(auto_remediation) == 1:
        tags.append("auto remediation: false")
    elif int(auto_remediation) == 2:
        tags.append("auto remediation: true")

    '''Other custome detection rule tags'''
    other_tags = input(
        "[+] Insert Other Tags Seperated by commas (,)\ne.g. example,*aa*,bbb,111*\n> ")  # CUSTOM TAGS

    '''Syntax check for other (custom) tags the user inserts'''
    syntax_check(other_tags, 'Tags')
    other_tags = other_tags.split(',')
    for custom_tag in other_tags:
        custom_tag.lower()
        tags.append(custom_tag)

    ## KIBANA CONNECTORS
    print('~~~ Connector list ~~~')
    for object in conn_list:
        print(object)

    while True:
        choose_torq_connector_num = input(
            f"[+] Choose Torq connector from the list above.\nChoice Must be INT!\n> ")
        try:
            int_value = int(choose_torq_connector_num)
            colon_pos = conn_list[int_value].find(':')
            choosen_connector = conn_list[int_value][colon_pos + 1:]
            print("~~~~~~~~~\nChoosen Connector: ", choosen_connector)
            break
        except ValueError:
            print(
                "[-] Not valid integer. Choose connector number from the list above ^")

    ## RULE ID STRING
    '''Generate random 32bit long for rule ID'''
    rule_id = generate_random_string()


    ## SEVERITY RATING STRING
    severity = input("[+] Severity Tag [low/ medium/ high/ critical]\n> ")

    ## RISK SCORE
    while True:
        risk_score = input(
            "[+] Choose Rule Risk Score between - Only Numbers 1-100\n> ")
        if risk_score.isdigit():
            if 0 < int(risk_score) <= 100:
                break
        else:
            risk_score = input(
                "[+] Choose Rule Risk Score between - Only Numbers 1-100\n> ")

    ## CREATOR NAME
    creator_name = input("Pls Enter your name here > ")

    ## FALSE POSITIVE CASES [ARRAY]
    false_positives = input(
        "Insert false positive cases seperated by commas (,)\n> ")
    false_positive_list = syntax_check(false_positives, 'false positive')

    print('~~~~~~~~~~~\nFinal JSON\n~~~~~~~~~~~')
    ## CONSTRUCT RULE DATA IN A JSON FORMAT
    json_data = {
        "rule_id": rule_id,
        "risk_score": int(risk_score),
        "description": description.lower(),
        "interval": '30m',
        "name": f"{platform}_{rulename}".lower(),
        "severity": severity,
        "tags": tags,
        "type": "query",
        "from": f"now-45m",
        "query": detection_query.lower(),
        "language": "kuery",
        "filters": [
            {
                "query": {
                    "match": {
                        "event.action": {
                            "query": "Process Create (rule: ProcessCreate)",
                            "type": "phrase"
                        }
                    }
                }
            }
        ],
        "index": index_list,
        "actions": [
            {
                "action_type_id": ".torq",
                "group": "default",
                "id": choosen_connector,
                "params": {
                    "message": "{{context.rule.description}}"
                }
            }
        ],
        "author": [f"{creator_name.lower()}"],
        "false_positives": false_positive_list,
        "enabled": False
    }
    
    print(json_data)
    rule_json = json.dumps(json_data, indent=4)
    return rule_json, rulename, platform


def send_json(json_data, rule_name, platform):
    '''
    This function receives:
        - json_data = A json with the detection info (based on user inputs)
        - rule_name = The rule name for the file name
        - platform = Platform of the logs data source
    Create the json file'''
    with open(f'{platform}_{rule_name}.json'.lower(), 'w') as file01:
        file01.write(json_data)
        # json.dump(json_data)


if __name__ == "__main__":
    ## CALL THE CREDS() FUNCTION TO GET ALL CREDS
    creds = get_creds()

    ## TRIGGER TO GET KB CONNECTORS
    conn_list = construct_connectors(kb_url=creds['connectors_url'],
                                     headers=creds['headers'],
                                     kb_user=creds['kb_user'],
                                     kb_pass=creds['kb_pass'])

    ## TRIGGER TO GET USER INPUT FOR JSON RULE DATA
    rule_data = data(conn_list)
    # rule_name = rule_data['name']

    ## TRIGGER JSON FILE WRITING TO CURRENT DIR
    send_json(rule_data[0], rule_data[1], rule_data[2])   ## 0 > JSON DATA | 1 > RULE NAME
