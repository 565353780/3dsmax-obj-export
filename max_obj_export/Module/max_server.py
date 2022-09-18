#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from max_obj_export.Config.path import TMP_SAVE_FOLDER_PATH

from max_obj_export.Method.path import removeIfExist
from max_obj_export.Method.signal import getDataIn, sendDataOut
from max_obj_export.Method.encode import getBase64Data, saveData

from max_obj_export.Method.load import loadMaxFile
from max_obj_export.Method.pose import setObjectPos, setObjectScale, setObjectRotation
from max_obj_export.Method.export import exportAll, transMaxToObj

class MaxServer(object):
    def __init__(self):
        return

    def receiveFile(self):
        data = getDataIn('receiveFile')
        if data is None:
            return True

        file_data = data['file_data']
        file_name = data['file_name']
        file_path = TMP_SAVE_FOLDER_PATH + file_name
        saveData(file_data, file_path)

        result = {'state': 'success'}
        sendDataOut('receiveFile', result)
        return True

    def sendFile(self):
        data = getDataIn('sendFile')
        if data is None:
            return True

        result = {
            'file_data': None,
        }

        file_name = data['file_name']
        file_path = TMP_SAVE_FOLDER_PATH + file_name
        if not os.path.exists(file_path):
            print("[WARN][MaxServer::sendFile]")
            print("\t file not exist!")
            sendDataOut('receiveFile', result)
            return False

        result['file_data'] = getBase64Data(file_path)
        sendDataOut('sendFile', result)

    def loadMaxFile(self):
        data = getDataIn('loadMaxFile')
        if data is None:
            return True

        file_name = data['file_name']
        file_path = TMP_SAVE_FOLDER_PATH + file_name
        if not os.path.exists(file_path):
            print("[ERROR][MaxServer::loadMaxFile]")
            print("\t file not exist!")

            result = {'state': 'failed'}
            sendDataOut('loadMaxFile', result)
            return False

        loadMaxFile(file_path)

        if 'pos' in data.keys():
            pos = data['pos']
            setObjectPos(file_name, pos)

        if 'scale' in data.keys():
            scale = data['scale']
            setObjectScale(file_name, scale)

        if 'rotation' in data.keys():
            rotation = data['rotation']
            setObjectRotation(file_name, rotation)

        result = {'state': 'success'}
        sendDataOut('loadMaxFile', result)
        return True

    def exportFile(self):
        data = getDataIn('exportFile')
        if data is None:
            return True

        file_name = data['file_name']

        file_save_path = TMP_SAVE_FOLDER_PATH + file_name
        if not exportAll(file_save_path):
            print("[ERROR][MaxServer::exportFile]")
            print("\t exportAll failed!")

            result = {'state': 'failed'}
            sendDataOut('exportFile', result)
            return False

        result = {'state': 'success'}
        sendDataOut('exportFile', result)
        return True

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
            print("[ERROR][MaxServer::transMaxToObj]")
            print("\t transMaxToObj failed!")
            return False

        removeIfExist(max_file_path)

        obj_data = getBase64Data(save_obj_file_path)
        result = {
            'obj_data': obj_data,
            'mtl_data': None,
        }

        removeIfExist(save_obj_file_path)

        mtl_file_path = TMP_SAVE_FOLDER_PATH + obj_file_basename + ".mtl"
        if os.path.exists(mtl_file_path):
            result['mtl_data'] = getBase64Data(mtl_file_path)

            removeIfExist(mtl_file_path)

        sendDataOut('transMaxToObj', result)
        return True

    def clear(self):
        data = getDataIn('clear')
        if data is None:
            return False

        for file_name in os.listdir(TMP_SAVE_FOLDER_PATH):
            file_path = TMP_SAVE_FOLDER_PATH + file_name
            removeIfExist(file_path)

        result = {'state': 'stop success'}
        sendDataOut('clear', result)
        return True

    def stop(self):
        data = getDataIn('stop')
        if data is None:
            return False

        result = {'state': 'stop success'}
        sendDataOut('stop', result)
        return True
    
    def start(self):
        while True:
            self.receiveFile()
            self.sendFile()
            self.loadMaxFile()
            self.exportFile()
            self.transMaxToObj()
            self.clear()

            if self.stop():
                break
        return True

def demo():
    max_server = MaxServer()
    max_server.start()
    return True

