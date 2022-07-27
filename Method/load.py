#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pymxs import runtime as rt

from Config.max import NO_PROMPT

def loadMaxFile(max_file_path):
    if not os.path.exists(max_file_path):
        print("[ERROR][max::loadMaxFile]")
        print("\t max_file not exist!")
        return False

    rt.loadMaxFile(max_file_path)
    return True

def resetMaxFile():
    rt.resetMaxFile(NO_PROMPT)
    return True

