#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests
from base64 import b64encode, b64decode

def removeIfExist(file_path):
    if not os.path.exists(file_path):
        return True

    os.remove(file_path)
    return True

def createFileFolder(file_path):
    file_name = file_path.split("/")[-1]
    file_folder_path = file_path.split(file_name)[0]
    os.makedirs(file_folder_path, exist_ok=True)
    return True

def getBase64Data(file_path):
    if not os.path.exists(file_path):
        print("[ERROR][demo::getBase64Data]")
        print("\t file not exist!")
        return None

    with open(file_path, 'rb') as f:
        file_data = f.read()
        base64_data = b64encode(file_data).decode().encode('utf-8')
        return base64_data

def getPostResult(max_file_path):
    max_file_data = getBase64Data(max_file_path)
    if max_file_data is None:
        print("[ERROR][demo::getPostResult]")
        print("\t getBase64Data failed!")
        return None

    data = {'max_file': max_file_data.decode('utf-8')}
    result = requests.post('http://192.168.2.15:9360/transToObj', data=json.dumps(data))
    result_json = json.loads(result.text)
    return result_json

def transToObj(max_file_path, save_obj_file_path):
    result = getPostResult(max_file_path)
    obj_file_base64_data = result['obj_file']
    if obj_file_base64_data is None:
        print("[ERROR][demo::getObjFileData]")
        print("\t obj_file_data is None!")
        return False

    createFileFolder(save_obj_file_path)
    removeIfExist(save_obj_file_path)
    obj_file_data = b64decode(obj_file_base64_data)
    with open(save_obj_file_path, 'wb') as f:
        f.write(obj_file_data)
    return True

def demo():
    #  max_file_path = "C:/Program Files/Autodesk/3ds Max 2023/presets/Particle Flow/earth_Squib Sand01.max"
    max_file_path = "/home/chli/chLi/earth_Squib Sand01.max"
    save_obj_file_path = "/home/chli/chLi/test.max"

    transToObj(max_file_path, save_obj_file_path)
    return True

if __name__ == "__main__":
    demo()

