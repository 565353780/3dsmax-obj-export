#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymxs import runtime as rt

from Method.obj_filter import getNames, getObject

def outputMaxFilePath():
    print("[INFO][output::outputMaxFilePath]")
    print("\t maxFilePath =")
    print(rt.maxFilePath)
    return True

def outputMaxFileName():
    print("[INFO][output::outputMaxFileName]")
    print("\t maxFileName =")
    print(rt.maxFileName)
    return True

def outputNames(names, info_level=0):
    line_start = "\t" * info_level
    if len(names) == 0:
        print(line_start + "[]")
        return True

    print(line_start + "[")

    for i, name in enumerate(names):
        mod = i % 5

        if mod == 0:
            print(line_start + "\t", end="")
        print(name + ", ", end="")
        if mod == 4:
            print()

    if len(names) % 5 != 4:
        print()

    print(line_start + "]")
    return True

def outputObject(object_info, info_level=0):
    obj = getObject(object_info)
    if obj is None:
        print("[WARN][MaxOp::outputObject]")
        print("\t getObject failed!")
        return False

    line_start = "\t" * info_level
    print(line_start + "[Object]")
    print(line_start + "\t name =", obj.name)
    print(line_start + "\t pos =", obj.pos)
    print(line_start + "\t scale =", obj.scale)
    print(line_start + "\t rotation =", obj.rotation)
    return True

def outputInfo(info_level=0):
    line_start = "\t" * info_level
    print(line_start + "[ObjectInfo]")
    print(line_start + "\t object_num =", len(rt.objects))
    print(line_start + "\t object_names =")
    outputNames(getNames(rt.objects), info_level + 2)
    print(line_start + "\t selection_num =", len(rt.selection))
    print(line_start + "\t selection_names =")
    outputNames(getNames(rt.selection), info_level + 2)
    return True

