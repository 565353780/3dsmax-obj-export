#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from base64 import b64encode, b64decode
from flask import Flask, request

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

app = Flask(__name__)

tmp_save_max_file_path = "/home/chli/chLi/tmp/tmp.max"

createFileFolder(tmp_save_max_file_path)

@app.route('/transToObj', methods=['POST'])
def transToObj():
    removeIfExist(tmp_save_max_file_path)

    data = request.get_data()
    data = json.loads(data)
    max_file_base64_data = data['max_file']
    max_file_data = b64decode(max_file_base64_data)
    with open(tmp_save_max_file_path, 'wb') as f:
        f.write(max_file_data)

    result = {'obj_file': None}

    obj_file_data = getBase64Data(tmp_save_max_file_path)
    if obj_file_data is None:
        print("[ERROR]")
        print("\t getBase64Data failed!")
        return json.dumps(result, ensure_ascii=False)

    result['obj_file'] = obj_file_data.decode('utf-8')
    return json.dumps(result, ensure_ascii=False)

app.run(port=9360, host='0.0.0.0')

