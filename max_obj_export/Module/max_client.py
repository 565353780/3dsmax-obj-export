#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../method-manage/")

import json
import requests

from method_manage.Method.encode import getBase64Data, saveData

class MaxClient(object):
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port

        self.url = "http://" + self.server_ip + ":" + str(self.server_port) + "/"
        return

    def getPostResult(self, route, data):
        result = requests.post(self.url + route, data=json.dumps(data)).text
        try:
            result_json = json.loads(result)
        except:
            print("[ERROR][MaxClient::getPostResult]")
            print("\t result not valid! result is:")
            print(result)
            return None
        return result_json

    def transMaxToObj(self, max_file_path, save_obj_file_path):
        max_data = getBase64Data(max_file_path)
        if max_data is None:
            print("[ERROR][MaxClient::getPostResult]")
            print("\t getBase64Data failed!")
            return None

        obj_file_basename = save_obj_file_path.split("/")[-1].split(".obj")[0]
        data = {'max_data': max_data, 'obj_file_basename': obj_file_basename}

        result = self.getPostResult('transMaxToObj', data)
        if result is None:
            print("[ERROR][MaxClient::transMaxToObj]")
            print("\t getPostResult failed!")
            return False

        obj_data = result['obj_data']
        if obj_data is None:
            print("[ERROR][MaxClient::transMaxToObj]")
            print("\t obj_data is None!")
            return False

        saveData(obj_data, save_obj_file_path)

        save_mtl_file_path = save_obj_file_path.replace(".obj", ".mtl")
        mtl_data = result['mtl_data']

        if mtl_data is not None:
            saveData(mtl_data, save_mtl_file_path)
        return True

    def stop(self):
        _ = self.getPostResult('stop', {'stop': 'start'})
        return True

def demo():
    server_ip = "192.168.2.15"
    server_port = 9365

    #  max_file_path = "C:/Program Files/Autodesk/3ds Max 2023/presets/Particle Flow/earth_Squib Sand01.max"
    max_file_path = "/home/chli/chLi/tmp.max"
    save_obj_file_path = "/home/chli/chLi/test.obj"

    max_client = MaxClient(server_ip, server_port)
    max_client.transMaxToObj(max_file_path, save_obj_file_path)

    #  max_client.stop()
    return True

