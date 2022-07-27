#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from multiprocessing import Process
from flask import Flask, request

from pymxs import runtime as rt

import sys
sys.path.append("D:/github/3dsmax-obj-export/")

from Method.path import removeIfExist
from Method.encode import getBase64Data, getDecodeData
from Method.load import loadMaxFile, resetMaxFile
from Method.export import exportObj

class MaxObjExp(object):
    def __init__(self):
        return

    def transToObj(self, max_file_path, save_obj_file_path):
        if not loadMaxFile(max_file_path):
            print("[ERROR][MaxObjExp::transToObj]")
            print("\t loadMaxFile failed!")
            return False

        if not exportObj(save_obj_file_path):
            print("[ERROR][MaxObjExp::transToObj]")
            print("\t exportObj failed!")
            return False

        if not resetMaxFile():
            print("[ERROR][MaxObjExp::transToObj]")
            print("\t resetMaxFile failed!")
            return False
        return True

    def outputMaxFilePath(self):
        print("[INFO][MaxObjExp::outputMaxFilePath]")
        print("\t maxFilePath =")
        print(rt.maxFilePath)
        return True

    def outputMaxFileName(self):
        print("[INFO][MaxObjExp::outputMaxFileName]")
        print("\t maxFileName =")
        print(rt.maxFileName)
        return True

def demo():
    max_file_path = "C:/Program Files/Autodesk/3ds Max 2023/presets/Particle Flow/earth_Squib Sand01.max"
    save_obj_file_path = "D:/test.obj"

    removeIfExist(save_obj_file_path)

    max_obj_exp = MaxObjExp()
    max_obj_exp.transToObj(max_file_path, save_obj_file_path)
    return True

def run(app, port):
    app.run(port=port, host='0.0.0.0')

def demo_flask():
    port = 9360
    route = "transToObj"
    tmp_save_folder_path = "D:/tmp/"

    app = Flask(__name__)

    max_obj_exp = MaxObjExp()

    if tmp_save_folder_path[-1] != "/":
        tmp_save_folder_path += "/"
    os.makedirs(tmp_save_folder_path, exist_ok=True)

    tmp_save_max_file_path = tmp_save_folder_path + "tmp.max"
    tmp_save_obj_file_path = tmp_save_folder_path + "tmp.obj"

    @app.route('/' + route, methods=['POST'])
    def transToObj():
        removeIfExist(tmp_save_max_file_path)
        removeIfExist(tmp_save_obj_file_path)

        data = request.get_data()
        data = json.loads(data)
        max_file_base64_data = data['max_file']
        max_file_data = getDecodeData(max_file_base64_data)
        with open(tmp_save_max_file_path, 'wb') as f:
            f.write(max_file_data)

        result = {'obj_file': None}

        if not max_obj_exp.transToObj(tmp_save_max_file_path, tmp_save_obj_file_path):
            print("[ERROR][demo_flask::transToObj]")
            print("\t transToObj failed!")
            return json.dumps(result, ensure_ascii=False)

        obj_file_data = getBase64Data(tmp_save_obj_file_path)
        if obj_file_data is None:
            print("[ERROR]")
            print("\t getBase64Data failed!")
            return json.dumps(result, ensure_ascii=False)

        result['obj_file'] = obj_file_data
        return json.dumps(result, ensure_ascii=False)

    p = Process(target=run, args=(port,))
    p.start()
    return True

def demo_io():
    tmp_save_folder_path = "D:/tmp/"
    max_copy_finished_signal = "max_copy_finished.txt"
    obj_trans_finished_signal = "obj_trans_finished.txt"
    stop_signal = "stop.txt"

    max_obj_exp = MaxObjExp()

    if tmp_save_folder_path[-1] != "/":
        tmp_save_folder_path += "/"
    os.makedirs(tmp_save_folder_path, exist_ok=True)

    max_copy_finished_signal_file_path = tmp_save_folder_path + max_copy_finished_signal
    obj_trans_finished_signal_file_path = tmp_save_folder_path + obj_trans_finished_signal
    stop_signal_file_path = tmp_save_folder_path + stop_signal

    while True:
        if os.path.exists(stop_signal_file_path):
            removeIfExist(stop_signal_file_path)
            break

        if not os.path.exists(max_copy_finished_signal_file_path):
            continue

        tmp_save_max_file_path = tmp_save_folder_path + "tmp.max"
        tmp_save_obj_file_path = tmp_save_folder_path + "tmp.obj"

        file_name_list = os.listdir(tmp_save_folder_path)
        for file_name in file_name_list:
            if file_name[-4:] != ".max":
                continue
            file_basename = file_name.split(".max")[0]
            tmp_save_max_file_path = tmp_save_folder_path + file_basename + ".max"
            tmp_save_obj_file_path = tmp_save_folder_path + file_basename + ".obj"
            break

        removeIfExist(max_copy_finished_signal_file_path)
        removeIfExist(tmp_save_obj_file_path)

        if not max_obj_exp.transToObj(tmp_save_max_file_path, tmp_save_obj_file_path):
            print("[ERROR][MaxObjExp::startServer]")
            print("\t transToObj failed!")

        removeIfExist(tmp_save_max_file_path)
        with open(obj_trans_finished_signal_file_path, "w") as f:
            f.write("1")
    return True

if __name__ == "__main__":
    #  demo()
    #  demo_flask()
    demo_io()

