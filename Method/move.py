#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymxs import runtime as rt

from Method.obj_filter import getObject

def moveObject(object_info, move_vector):
    obj = getObject(object_info)
    if obj is None:
        print("[ERROR][move::moveObject]")
        print("\t getObject failed!")
        return False

    move_point = rt.Point3(move_vector[0],
                           move_vector[1],
                           move_vector[2])
    rt.move(obj, move_point)
    return True

def moveSelection(move_vector):
    move_point = rt.Point3(move_vector[0],
                           move_vector[1],
                           move_vector[2])
    rt.move(rt.selection, move_point)
    return True

def moveAll(move_vector):
    move_point = rt.Point3(move_vector[0],
                           move_vector[1],
                           move_vector[2])
    rt.move(rt.objects, move_point)
    return True

