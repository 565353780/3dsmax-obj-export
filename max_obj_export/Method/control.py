#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymxs import runtime as rt

from max_obj_export.Method.obj_filter import getObject

def execute(cmd):
    rt.execute(cmd)
    return True

def setUserProp(obj_info, prop_name, prop_value):
    obj = getObject(obj_info)
    if obj is None:
        print("[ERROR][control::setUserProp]")
        print("\t getObject failed!")
        return False

    rt.setUserProp(obj, prop_name, prop_value)
    return True

def getPolygonCount(obj):
    return rt.getPolygonCount(obj)

def createBox():
    rt.box()
    return True

