import requests
from requests.auth import HTTPBasicAuth
import json
import os

'''
SentinelByte | Aug 26, 2024
References:
- https://www.elastic.co/guide/en/kibana/current/api.html
- https://www.elastic.co/guide/en/kibana/current/create-rule-api.html
- https://www.elastic.co/guide/en/security/8.14/rule-api-overview.html
- https://www.elastic.co/guide/en/security/8.14/rules-api-create.html#ref-fields-all
'''

def get_creds():
    ## ELASTIC SECRETS
    kb_user = ''
    kb_pwd = ''

    ## DETECTION POST URL - TO BE FETCHED FROM AKEYLESS!!
    kb_url = ''
    detection_endpoint = "/api/detection_engine/rules"
    detection_post_url = f'{kb_url}{detection_endpoint}'
    
    ## MORE ENDPOINTS
    # endpoint = "/api/index_management/indices"    # INDEX GET URL
    # endpoint = "/api/alerting/rule"               # ALERTS POST URL
    
    ## QUERY PARAMS
    headers = {
        'Content-Type': 'application/json',
        'kbn-xsrf': 'true'  ## Required for Kibana requests
    }

    creds_data = {'kb_user':kb_user,
                  'kb_pass':kb_pwd,
                  'detection_url':detection_post_url,
                  'headers':headers
    } 

    return creds_data


## KIBANA REQUEST GET
'''Use this function if you want to receive dat afrom kibana
Get request method
Change the endpoint URL based on the data you want to fetch
Make sure you are using credentials with proper permission to fetch the data you desire'''
# def kb_get(query_get_url, headers, kb_user, kb_pwd):
#     # Use this method to fetch all indices for example
#     response = requests.get(query_get_url,
#                             headers=headers,
#                             auth=HTTPBasicAuth(kb_user, kb_pwd))

#     if response.status_code == 200:
#         data = response.json()
#         print(data)
#     else:
#         print(
#             f"Failed to retrieve data:\n{response.status_code} - {response.text}")


## KIBANA REQUEST POST
''''''
def kb_post(detection_post_url, headers, rule_body, kb_user, kb_pwd):
    '''
    Create a detection rule in Kibana via Requests and Kibana API.
    This function gets:
        - detection_post_url = kibana detection url
        - headers = Necessary headers for Kibana request
        - rule_body = The detection rule data
        - kb_user = Kibana username for auth
        - kb_pwd = Kibana password for auth
    '''
    response = requests.post(detection_post_url,
                             headers=headers,
                             json=rule_body,
                             auth=HTTPBasicAuth(kb_user, kb_pwd))

    if response.status_code == 200:
        data = response.json()
        return data
    
    elif response.status_code == 409:
        print("[!] Rule name already exists.\n\t- Delete previous JSON.\n\t- Create a new one via craft_json.py.")

    else:
        print(
            f"Failed to retrieve data:\n{response.status_code} - {response.text}")
        

## MAIN TRIGGER FUNCTION
def main_func():
    '''
    This MAIN function look for json file in current working directory.
    This json file should be created using the create_json.py file.
    Make sure it saves the json files in the right system path you wish.
    Then, trigger creds function to receive credentials.
    Later, trigger the kb_post function which gets:
        - creds['detection_url'] = kibana detection url
        - creds['headers'] = Necessary headers for Kibana request
        - rule_body = The detection rule data
        - creds['kb_user'] = Kibana username for auth
        - creds['kb_pass'] = Kibana password for auth
        '''

    ## LOAD JSON
    current_dir = os.getcwd()
    files = os.listdir(current_dir)
    json_files = [file for file in files if file.endswith('.json')]
    filename = json_files[0]
    with open(filename, 'r') as file1:
        rule_body = json.load(file1)

    ## TRIGGER GET CREDS
    creds = get_creds()

    ## KB FUNCTIONS (GET/POST)
    '''Uncomment kb_get if you wish to fetch data from Kibana'''
    # kb_get(query_get_url, headers, kb_user, kb_pwd)

    '''See funtion explaination above ^^ '''
    kb_post(creds['detection_url'], creds['headers'], rule_body, creds['kb_user'], creds['kb_pass'])


'''SentinelByte | Aug 26, 2024'''
if __name__ == '__main__':
    main_func()
