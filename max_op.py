#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymxs import runtime as rt

import sys
sys.path.append("D:/github/3dsmax-obj-export/")

from Method.obj_filter import getNames, getObject
from Method.select import selectObject, deSelectObject
from Method.control import createBox
from Method.delete import deleteAll
from Method.move import moveObject
from Method.pose import getQuatFromAngle, setObjectPos, setObjectScale, setObjectRotation

class MaxOp(object):
    def __init__(self):
        return

    def getPolygonCount(self, obj):
        return rt.getPolygonCount(obj)

    def outputNames(self, names, info_level=0):
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

    def outputObject(self, object_info, info_level=0):
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

    def outputInfo(self, info_level=0):
        line_start = "\t" * info_level
        print(line_start + "[ObjectInfo]")
        print(line_start + "\t object_num =", len(rt.objects))
        print(line_start + "\t object_names =")
        self.outputNames(getNames(rt.objects), info_level + 2)
        print(line_start + "\t selection_num =", len(rt.selection))
        print(line_start + "\t selection_names =")
        self.outputNames(getNames(rt.selection), info_level + 2)
        return True

    def test(self):
        print("[INFO][MaxOp::test]")
        print("\t test start...")

        deleteAll()
        object_names = getNames(rt.objects)
        if len(object_names) != 0:
            print("[ERROR][MaxOp::test]")
            print("\t deleteAll for first time failed!")
            return False

        createBox()
        object_names = getNames(rt.objects)
        if object_names != ["Box001"]:
            print("[ERROR][MaxOp::test]")
            print("\t createBox for Box001 failed!")
            return False

        createBox()
        object_names = getNames(rt.objects)
        if object_names != ["Box001", "Box002"]:
            print("[ERROR][MaxOp::test]")
            print("\t createBox for Box002 failed!")
            return False

        selectObject("Box001")
        selection_names = getNames(rt.selection)
        if selection_names != ["Box001"]:
            print("[ERROR][MaxOp::test]")
            print("\t selectObject for Box001 failed!")
            return False

        selectObject("Box002")
        selection_names = getNames(rt.selection)
        if selection_names != ["Box002", "Box001"]:
            print("[ERROR][MaxOp::test]")
            print("\t selectObject for Box002 failed!")
            return False

        deSelectObject("Box001")
        selection_names = getNames(rt.selection)
        if selection_names != ["Box002"]:
            print("[ERROR][MaxOp::test]")
            print("\t deSelectObject for Box001 failed!")
            return False

        deSelectObject("Box002")
        selection_names = getNames(rt.selection)
        if len(selection_names) != 0:
            print("[ERROR][MaxOp::test]")
            print("\t deSelectObject for Box002 failed!")
            return False

        moveObject("Box001", [1, 1, 1])
        obj = getObject("Box001")
        if obj is None:
            print("[ERROR][MaxOp::test]")
            print("\t getObject for move failed!")
            return False
        if obj.pos != rt.Point3(1, 1, 1):
            print("[ERROR][MaxOp::test]")
            print("\t moveObject for Box001 failed!")
            return False

        setObjectPos("Box001", [2, 2, 2])
        obj = getObject("Box001")
        if obj is None:
            print("[ERROR][MaxOp::test]")
            print("\t getObject for set pos failed!")
            return False
        if obj.pos != rt.Point3(2, 2, 2):
            print("[ERROR][MaxOp::test]")
            print("\t setObjectPos for Box001 failed!")
            return False

        setObjectPos("Box001", [0, 0, 0])

        setObjectScale("Box001", [2, 3, 1])
        obj = getObject("Box001")
        if obj is None:
            print("[ERROR][MaxOp::test]")
            print("\t getObject for set scale failed!")
            return False
        if obj.scale != rt.Point3(2, 3, 1):
            print("[ERROR][MaxOp::test]")
            print("\t setObjectScale for Box001 failed!")
            return False

        setObjectRotation("Box001", [90, 0, 0])
        obj = getObject("Box001")
        if obj is None:
            print("[ERROR][MaxOp::test]")
            print("\t getObject for set rotation failed!")
            return False
        if obj.rotation != getQuatFromAngle([90, 0, 0]):
            print("[ERROR][MaxOp::test]")
            print("\t setObjectRotation for Box001 failed!")
            return False

        deleteAll()
        object_names = getNames(rt.objects)
        if len(object_names) != 0:
            print("[ERROR][MaxOp::test]")
            print("\t deleteAll for last time failed!")
            return False

        print("[INFO][MaxOp::test]")
        print("\t all test running succees!")
        return True

def demo():
    max_op = MaxOp()
    max_op.test()
    return True

if __name__ == "__main__":
    demo()

