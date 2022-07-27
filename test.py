#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

    def execute(self, cmd, update=True):
        rt.execute(cmd)
        if update:
            self.update()
        return True

    def setUserProp(self, obj, prop_name, prop_value, update=True):
        rt.setUserProp(obj, prop_name, prop_value)
        if update:
            self.update()
        return True

    def createBox(self, update=True):
        rt.box()
        if update:
            self.update()
        return True

    def selectObject(self, object_info, with_history=True, update=True):
        obj = self.getObject(object_info)
        if obj is None:
            print("[ERROR][MaxOp::selectObject]")
            print("\t getObject failed!")
            return False

        if with_history:
            rt.select([obj] + self.selection)
        else:
            rt.select(obj)

        if update:
            self.update()
        return True

    def selectAll(self, update=True):
        rt.select(rt.objects)
        if update:
            self.update()
        return True

    def deSelectObject(self, object_info, update=True):
        obj = self.getObject(object_info)
        if obj is None:
            print("[ERROR][MaxOp::deSelectObject]")
            print("\t getObject failed!")
            return False

        rt.deselect(obj)
        if update:
            self.update()
        return True

    def deSelectAll(self, update=True):
        rt.deselect(rt.objects)
        if update:
            self.update()
        return True

    def deleteObject(self, object_info, update=True):
        obj = self.getObject(object_info)
        if obj is None:
            print("[ERROR][MaxOp::deleteObject]")
            print("\t getObject failed!")
            return False

        rt.delete(obj)
        if update:
            self.update()
        return True

    def deleteAll(self, update=True):
        rt.delete(rt.objects)
        if update:
            self.update()
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

def demo():
    max_op = MaxOp()

    #  max_op.createBox()
    max_op.outputInfo()

    max_op.selectObject("Box003")
    max_op.outputInfo()
    max_op.selectObject("Box004")
    max_op.outputInfo()
    max_op.deSelectObject("Box003")
    max_op.outputInfo()
    max_op.deSelectObject("Box004")
    max_op.outputInfo()

    print("========")
    return True

if __name__ == "__main__":
    demo()

