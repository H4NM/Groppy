import requests
from settings import *

def get_request_elastic(url: str, credentials: str=None, request_body: dict=None, cert: str=None, api_key: str=None) -> object:
    request_headers = { 'user-agent': '{}/{}'.format(app_title,app_version), 'content-type': 'application/json'}
    if api_key:
        request_headers['Authorization'] = 'ApiKey {}'.format(api_key)
    
    response = requests.get(url, auth=credentials, json=request_body, verify=cert,  headers=request_headers, timeout = requests_timeout)

    if not response.status_code == 200:
        raise ConnectionError(response.text)
    return response

def retrieve_requested_field(es_response: dict, field: str, unique: bool=True) -> list:
    field_list = []
    for doc in es_response['hits']['hits']:
        if 'fields' in doc:
            data_from_field = doc['fields'][field][0]
            if unique and data_from_field in field_list:
                continue
            field_list.append(data_from_field)
    return field_list


def populate_json(field: str, query: str) -> dict:
    return {
        "query":{
             "query_string": {
                "query": query,
            }
        },
        "fields":[field],
        "_source": False,
        "size": es_max_docs
    }

def get_field_names(fields: dict) -> list:
    global all_parsed_fields
    all_parsed_fields=[]
    recurse_get_field_names(fields, [])
    return all_parsed_fields

def recurse_get_field_names(fields: dict, prev_list: list):
    global all_parsed_fields
    for key in fields:
        prev_list.append(key)
        if "properties" in fields[key]:
            recurse_get_field_names(fields[key]["properties"], prev_list)
            prev_list = []
        else:
            all_parsed_fields.append(".".join(prev_list))
            prev_list.pop()