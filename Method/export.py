#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymxs import runtime as rt

from Config.max import ALL, NO_PROMPT

def exportObj(save_file_path, selectedOnly=False):
    rt.exportFile(save_file_path, NO_PROMPT,
                  selectedOnly=selectedOnly,
                  using=rt.ObjExp)
    return True

def exportObjOneByOne(self, save_folder_path):
    if save_folder_path[-1] != "/":
        save_folder_path += "/"

    rt.select(ALL)
    select_obj = rt.selection
    for i in range(len(select_obj)):
        rt.select(select_obj[i])
        save_file_path = save_folder_path + str(i) + ".obj"
        self.exportObj(save_file_path, True)
    return True

def exportAllObj(save_file_path):
    rt.select(ALL)
    exportObj(save_file_path, True)
    return True

