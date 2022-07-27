#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scipy.spatial.transform import Rotation as R

import pymxs
from pymxs import runtime as rt

def getNames(object_list):
    name_list = []
    for obj in object_list:
        name_list.append(obj.name)
    return name_list

def getObjectByIdx(object_idx):
    if object_idx >= len(rt.objects):
        print("[ERROR][conrtol::getObjectByIdx]")
        print("\t object_idx out of range!")
        return None
    return rt.objects[object_idx]

def getObjectIdxByName(object_name):
    object_names = getNames(rt.objects)
    if object_name not in object_names:
        print("[ERROR][control::getObjectIdxByName]")
        print("\t object_name not exist!")
        return None

    object_idx = object_names.index(object_name)
    return object_idx

def getObjectByName(object_name):
    object_idx = getObjectIdxByName(object_name)
    if object_idx is None:
        print("[ERROR][control::getObjectByName]")
        print("\t getObjectIdxByName failed!")
        return None

    obj = getObjectByIdx(object_idx)
    if obj is None:
        print("[ERROR][control::getObjectByName]")
        print("\t getObjectByIdx failed!")
        return None

    return obj

def getObject(object_info):
    if isinstance(object_info, str):
        obj = getObjectByName(object_info)
        if obj is None:
            print("[ERROR][control::getObject]")
            print("\t getObjectByName failed!")
            return None
        return obj

    if isinstance(object_info, int):
        obj = getObjectByIdx(object_info)
        if obj is None:
            print("[ERROR][control::getObject]")
            print("\t getObjectByIdx failed!")
            return None
        return obj

    if isinstance(object_info, pymxs.MXSWrapperBase):
        return object_info

    print("[ERROR][control::getObject]")
    print("\t object_info not valid!")
    return None

