#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scipy.spatial.transform import Rotation as R
from pymxs import runtime as rt

from Method.obj_filter import getObject

def getQuatFromAngle(angle_list, axis='zxy'):
    quat = R.from_euler(axis, angle_list, degrees=True).as_quat()
    rotation_quat = rt.Quat(float(quat[0]),
                            float(quat[1]),
                            float(quat[2]),
                            float(quat[3]))
    return rotation_quat

def setObjectPos(object_info, pos_vector):
    obj = getObject(object_info)
    if obj is None:
        print("[ERROR][pose::setObjectPos]")
        print("\t getObject failed!")
        return False

    pos_point = rt.Point3(pos_vector[0],
                          pos_vector[1],
                          pos_vector[2])
    obj.pos = pos_point
    return True

def setObjectScale(object_info, scale_vector):
    obj = getObject(object_info)
    if obj is None:
        print("[ERROR][pose::setObjectScale]")
        print("\t getObject failed!")
        return False

    scale_point = rt.Point3(scale_vector[0],
                            scale_vector[1],
                            scale_vector[2])
    obj.scale = scale_point
    return True

def setObjectRotation(object_info, rotation_vector):
    obj = getObject(object_info)
    if obj is None:
        print("[ERROR][pose::setObjectRotation]")
        print("\t getObject failed!")
        return False

    rotation_quat = getQuatFromAngle(rotation_vector)
    obj.rotation = rotation_quat
    return True

