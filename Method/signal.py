#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from Method.path import createFileFolder

def sendSignal(signal_file_path, signal_data="1"):
    createFileFolder(signal_file_path)

    with open(signal_file_path, "w") as f:
        f.write(signal_data)
    return True

def getSignal(signal_file_path):
    while not os.path.exists(signal_file_path):
        continue

    data = None
    with open(signal_file_path, "r") as f:
        data = f.read()

    while os.path.exists(signal_file_path):
        try:
            os.remove(signal_file_path)
        except:
            continue
    return data

