#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def removeIfExist(file_path):
    if not os.path.exists(file_path):
        return True

    while os.path.exists(file_path):
        try:
            os.remove(file_path)
        except:
            continue
    return True

def createFileFolder(file_path):
    file_name = file_path.split("/")[-1]
    file_folder_path = file_path.split(file_name)[0]
    os.makedirs(file_folder_path, exist_ok=True)
    return True

