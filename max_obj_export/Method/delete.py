#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymxs import runtime as rt

from max_obj_export.Method.obj_filter import getObject

def deleteObject(object_info):
    obj = getObject(object_info)
    if obj is None:
        print("[ERROR][delete::deleteObject]")
        print("\t getObject failed!")
        return False

    rt.delete(obj)
    return True

def deleteSelection():
    rt.delete(rt.selection)
    return True

def deleteAll():
    rt.delete(rt.objects)
    return True

