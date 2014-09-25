import requests
import json
import time
from collections import defaultdict


base_url = "http://localhost:9080/"

def _requestNERService(request_url, request_args):
    url = base_url + request_url
    headers = {'content-type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(request_args))
    if str(response.status_code) not in ['201', '200']:
        return {}
    return response.json()


def get_entities(doc, base_org=None):
    args = {'id': '0', 'contents': doc}
    response = _requestNERService('process_doc', args)
    '''res = []
    if base_org:
        if "ORGANIZATION" in response.keys():
            response["ORGANIZATION"].append(base_org.lower())
        else:
            response["ORGANIZATION"] = [base_org.lower()]
    for key in response.keys():
        response[key] = [x.lower() for x in response[key] if len(x.split()) < 5]
        response["DE" + key] = get_dedup_dict(list(response[key]))
        response["ID" + key] = get_dedup_index(response["DE" + key])
        res.extend(response[key])
    response['ALL'] = res'''
    return response


def get_dedup_dict(res):
    deDict = {}
    idx = 1
    while res:
        check_entity = res.pop()
        for x in res:
            if check_entity in x or x in check_entity:
                temp_id = None
                if check_entity in deDict.keys():
                    temp_id = deDict[check_entity]
                elif x in deDict.keys():
                    temp_id = deDict[x]
                else:
                    temp_id = idx
                    idx += 1
                deDict[check_entity] = temp_id
                deDict[x] = temp_id
        if check_entity not in deDict.keys():
            deDict[check_entity] = idx
            idx += 1
    return deDict

def get_dedup_index(res):
    deDict = defaultdict(list)
    for x in res.keys():
        deDict[res[x]].append(x)
    return deDict
