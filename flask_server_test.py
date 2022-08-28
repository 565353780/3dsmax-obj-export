#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask

import sys
sys.path.append("D:/github/method-manage/")

from method_manage.Config.path import TMP_SAVE_FOLDER_PATH

def demo():
    port = 9365

    app = Flask(__name__)

    os.makedirs(TMP_SAVE_FOLDER_PATH, exist_ok=True)

    @app.route('/')
    def index():
        return "Hello"

    @app.route('/transMaxToObj', methods=['POST'])
    def transMaxToObj():
        print("in transMaxToObj!")
        return "transMaxToObj"

    @app.route('/stop', methods=['POST'])
    def stop():
        print("in stop!")
        return "stop"

    app.run('0.0.0.0', port)
    return True

if __name__ == "__main__":
    demo()

