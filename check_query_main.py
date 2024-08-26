import validate_query
import check_query
import os
import json

## GET CREDS
'''Use this if you need to retreive credentials from an external vault'''
# def creds():
#     '''Retreive credentials from your desire vault.
#     This function must use an API of the vualt you use (Secret Manager/ CyberArk/ etc.)'''
#     esurl = ''
#     es_key = ''

#     creds_data = {
#         'esurl':esurl,
#         'es_key':es_key
#     }

#     return creds_data


## GET .JSON RULE DATA FILE NAME
def get_json():
    '''look for th json file to extract the detection query and other data the check the sytnax.
    Returns an array with the KQL query, query index, and a rule name.'''
    current_dir = os.getcwd()
    files = os.listdir(current_dir)
    json_files = [file for file in files if file.endswith('.json')]
    filename = json_files[0]

    with open(filename, 'r') as file01:
        json_data = json.load (file01)

    rule_kuery = json_data['query']
    rule_name = json_data['name']
    rule_index = json_data['index'][0]

    json_info = {
        'rule_kuery':rule_kuery,
        'rule_name':rule_name,
        'rule_index':rule_index,
        'filename':filename
    }

    return json_info

def main():
    '''Note!
        - validate_query.main get: rule_index & rule_name.
        - validate_query.main trigger validate_query.eql_query() function. 
        - validate_query.eql_query() also get esurl & api_key there.'''
    
    ## GET CREDS (IF NEEDED)
    # credentials = creds()

    ## TRIGGER TO GET JSON FILE
    json_info = get_json()

    ## TRIGGER THE VALIDATE QUERY (SYNTAX CHECK) TO RETURN TRUE/FALSE
    ''' validate_query.main method receive:
        - json_info['rule_index'] = rule index
        - json_info['rule_kuery'] = Elastic EQL query 
        The Method return true/false based on syatax check '''
    boolean = validate_query.main(json_info['rule_index'],
                                  json_info['rule_kuery']) 
    
    ## CHECK FOR RESULTS FROM KUERY
    num_of_results = check_query.check_main(json_info['filename'],
                                            json_info['rule_kuery'],
                                            json_info['rule_index'])
    
    ## PRINT CHECKS OUTPUT
    print("Query Validation Result:", boolean)
    print(f"Numebr of results: {num_of_results}")


## TRIGGER THE CODE
if __name__ == '__main__':
    main()
