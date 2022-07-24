#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from base64 import b64encode, b64decode
from multiprocessing import Process
from flask import Flask, request

from pymxs import runtime as rt

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

class MaxObjExp(object):
    def __init__(self):
        self.all = rt.Name('all')
        self.no_prompt = rt.Name('noPrompt')
        return

    def loadMaxFile(self, max_file_path):
        if not os.path.exists(max_file_path):
            print("[ERROR][MaxObjExp::loadMaxFile]")
            print("\t max_file not exist!")
            return False

        rt.loadMaxFile(max_file_path)
        return True

    def resetMaxFile(self):
        rt.resetMaxFile(self.no_prompt)
        return True

    def exportObj(self, save_file_path, selectedOnly=False):
        rt.exportFile(save_file_path, self.no_prompt,
                      selectedOnly=selectedOnly,
                      using=rt.ObjExp)
        return True

    def exportObjOneByOne(self, save_folder_path):
        if save_folder_path[-1] != "/":
            save_folder_path += "/"

        rt.select(self.all)
        select_obj = rt.selection
        for i in range(len(select_obj)):
            rt.select(select_obj[i])
            save_file_path = save_folder_path + str(i) + ".obj"
            self.exportObj(save_file_path, True)
        return True

    def exportAllObj(self, save_file_path):
        rt.select(self.all)
        self.exportObj(save_file_path, True)
        return True

    def transToObj(self, max_file_path, save_obj_file_path):
        if not self.loadMaxFile(max_file_path):
            print("[ERROR][MaxObjExp::transToObj]")
            print("\t loadMaxFile failed!")
            return False

        if not self.exportObj(save_obj_file_path):
            print("[ERROR][MaxObjExp::transToObj]")
            print("\t exportObj failed!")
            return False

        if not self.resetMaxFile():
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
        max_file_data = b64decode(max_file_base64_data)
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

        result['obj_file'] = obj_file_data.decode('utf-8')
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

    tmp_save_max_file_path = tmp_save_folder_path + "tmp.max"
    tmp_save_obj_file_path = tmp_save_folder_path + "tmp.obj"

    max_copy_finished_signal_file_path = tmp_save_folder_path + max_copy_finished_signal
    obj_trans_finished_signal_file_path = tmp_save_folder_path + obj_trans_finished_signal
    stop_signal_file_path = tmp_save_folder_path + stop_signal

    while True:
        if not os.path.exists(max_copy_finished_signal_file_path):
            continue

        removeIfExist(max_copy_finished_signal_file_path)
        removeIfExist(tmp_save_obj_file_path)

        if not max_obj_exp.transToObj(tmp_save_max_file_path, tmp_save_obj_file_path):
            print("[ERROR][MaxObjExp::startServer]")
            print("\t transToObj failed!")

        removeIfExist(tmp_save_max_file_path)
        with open(obj_trans_finished_signal_file_path, "w") as f:
            f.write("1")

        if os.path.exists(stop_signal_file_path):
            removeIfExist(stop_signal_file_path)
            break
    return True

if __name__ == "__main__":
    #  demo()
    #  demo_flask()
    demo_io()

