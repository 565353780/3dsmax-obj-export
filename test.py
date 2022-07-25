#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymxs import runtime as rt

class MaxOp(object):
    def __init__(self):
        self.objects = []
        self.object_names = []
        self.selection = []
        self.selection_names = []
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

    def selectObject(self, obj, update=True):
        rt.select(obj)
        if update:
            self.update()
        return True

    def selectObjectByIdx(self, object_idx, update=True):
        if object_idx >= len(self.objects):
            print("[ERROR][MaxOp::selectObjectByIdx]")
            print("\t object_idx out of range!")
            return False

        self.selectObject(self.objects[object_idx], False)
        if update:
            self.update()
        return True

    def selectObjectByName(self, object_name, update=True):
        if object_name not in self.object_names:
            print("[ERROR][MaxOp::selectObjectByName]")
            print("\t object_name not exist!")
            return False

        object_idx = self.object_names.index(object_name)
        if not self.selectObjectByIdx(object_idx, False):
            print("[ERROR][MaxOp::selectObjectByName]")
            print("\t selectObjectByIdx failed!")
            return False
        if update:
            self.update()
        return True

    def selectAll(self, update=True):
        rt.select(rt.objects)
        if update:
            self.update()
        return True

    def deSelectObject(self, obj, update=True):
        rt.deselect(obj)
        if update:
            self.update()
        return True

    def deSelectObjectByIdx(self, object_idx, update=True):
        if object_idx >= len(self.objects):
            print("[ERROR][MaxOp::deSelectObjectByIdx]")
            print("\t object_idx out of range!")
            return False

        self.deSelectObject(self.objects[object_idx], False)
        if update:
            self.update()
        return True

    def deSelectObjectByName(self, object_name, update=True):
        if object_name not in self.object_names:
            print("[ERROR][MaxOp::selectObjectByName]")
            print("\t object_name not exist!")
            return False

        object_idx = self.object_names.index(object_name)
        if not self.deSelectObjectByIdx(object_idx, False):
            print("[ERROR][MaxOp::deSelectObjectByName]")
            print("\t deSelectObjectByIdx failed!")
            return False
        if update:
            self.update()
        return True

    def deSelectAll(self, update=True):
        rt.deselect(rt.objects)
        if update:
            self.update()
        return True

    def chooseObject(self, update=True):
        if not self.deSelectAll(False):
            print("[ERROR][MaxOp::chooseObject]")
            print("\t deSelectAll failed!")
            return False

        if update:
            self.update()
        return True

    def deleteAll(self, update=True):
        rt.delete(rt.objects)
        self.update()
        return True

    def getNames(self, object_list):
        name_list = []
        for obj in object_list:
            name_list.append(obj.name)
        return name_list

    def getObjects(self):
        return self.objects

    def getSelection(self):
        return self.selection

    def getAllObjectNames(self):
        return self.object_names

    def getSelectionNames(self):
        return self.selection_names

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

    max_op.createBox()
    max_op.outputInfo()
    max_op.selectObjectByName("Box001")
    max_op.outputInfo()
    max_op.deSelectObjectByName("Box001")
    max_op.outputInfo()

    print("========")
    return True

if __name__ == "__main__":
    demo()

