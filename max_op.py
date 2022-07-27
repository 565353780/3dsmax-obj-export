#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scipy.spatial.transform import Rotation as R

import pymxs
from pymxs import runtime as rt

class MaxOp(object):
    def __init__(self):
        self.objects = []
        self.object_names = []
        self.selection = []
        self.selection_names = []

        self.update()
        return

    def update(self):
        self.objects = rt.objects
        self.object_names = self.getNames(self.objects)
        self.selection = rt.selection
        self.selection_names = self.getNames(self.selection)
        return True

    def execute(self, cmd):
        rt.execute(cmd)
        self.update()
        return True

    def setUserProp(self, obj, prop_name, prop_value):
        rt.setUserProp(obj, prop_name, prop_value)
        self.update()
        return True

    def createBox(self):
        rt.box()
        self.update()
        return True

    def selectObject(self, object_info, with_history=True):
        obj = self.getObject(object_info)
        if obj is None:
            print("[ERROR][MaxOp::selectObject]")
            print("\t getObject failed!")
            return False

        if with_history:
            rt.select([obj] + self.selection)
        else:
            rt.select(obj)

        self.update()
        return True

    def selectAll(self):
        rt.select(self.objects)
        self.update()
        return True

    def deSelectObject(self, object_info):
        obj = self.getObject(object_info)
        if obj is None:
            print("[ERROR][MaxOp::deSelectObject]")
            print("\t getObject failed!")
            return False

        rt.deselect(obj)
        self.update()
        return True

    def deSelectAll(self):
        rt.deselect(self.objects)
        self.update()
        return True

    def deleteObject(self, object_info):
        obj = self.getObject(object_info)
        if obj is None:
            print("[ERROR][MaxOp::deleteObject]")
            print("\t getObject failed!")
            return False

        rt.delete(obj)
        self.update()
        return True

    def deleteSelection(self):
        rt.delete(self.selection)
        self.update()
        return True

    def deleteAll(self):
        rt.delete(self.objects)
        self.update()
        return True

    def moveObject(self, object_info, move_vector):
        obj = self.getObject(object_info)
        if obj is None:
            print("[ERROR][MaxOp::moveObject]")
            print("\t getObject failed!")
            return False

        move_point = rt.Point3(move_vector[0],
                               move_vector[1],
                               move_vector[2])
        rt.move(obj, move_point)
        return True

    def moveSelection(self, move_vector):
        move_point = rt.Point3(move_vector[0],
                               move_vector[1],
                               move_vector[2])
        rt.move(self.selection, move_point)
        return True

    def moveAll(self, move_vector):
        move_point = rt.Point3(move_vector[0],
                               move_vector[1],
                               move_vector[2])
        rt.move(self.objects, move_point)
        return True

    def setObjectPos(self, object_info, pos_vector):
        obj = self.getObject(object_info)
        if obj is None:
            print("[ERROR][MaxOp::setObjectPos]")
            print("\t getObject failed!")
            return False

        pos_point = rt.Point3(pos_vector[0],
                              pos_vector[1],
                              pos_vector[2])
        obj.pos = pos_point
        return True

    def setObjectScale(self, object_info, scale_vector):
        obj = self.getObject(object_info)
        if obj is None:
            print("[ERROR][MaxOp::setObjectScale]")
            print("\t getObject failed!")
            return False

        scale_point = rt.Point3(scale_vector[0],
                                scale_vector[1],
                                scale_vector[2])
        obj.scale = scale_point
        return True

    def setObjectRotation(self, object_info, rotation_vector):
        obj = self.getObject(object_info)
        if obj is None:
            print("[ERROR][MaxOp::setObjectRotation]")
            print("\t getObject failed!")
            return False

        quat = R.from_euler('zxy', rotation_vector, degrees=True).as_quat()
        rotation_quat = rt.Quat(float(quat[0]),
                                float(quat[1]),
                                float(quat[2]),
                                float(quat[3]))
        obj.rotation = rotation_quat
        return True

    def getObjectByIdx(self, object_idx):
        if object_idx >= len(self.objects):
            print("[ERROR][MaxOp::getObjectByIdx]")
            print("\t object_idx out of range!")
            return None
        return self.objects[object_idx]

    def getObjectIdxByName(self, object_name):
        if object_name not in self.object_names:
            print("[ERROR][MaxOp::getObjectIdxByName]")
            print("\t object_name not exist!")
            return None

        object_idx = self.object_names.index(object_name)
        return object_idx

    def getObjectByName(self, object_name):
        object_idx = self.getObjectIdxByName(object_name)
        if object_idx is None:
            print("[ERROR][MaxOp::getObjectByName]")
            print("\t getObjectIdxByName failed!")
            return None

        obj = self.getObjectByIdx(object_idx)
        if obj is None:
            print("[ERROR][MaxOp::getObjectByName]")
            print("\t getObjectByIdx failed!")
            return None

        return obj

    def getObject(self, object_info):
        if isinstance(object_info, str):
            obj = self.getObjectByName(object_info)
            if obj is None:
                print("[ERROR][MaxOp::getObject]")
                print("\t getObjectByName failed!")
                return None
            return obj

        if isinstance(object_info, int):
            obj = self.getObjectByIdx(object_info)
            if obj is None:
                print("[ERROR][MaxOp::getObject]")
                print("\t getObjectByIdx failed!")
                return None
            return obj

        if isinstance(object_info, pymxs.MXSWrapperBase):
            return object_info

        print("[ERROR][MaxOp::getObject]")
        print("\t object_info not valid!")
        return None

    def getNames(self, object_list):
        name_list = []
        for obj in object_list:
            name_list.append(obj.name)
        return name_list

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
        obj = self.getObject(object_info)
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
        print(line_start + "\t object_num =", len(self.objects))
        print(line_start + "\t object_names =")
        self.outputNames(self.object_names, info_level + 2)
        print(line_start + "\t selection_num =", len(self.selection))
        print(line_start + "\t selection_names =")
        self.outputNames(self.selection_names, info_level + 2)
        return True

    def test(self):
        self.deleteAll()
        if len(self.object_names) != 0:
            print("[ERROR][MaxOp::test]")
            print("\t deleteAll failed!")
            return False

        self.createBox()
        if self.object_names != ["Box001"]:
            print("[ERROR][MaxOp::test]")
            print("\t createBox for Box001 failed!")
            return False

        self.createBox()
        if self.object_names != ["Box001", "Box002"]:
            print("[ERROR][MaxOp::test]")
            print("\t createBox for Box002 failed!")
            return False

        self.selectObject("Box001")
        if self.selection_names != ["Box001"]:
            print("[ERROR][MaxOp::test]")
            print("\t selectObject for Box001 failed!")
            return False

        self.selectObject("Box002")
        if self.selection_names != ["Box002", "Box001"]:
            print("[ERROR][MaxOp::test]")
            print("\t selectObject for Box002 failed!")
            return False

        self.deSelectObject("Box001")
        if self.selection_names != ["Box002"]:
            print("[ERROR][MaxOp::test]")
            print("\t deSelectObject for Box001 failed!")
            return False

        self.deSelectObject("Box002")
        if len(self.selection_names) != 0:
            print("[ERROR][MaxOp::test]")
            print("\t deSelectObject for Box002 failed!")
            return False

        self.moveObject("Box001", [1, 1, 1])
        obj = self.getObject("Box001")
        if obj is None:
            print("[ERROR][MaxOp::test]")
            print("\t getObject for move failed!")
            return False
        if obj.pos != rt.Point3(1, 1, 1):
            print("[ERROR][MaxOp::test]")
            print("\t moveObject for Box001 failed!")
            return False

        self.setObjectPos("Box001", [2, 2, 2])
        obj = self.getObject("Box001")
        if obj is None:
            print("[ERROR][MaxOp::test]")
            print("\t getObject for set pos failed!")
            return False
        if obj.pos != rt.Point3(2, 2, 2):
            print("[ERROR][MaxOp::test]")
            print("\t setObjectPos for Box001 failed!")
            return False

        self.setObjectPos("Box001", [0, 0, 0])

        self.setObjectScale("Box001", [2, 3, 1])
        obj = self.getObject("Box001")
        if obj is None:
            print("[ERROR][MaxOp::test]")
            print("\t getObject for set scale failed!")
            return False
        if obj.scale != rt.Point3(2, 3, 1):
            print("[ERROR][MaxOp::test]")
            print("\t setObjectScale for Box001 failed!")
            return False

        self.setObjectRotation("Box001", [90, 0, 0])
        obj = self.getObject("Box001")
        if obj is None:
            print("[ERROR][MaxOp::test]")
            print("\t getObject for set rotation failed!")
            return False
        quat = R.from_euler('zxy', [90, 0, 0], degrees=True).as_quat()
        if obj.rotation != rt.Quat(float(quat[0]),
                                   float(quat[1]),
                                   float(quat[2]),
                                   float(quat[3])):
            print("[ERROR][MaxOp::test]")
            print("\t setObjectRotation for Box001 failed!")
            return False

        self.deleteAll()
        if len(self.object_names) != 0:
            print("[ERROR][MaxOp::test]")
            print("\t deleteAll failed!")
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

