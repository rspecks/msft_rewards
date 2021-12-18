import pyautogui
import time
from classes.computer import Computer

EMPTY = ""
FILE_LOC = 0
NEED_HELP = 1
pyautogui.PAUSE = 0.75
pyautogui.FAILSAFE = True

class ImageHandler():
    def __init__(self, pic_data):
        self.pic_data = pic_data
    
    def exceptionHandler(self, obj, excption):
        
        flag = False
        try:
            obj_location = pyautogui.center(obj)
            flag = True
        except Exception:
            pass
        if excption >= 1:
            time.sleep(2.5)
        if flag:
            return obj_location
        else:
            return EMPTY

    def imgHandler(self,desired_data, default_action=True,special_flag=False, confidence_num=0.8, time_delay=0):
    
        file_loc = self.jsonReader(desired_data)
        excption = 0 
        looking = True
        while looking:
            time.sleep(time_delay)
            obj = pyautogui.locateOnScreen(file_loc, confidence=confidence_num)
            obj_location = self.exceptionHandler(obj, excption)
            excption+=1
            if obj_location != EMPTY:
                if default_action:
                    Computer.click(obj_location)
                else:
                    Computer.doubleClick(obj_location)
                    Computer.copy()

                looking = False
            elif special_flag:
                return EMPTY 

    def jsonReader(self, desired_data):
        list_of_data = []
        for data in self.pic_data:
            if data["Obj_Name"] == desired_data:
                return data["File_Loc"]

    