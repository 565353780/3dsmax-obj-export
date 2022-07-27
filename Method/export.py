#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymxs import runtime as rt

from Config.max import NO_PROMPT
from Config.export import EXPORT

from Method.load import loadMaxFile, resetMaxFile
from Method.obj_filter import getNames
from Method.select import selectObjects, selectAll, deSelectAll

def exportFile(save_file_path, selectedOnly):
    file_type = save_file_path.split(".")[-1]

    if file_type not in EXPORT.keys():
        print("[ERROR][export::exportFile]")
        print("\t file_type not valid!")
        return False

    rt.exportFile(save_file_path, NO_PROMPT,
                  selectedOnly=selectedOnly,
                  using=EXPORT[file_type])
    return True

def exportSelection(save_file_path):
    if not exportFile(save_file_path, True):
        print("[ERROR][export::exportSelection]")
        print("\t exportFile failed!")
        return False
    return True

def exportAll(save_file_path):
    #  selection_names = getNames(rt.selection)

    #  selectAll()
    if not exportFile(save_file_path, False):
        print("[ERROR][export::exportAll]")
        print("\t exportFile failed!")
        return False
    #  deSelectAll()

    #  if not selectObjects(selection_names):
        #  print("[ERROR][export::exportAll]")
        #  print("\t selectObjects failed!")
        #  return False

    return True

def transMaxToObj(max_file_path, save_obj_file_path):
    if not loadMaxFile(max_file_path):
        print("[ERROR][export::transMaxToObj]")
        print("\t loadMaxFile failed!")
        return False

    if not exportAll(save_obj_file_path):
        print("[ERROR][export::transMaxToObj]")
        print("\t exportObj failed!")
        return False

    if not resetMaxFile():
        print("[ERROR][export::transMaxToObj]")
        print("\t resetMaxFile failed!")
        return False
    return True

