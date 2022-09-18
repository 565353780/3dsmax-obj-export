#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from flask import Flask, request

from max_obj_export.Config.path import TMP_SAVE_FOLDER_PATH

from max_obj_export.Method.signal import sendDataIn, getDataOut

def demo():
    port = 9365

    app = Flask(__name__)

    os.makedirs(TMP_SAVE_FOLDER_PATH, exist_ok=True)

    @app.route('/')
    def index():
        return "Hello"

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

