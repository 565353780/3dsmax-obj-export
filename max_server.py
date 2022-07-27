#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import sys
sys.path.append("D:/github/3dsmax-obj-export/")

from Method.path import removeIfExist
from Method.export import transToObj

def demo():
    tmp_save_folder_path = "D:/tmp/"
    max_copy_finished_signal = "max_copy_finished.txt"
    obj_trans_finished_signal = "obj_trans_finished.txt"
    stop_signal = "stop.txt"

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

        if not transToObj(tmp_save_max_file_path, tmp_save_obj_file_path):
            print("[ERROR][MaxObjExp::startServer]")
            print("\t transToObj failed!")

        removeIfExist(tmp_save_max_file_path)
        with open(obj_trans_finished_signal_file_path, "w") as f:
            f.write("1")
    return True

if __name__ == "__main__":
    demo()

