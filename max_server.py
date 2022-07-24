#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
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

    def startServer(self, port):
        app = Flask(__name__)

        tmp_save_max_file_path = "D:/tmp/tmp.max"
        tmp_save_obj_file_path = "D:/tmp/tmp.obj"

        createFileFolder(tmp_save_max_file_path)
        createFileFolder(tmp_save_obj_file_path)

        @app.route('/transToObj', methods=['POST'])
        def transToObj():
            removeIfExist(tmp_save_max_file_path)
            removeIfExist(tmp_save_obj_file_path)

            ff = request.files['max_file']
            ff.save(tmp_save_max_file_path)

            result = {
                'code': 200,
                'state': 'failure',
                'obj_file': None,
            }

            if not self.transToObj(tmp_save_max_file_path, tmp_save_obj_file_path):
                print("[ERROR][MaxObjExp::startServer]")
                print("\t transToObj failed!")
                with open("D:/tmp/debug.txt", "a") as f:
                    f.write("transToObj failed!\n")
                return result

            result['state'] = 'success'
            result['obj_file'] = open(tmp_save_obj_file_path, 'rb')
            with open("D:/tmp/debug.txt", "a") as f:
                f.write("transToObj success!\n")
            return result

        app.run(port=port, host='0.0.0.0')
        return True

def demo():
    max_file_path = "C:/Program Files/Autodesk/3ds Max 2023/presets/Particle Flow/earth_Squib Sand01.max"
    save_obj_file_path = "D:/test.obj"

    removeIfExist(save_obj_file_path)

    max_obj_exp = MaxObjExp()
    max_obj_exp.transToObj(max_file_path, save_obj_file_path)
    return True

def demo_flask():
    max_obj_exp = MaxObjExp()
    max_obj_exp.startServer(9360)
    return True

if __name__ == "__main__":
    #  demo()
    demo_flask()

