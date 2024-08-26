from elasticsearch import Elasticsearch             # ES SDK
# from elastic_transport import RequestsHttpNode    # UNMARK THIS IF USING PROXY

## PROXIES (IF NEEDED)
'''Uncomment next 4 lines to use proxies'''
# proxies = {
#     "http_proxy": "",
#     "https_proxy": ""
# }

def eql_query(esurl, api_key, index, eql_kuery):
    '''Ajust the class CustomHttpNode(RequestsHttpNode) to use proxy if needed
    If used - make sure to unmark the node_class=CustomHttpNode in the es param below'''
    
    es = Elasticsearch(
        esurl,
        api_key=api_key,
        # node_class=CustomHttpNode
    )

    '''Making a request using built in elasticsearch validate query
    This should return true/false.
    Indicating query is working or not'''
    try:
        response = es.indices.validate_query(index=index, q=eql_kuery, explain='true')
        if response._body['valid'] == True:
            return True 
        else:
            return False
        
    except Exception as e:
        return f"Error executing EQL query: {e}"
    

def main(index, eql_kuery):
    '''This is a child function of check_query_main.py  
    Triggered by check_query_main.py.'''
    # ELASTIC CREDS
    es_key = ''
    esurl = ''

    ## TRIGGER eql_query() FUNCTION
    results = eql_query(esurl, es_key, index, eql_kuery)

    ## RETURN RESULTS (TRUE/FALSE)
    return results
