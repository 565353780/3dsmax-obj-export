#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

from Config.path import TMP_SAVE_FOLDER_PATH

from Method.path import removeIfExist
from Method.export import transMaxToObj
from Method.signal import getDataIn, sendDataOut
from Method.encode import getBase64Data, saveData

class MaxServer(object):
    def __init__(self):
        return

    def transMaxToObj(self):
        data = getDataIn('transMaxToObj')
        if data is None:
            return True

        max_data = data['max_data']
        obj_file_basename = data['obj_file_basename']

        max_file_path = TMP_SAVE_FOLDER_PATH + obj_file_basename + ".max"
        saveData(max_data, max_file_path)

        save_obj_file_path = TMP_SAVE_FOLDER_PATH + obj_file_basename + ".obj"
        if not transMaxToObj(max_file_path, save_obj_file_path):
            print("[ERROR][MaxServer]")
            print("\t transMaxToObj failed!")
            return False

        removeIfExist(max_file_path)

        obj_data = getBase64Data(save_obj_file_path)
        result_json = {
            'obj_data': obj_data,
            'mtl_data': None,
        }

        removeIfExist(save_obj_file_path)

        mtl_file_path = TMP_SAVE_FOLDER_PATH + obj_file_basename + ".mtl"
        if os.path.exists(mtl_file_path):
            result_json['mtl_data'] = getBase64Data(mtl_file_path)

            removeIfExist(mtl_file_path)

        sendDataOut('transMaxToObj', json.dumps(result_json))
        return True

    def stop(self):
        data = getDataIn('stop')
        if data is None:
            return False

        result_json = {'state': 'stop success'}
        sendDataOut('stop', json.dumps(result_json))
        return True
    
    def start(self):
        while True:
            self.transMaxToObj()

            if self.stop():
                break
        return True

def demo():
    max_server = MaxServer()
    max_server.start()
    return True

