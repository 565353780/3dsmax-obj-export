#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from flask import Flask, request

import sys
sys.path.append("D:/github/3dsmax-obj-export/")

from Config.path import TMP_SAVE_FOLDER_PATH

from Method.signal import sendDataIn, getDataOut

def demo():
    port = 9360

    app = Flask(__name__)

    os.makedirs(TMP_SAVE_FOLDER_PATH, exist_ok=True)

    @app.route('/transMaxToObj', methods=['POST'])
    def transMaxToObj():
        data = request.get_data()
        sendDataIn('transMaxToObj', data)
        result_data = getDataOut('transMaxToObj')
        return json.dumps(result_data, ensure_ascii=False)

    @app.route('/stop', methods=['POST'])
    def stop():
        sendDataIn('stop', b'1')
        result_data = getDataOut('stop')
        return json.dumps(result_data, ensure_ascii=False)

    app.run('0.0.0.0', port)
    return True

if __name__ == "__main__":
    demo()

