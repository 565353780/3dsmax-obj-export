#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

from Config.path import TMP_SAVE_FOLDER_PATH
from Config.signal import START, DATA_IN, DATA_OUT, FINISH

from Method.path import removeIfExist, createFileFolder

def writeData(data_file_path, data, format="wb"):
    createFileFolder(data_file_path)

    with open(data_file_path, format) as f:
        f.write(data)
    return True

def sendSignal(signal_file_name, data="1"):
    signal_file_path = TMP_SAVE_FOLDER_PATH + signal_file_name
    createFileFolder(signal_file_path)

    with open(signal_file_path, "w") as f:
        f.write(data)
    return True

def sendDataIn(signal, data):
    if signal not in START.keys():
        print("[ERROR][signal::sendDataIn]")
        print("\t signal not exist!")
        return False

    data_file_path = TMP_SAVE_FOLDER_PATH + DATA_IN[signal]
    writeData(data_file_path, data)

    sendSignal(START[signal])
    return True

def getDataIn(signal):
    if signal not in DATA_IN.keys():
        print("[ERROR][signal::getDataIn]")
        print("\t signal not exist!")
        return None

    signal_file_path = TMP_SAVE_FOLDER_PATH + START[signal]
    if not os.path.exists(signal_file_path):
        return None

    removeIfExist(signal_file_path)

    data_file_path = TMP_SAVE_FOLDER_PATH + DATA_IN[signal]
    if not os.path.exists(data_file_path):
        print("[ERROR][signal::getData]")
        print("\t data_file not exist!")
        return None

    with open(data_file_path, "rb") as f:
        data = f.read()
    data_json = json.loads(data)

    removeIfExist(data_file_path)
    return data_json

def sendDataOut(signal, data):
    if signal not in DATA_OUT.keys():
        print("[ERROR][signal::sendDataOut]")
        print("\t signal not exist!")
        return False

    data_file_path = TMP_SAVE_FOLDER_PATH + DATA_OUT[signal]
    writeData(data_file_path, data, "w")

    sendSignal(FINISH[signal])
    return True

def getDataOut(signal):
    if signal not in FINISH.keys():
        print("[ERROR][signal::getDataOut]")
        print("\t signal not exist!")
        return None

    signal_file_path = TMP_SAVE_FOLDER_PATH + FINISH[signal]
    while not os.path.exists(signal_file_path):
        continue

    removeIfExist(signal_file_path)

    data = None
    data_file_path = TMP_SAVE_FOLDER_PATH + DATA_OUT[signal]
    with open(data_file_path, "r") as f:
        data = f.read()
    data_json = json.loads(data)

    removeIfExist(data_file_path)
    return data_json

