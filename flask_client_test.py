#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../method-manage/")

import json
import requests

def getPostResult(url, route, data):
    result = requests.post(url + route, data=json.dumps(data)).text
    try:
        result_json = json.loads(result)
    except:
        print("[ERROR][flask_client_test::getPostResult]")
        print("\t result not valid! result is:")
        print(result)
        return None
    return result_json

def demo():
    url = "http://192.168.2.15:9365/"

    getPostResult(url, "transMaxToObj", "")
    return True

