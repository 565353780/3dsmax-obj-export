#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests

from Method.path import removeIfExist, createFileFolder
from Method.encode import getBase64Data, getDecodeData

class MaxObjExpClient(object):
    def __init__(self, server_ip, server_port, server_route):
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_route = server_route

        self.url = "http://" + self.server_ip + ":" + str(self.server_port) + "/" + self.server_route
        return

    def getPostResult(self, max_file_path):
        max_file_data = getBase64Data(max_file_path)
        if max_file_data is None:
            print("[ERROR][MaxObjExpClient::getPostResult]")
            print("\t getBase64Data failed!")
            return None

        data = {'max_file': max_file_data}
        result = requests.post(self.url, data=json.dumps(data)).text
        try:
            result_json = json.loads(result)
        except:
            print("[ERROR][MaxObjExpClient::getPostResult]")
            print("\t result not valid! result is:")
            print(result)
            return None
        return result_json

    def transToObj(self, max_file_path, save_obj_file_path):
        result = self.getPostResult(max_file_path)
        if result is None:
            print("[ERROR][MaxObjExpClient::transToObj]")
            print("\t getPostResult failed!")
            return False

        obj_file_base64_data = result['obj_file']
        if obj_file_base64_data is None:
            print("[ERROR][MaxObjExpClient::transToObj]")
            print("\t obj_file_data is None!")
            return False

        createFileFolder(save_obj_file_path)
        removeIfExist(save_obj_file_path)
        obj_file_data = getDecodeData(obj_file_base64_data)
        with open(save_obj_file_path, 'wb') as f:
            f.write(obj_file_data)
        return True

def demo():
    server_ip = "192.168.2.16"
    server_port = 9360
    server_route = "transToObj"
    #  max_file_path = "C:/Program Files/Autodesk/3ds Max 2023/presets/Particle Flow/earth_Squib Sand01.max"
    max_file_path = "/home/chli/chLi/tmp.max"
    save_obj_file_path = "/home/chli/chLi/test.obj"

    max_obj_exp_client = MaxObjExpClient(server_ip, server_port, server_route)
    max_obj_exp_client.transToObj(max_file_path, save_obj_file_path)
    return True

