#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Module.max_client import MaxClient

if __name__ == "__main__":
    server_ip = "192.168.2.16"
    server_port = 9365

    #  max_file_path = "C:/Program Files/Autodesk/3ds Max 2023/presets/Particle Flow/earth_Squib Sand01.max"
    max_file_path = "/home/chli/chLi/tmp.max"
    save_obj_file_path = "/home/chli/chLi/test.obj"

    max_client = MaxClient(server_ip, server_port)
    max_client.transMaxToObj(max_file_path, save_obj_file_path)

    #  max_client.stop()

