#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymxs import runtime as rt

from max_obj_export.Method.obj_filter import getNames, getObject
from max_obj_export.Method.select import selectObject, deSelectObject
from max_obj_export.Method.control import createBox
from max_obj_export.Method.delete import deleteAll
from max_obj_export.Method.move import moveObject
from max_obj_export.Method.pose import getQuatFromAngle, setObjectPos, setObjectScale, setObjectRotation

def test():
    print("[INFO][test::test]")
    print("\t test start...")

    deleteAll()
    object_names = getNames(rt.objects)
    if len(object_names) != 0:
        print("[ERROR][test::test]")
        print("\t deleteAll for first time failed!")
        return False

    createBox()
    object_names = getNames(rt.objects)
    if object_names != ["Box001"]:
        print("[ERROR][test::test]")
        print("\t createBox for Box001 failed!")
        return False

    createBox()
    object_names = getNames(rt.objects)
    if object_names != ["Box001", "Box002"]:
        print("[ERROR][test::test]")
        print("\t createBox for Box002 failed!")
        return False

    selectObject("Box001")
    selection_names = getNames(rt.selection)
    if selection_names != ["Box001"]:
        print("[ERROR][test::test]")
        print("\t selectObject for Box001 failed!")
        return False

    selectObject("Box002")
    selection_names = getNames(rt.selection)
    if selection_names != ["Box002", "Box001"]:
        print("[ERROR][test::test]")
        print("\t selectObject for Box002 failed!")
        return False

    deSelectObject("Box001")
    selection_names = getNames(rt.selection)
    if selection_names != ["Box002"]:
        print("[ERROR][test::test]")
        print("\t deSelectObject for Box001 failed!")
        return False

    deSelectObject("Box002")
    selection_names = getNames(rt.selection)
    if len(selection_names) != 0:
        print("[ERROR][test::test]")
        print("\t deSelectObject for Box002 failed!")
        return False

    moveObject("Box001", [1, 1, 1])
    obj = getObject("Box001")
    if obj is None:
        print("[ERROR][test::test]")
        print("\t getObject for move failed!")
        return False
    if obj.pos != rt.Point3(1, 1, 1):
        print("[ERROR][test::test]")
        print("\t moveObject for Box001 failed!")
        return False

    setObjectPos("Box001", [2, 2, 2])
    obj = getObject("Box001")
    if obj is None:
        print("[ERROR][test::test]")
        print("\t getObject for set pos failed!")
        return False
    if obj.pos != rt.Point3(2, 2, 2):
        print("[ERROR][test::test]")
        print("\t setObjectPos for Box001 failed!")
        return False

    setObjectPos("Box001", [0, 0, 0])

    setObjectScale("Box001", [2, 3, 1])
    obj = getObject("Box001")
    if obj is None:
        print("[ERROR][test::test]")
        print("\t getObject for set scale failed!")
        return False
    if obj.scale != rt.Point3(2, 3, 1):
        print("[ERROR][test::test]")
        print("\t setObjectScale for Box001 failed!")
        return False

    setObjectRotation("Box001", [90, 0, 0])
    obj = getObject("Box001")
    if obj is None:
        print("[ERROR][test::test]")
        print("\t getObject for set rotation failed!")
        return False
    if obj.rotation != getQuatFromAngle([90, 0, 0]):
        print("[ERROR][test::test]")
        print("\t setObjectRotation for Box001 failed!")
        return False

    deleteAll()
    object_names = getNames(rt.objects)
    if len(object_names) != 0:
        print("[ERROR][test::test]")
        print("\t deleteAll for last time failed!")
        return False

    print("[INFO][test::test]")
    print("\t all test running succees!")
    return True

