#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymxs import runtime as rt

from Method.obj_filter import getObject

def selectObject(object_info, with_history=True):
    obj = getObject(object_info)
    if obj is None:
        print("[ERROR][select::selectObject]")
        print("\t getObject failed!")
        return False

    if with_history:
        rt.select([obj] + rt.selection)
    else:
        rt.select(obj)
    return True

def selectAll():
    rt.select(rt.objects)
    return True

def deSelectObject(object_info):
    obj = getObject(object_info)
    if obj is None:
        print("[ERROR][select::deSelectObject]")
        print("\t getObject failed!")
        return False

    rt.deselect(obj)
    return True

def deSelectAll():
    rt.deselect(rt.objects)
    return True

