from elasticsearch import Elasticsearch                 ## ES SDK
# from elastic_transport import RequestsHttpNode        ## UNMARK IF RUNING BEHIND PROXY
# from datetime import datetime, timedelta, timezone    ## UNMARK TO USE CUSTOM TIME

## TIMEFRAME 2D /7D /30D
'''Uncomment this if U want to change the search timeframe
Once in use, must change the <gte> value in query_string var below'''
# current_time = datetime.now(timezone.utc)
# start_time = current_time - timedelta(days=3)
# fcurrent_time = current_time.strftime('%Y-%m-%dT%H:%M:%S')
# fstart_time = start_time.strftime('%Y-%m-%dT%H:%M:%S')

# PROXIES (IF NEEDED)
proxies = {
    'http_proxy': '',
    'https_proxy': ''
}

## CONSTRUCT DSL QUERY TO CHECK FOR RESULTS IN LAST ONE WEEK
def eql_query(esurl, es_key, rule_kuery, rule_index):
    '''
    This function get elastic url, elastic token, query search, and index.
    It return the number of results (if so) matched in the past week.
    Note! Configure a class CustomHttpNode(RequestsHttpNode) if needed to run behind proxy
    '''
    es = Elasticsearch(
        esurl,
        api_key=es_key,
        # node_class=CustomHttpNode ## use this if using proxy
    )

    query_string = {
        "query": {
            "bool": {
                "must": [
                    {
                        "query_string": {
                            "query": f"{rule_kuery}"
                        }
                    },
                    {
                        "range": {
                            "@timestamp": {
                                "gte": "now-1w/w", ## here you can adjust the time as needed. defult I set to 1week.
                                "lt": "now"
                            }
                        }
                    }
                ]
            }
        }
    }

    try:
        response = es.search(index=rule_index, body=query_string)
        '''
        Using the search method from elasticsearch library.
        Uncomment next 3 line if result data is needed
        For hit in response['hits']['hits']:
            print(hit['_source'])
        num_results = response._body['hits']['total']['value']'''
        
        num_results = response._body['hits']['total']['value']

    except Exception as e:
        print(f"[X] Error executing EQL query: {e}")

    return num_results


def check_main(filename, rule_kuery, rule_index):
    '''This function is a child one of check_query_main.py.
    Receives:
        - filename = json file name
        - rule_kuery = search query
        - rule_index = index to search in
        '''
    filename = filename

    '''get your elk creds from anywhere you saved them.
    Make sure to retreive them securely - do not save them hardcoded here!!!'''
    esurl = ''
    es_key = ''

    ## TRIGGER eql_query FUNCTION
    results = eql_query(esurl, es_key, rule_kuery, rule_index)

    ## PRINT RESULTS
    print(f"Provided query resulted with {results} results")
