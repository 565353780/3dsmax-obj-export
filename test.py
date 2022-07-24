import os
import flask
from pymxs import runtime as rt

def createFileFolder(file_path):
    file_name = file_path.split("/")[-1]
    file_folder_path = file_path.split(file_name)[0]
    os.makedirs(file_folder_path)
    return True

class MaxObjExp(object):
    def __init__(self):
        self.all = rt.Name('all')
        self.no_prompt = rt.Name('noPrompt')
        return

    def loadMaxFile(self, max_file_path):
        if not os.path.exists(max_file_path):
            print("[ERROR][MaxObjExp::loadMaxFile]")
            print("\t max_file not exist!")
            return False

        rt.loadMaxFile(max_file_path)
        return True

    def resetMaxFile(self):
        rt.resetMaxFile(self.no_prompt)
        return True

    def exportObj(self, save_file_path, selectedOnly=False):
        rt.exportFile(save_file_path, self.no_prompt,
                      selectedOnly=selectedOnly,
                      using=rt.ObjExp)
        return True

    def exportObjOneByOne(self, save_folder_path):
        if save_folder_path[-1] != "/":
            save_folder_path += "/"

        rt.select(self.all)
        select_obj = rt.selection
        for i in range(len(select_obj)):
            rt.select(select_obj[i])
            save_file_path = save_folder_path + str(i) + ".obj"
            self.exportObj(save_file_path, True)
        return True

    def exportAllObj(self, save_file_path):
        rt.select(self.all)
        self.exportObj(save_file_path, True)
        return True

    def transToObj(self, max_file_path, save_obj_file_path):
        if not self.loadMaxFile(max_file_path):
            print("[ERROR][MaxObjExp::transToObj]")
            print("\t loadMaxFile failed!")
            return False

        if not self.exportObj(save_obj_file_path):
            print("[ERROR][MaxObjExp::transToObj]")
            print("\t exportObj failed!")
            return False

        if not self.resetMaxFile():
            print("[ERROR][MaxObjExp::transToObj]")
            print("\t resetMaxFile failed!")
            return False
        return True

    def outputMaxFilePath(self):
        print("[INFO][MaxObjExp::outputMaxFilePath]")
        print("\t maxFilePath =")
        print(rt.maxFilePath)
        return True

    def outputMaxFileName(self):
        print("[INFO][MaxObjExp::outputMaxFileName]")
        print("\t maxFileName =")
        print(rt.maxFileName)
        return True

def demo():
    max_file_path = "C:/Program Files/Autodesk/3ds Max 2023/presets/Particle Flow/earth_Squib Sand01.max"
    save_obj_file_path = "D:/test.obj"

    max_obj_exp = MaxObjExp()
    max_obj_exp.transToObj(max_file_path, save_obj_file_path)
    return True

if __name__ == "__main__":
    demo()

