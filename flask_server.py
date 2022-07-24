#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from flask import Flask, request

from Method.path import removeIfExist
from Method.encode import getBase64Data, getDecodeData
from Method.signal import sendSignal, getSignal

def demo():
    port = 9360
    route = "transToObj"
    tmp_save_folder_path = "D:/tmp/"
    max_copy_finished_signal = "max_copy_finished.txt"
    obj_trans_finished_signal = "obj_trans_finished.txt"
    stop_signal = "stop.txt"

    app = Flask(__name__)

    if tmp_save_folder_path[-1] != "/":
        tmp_save_folder_path += "/"
    os.makedirs(tmp_save_folder_path, exist_ok=True)

    max_copy_finished_signal_file_path = tmp_save_folder_path + max_copy_finished_signal
    obj_trans_finished_signal_file_path = tmp_save_folder_path + obj_trans_finished_signal
    stop_signal_file_path = tmp_save_folder_path + stop_signal

    @app.route('/' + route, methods=['POST'])
    def transToObj():
        data = request.get_data()
        data = json.loads(data)

        obj_file_basename = data['obj_file_basename']
        tmp_save_file_basepath = tmp_save_folder_path + obj_file_basename
        tmp_save_max_file_path = tmp_save_file_basepath + ".max"
        tmp_save_obj_file_path = tmp_save_file_basepath + ".obj"
        tmp_save_mtl_file_path = tmp_save_file_basepath + ".mtl"

        removeIfExist(tmp_save_max_file_path)
        removeIfExist(max_copy_finished_signal_file_path)
        removeIfExist(tmp_save_obj_file_path)
        removeIfExist(tmp_save_mtl_file_path)
        removeIfExist(obj_trans_finished_signal_file_path)

        max_file_base64_data = data['max_file']
        max_file_data = getDecodeData(max_file_base64_data)

        with open(tmp_save_max_file_path, 'wb') as f:
            f.write(max_file_data)

        sendSignal(max_copy_finished_signal_file_path)

        result = {'obj_file': None, 'mtl_file': None}

        getSignal(obj_trans_finished_signal_file_path)
        if not os.path.exists(tmp_save_obj_file_path):
            print("[ERROR][demo::transToObj]")
            print("\t transToObj failed!")
            removeIfExist(tmp_save_obj_file_path)
            removeIfExist(tmp_save_mtl_file_path)
            return json.dumps(result, ensure_ascii=False)

        obj_file_data = getBase64Data(tmp_save_obj_file_path)
        if obj_file_data is None:
            print("[ERROR]")
            print("\t getBase64Data failed!")
            removeIfExist(tmp_save_obj_file_path)
            removeIfExist(tmp_save_mtl_file_path)
            return json.dumps(result, ensure_ascii=False)
        result['obj_file'] = obj_file_data

        if os.path.exists(tmp_save_mtl_file_path):
            mtl_file_data = getBase64Data(tmp_save_mtl_file_path)
            if mtl_file_data is not None:
                result['mtl_file'] = mtl_file_data
        removeIfExist(tmp_save_obj_file_path)
        removeIfExist(tmp_save_mtl_file_path)
        return json.dumps(result, ensure_ascii=False)

    @app.route('/stop', methods=['POST'])
    def stop():
        sendSignal(stop_signal_file_path)
        exit()

    app.run('0.0.0.0', port)
    return True

if __name__ == "__main__":
    demo()

