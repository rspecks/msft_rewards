# Main TODOs
# - Set up logging 
# - Add different checks to ensure on right page
# - Organize files with OOP structure 
# - Add documentation (why so late? idk cuz fk documentation)
# - Move to laptop (or any available compatible device)
# -- Setup web server (or API?? Would be a first for me) on laptop
# -- Allow for remote points making \(￣︶￣*\))
# - Attempt luck at other ways to make points

import random
import pyautogui
import time
import pyperclip
import logging
import os
import json

EMPTY = ""
PC_REWARD_CAP = "150"
MOB_REWARD_CAP = "100"
#TODO Enum probs
EDGE = 1
ANDR_STUD = 2 
# ya defo enums
FILE_LOC = 0
NEED_HELP = 1


# failsafes, drag mouse to top left corner of screen to quit app
pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True

def main():

    # JSOOOOOOOOOOOOOOOOOOOOON
    with open("files/pic_data.json") as file:
        pic_data = json.load(file)
    
    #Create and configure logger
    logging.basicConfig(filename="newfile.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    
    #Creating an object
    logger=logging.getLogger()
    
    #Setting the threshold of logger to ERROR
    logger.setLevel(logging.FATAL)

    # get a bunch of words
    word_dir = "files/word_list.txt"
    with open(word_dir, 'r') as fh:
        word_list = fh.readlines()
    this_word = ""
    word_count = 0
    for word in word_list:
        inner_count = 0 
        for letter in str(word):    
            if letter != "\'" and letter != "\\" and (len(word)-1) != inner_count:
                this_word = this_word + str(letter)
            inner_count+=1
        word_list[word_count] = this_word
        this_word = ""
        word_count+=1 

    ################################################
    # Functionality for browser points starts here #
    ################################################

    AppLauncher(EDGE)

    # # waiting on browser (can adjust)
    # time.sleep(2)

    # going to bing.com
    pyautogui.hotkey('ctrl','t')
    pyautogui.typewrite('bing.com')
    pyautogui.typewrite(['enter'])

    # more waiting
    time.sleep(1)

    # vars
    pc_keep_going = True
    pc_count = 0 

    while pc_keep_going:

        LetsGetRandom(word_list)

        pyautogui.typewrite(['f6'])
        pyautogui.typewrite(['f6'])
        pyautogui.typewrite('bing.com')
        pyautogui.typewrite(['enter'])

        pc_count+=1

        if pc_count >= 15:
            
            desired_data = "msft_rewards"
            list_of_data = JsonReader(desired_data, pic_data)
            msft_rewards_location = LookingForLocation(list_of_data[FILE_LOC], list_of_data[NEED_HELP])
            pyautogui.click(msft_rewards_location)
            
            desired_data = "pc_earnings"
            list_of_data = JsonReader(desired_data, pic_data)
            earnings_location = LookingForLocation(list_of_data[FILE_LOC], list_of_data[NEED_HELP])
            pyautogui.doubleClick(earnings_location)
            pyautogui.hotkey('ctrl','c')
            
            rewards_value = pyperclip.paste()
            if rewards_value == PC_REWARD_CAP:
                pc_keep_going = False
                pyautogui.alert(text='Got the loot, onto the next task', title='All Done!')
            else:
                pc_count = 10

    ###############################################
    # Functionality for mobile points starts here #
    ###############################################

    AppLauncher(ANDR_STUD)

    # clicking avd manager
    desired_data = "avd_mgr"
    list_of_data = JsonReader(desired_data, pic_data)
    avd_mgr_location = LookingForLocation(list_of_data[FILE_LOC], list_of_data[NEED_HELP])
    pyautogui.click(avd_mgr_location)
    
    # clicking play on vm
    desired_data = "vm_play"
    list_of_data = JsonReader(desired_data, pic_data)
    as_vm_play_location = LookingForLocation(list_of_data[FILE_LOC], list_of_data[NEED_HELP])
    pyautogui.click(as_vm_play_location)

    # clicking vm power button 
    desired_data = "vm_pwr_bttn"
    list_of_data = JsonReader(desired_data, pic_data)
    as_vm_pwr_bttn_location = LookingForLocation(list_of_data[FILE_LOC], list_of_data[NEED_HELP])
    pyautogui.click(as_vm_pwr_bttn_location)

    # mama im coming hooOOOooomme (clicking home button on vm)
    special_loop = True
    while special_loop:
        desired_data = "vm_home_bttn"
        list_of_data = JsonReader(desired_data, pic_data)
        as_vm_home_bttn_location = LookingForLocation(list_of_data[FILE_LOC], list_of_data[NEED_HELP])
        pyautogui.click(as_vm_home_bttn_location)

        # flagging the problem child, plays loop back
        desired_data = "vm_chrome_app"
        list_of_data = JsonReader(desired_data, pic_data)
        vm_chrome_app_location = LookingForLocation(list_of_data[FILE_LOC], list_of_data[NEED_HELP], special_loop)
        if vm_chrome_app_location != EMPTY:
            pyautogui.click(vm_chrome_app_location)
            special_loop = False

    # clicking mobile search link
    desired_data = "vm_mobile_search_link"
    list_of_data = JsonReader(desired_data, pic_data)
    vm_mobile_search_link_location = LookingForLocation(list_of_data[FILE_LOC], list_of_data[NEED_HELP])
    pyautogui.click(vm_mobile_search_link_location)

    mobile_keep_going = True
    mobile_count = 0 
    while mobile_keep_going:

        # clicking search
        desired_data = "vm_rewards_search"
        list_of_data = JsonReader(desired_data, pic_data)
        vm_rewards_search_location = LookingForLocation(list_of_data[FILE_LOC], list_of_data[NEED_HELP])
        pyautogui.click(vm_rewards_search_location)
        
        # click the x button that appears when you click on search; clears search
        desired_data = "vm_search_x_bttn"
        list_of_data = JsonReader(desired_data, pic_data)
        vm_search_x_bttn_location = LookingForLocation(list_of_data[FILE_LOC], list_of_data[NEED_HELP])
        pyautogui.click(vm_search_x_bttn_location)

        LetsGetRandom(word_list)

        mobile_count +=1 

        if mobile_count >= 10:
            
            AppLauncher(EDGE)
            special_loop = True
            while special_loop:
                desired_data = "msft_rewards"
                list_of_data = JsonReader(desired_data, pic_data)
                msft_rewards_location = LookingForLocation(list_of_data[FILE_LOC], list_of_data[NEED_HELP])
                pyautogui.click(msft_rewards_location)

                # potential problem child
                desired_data = "mobile_earnings"
                list_of_data = JsonReader(desired_data, pic_data)
                mobile_earnings_location = LookingForLocation(list_of_data[FILE_LOC], list_of_data[NEED_HELP], special_loop)
                if mobile_earnings_location != EMPTY:
                    pyautogui.doubleClick(mobile_earnings_location)
                    pyautogui.hotkey('ctrl','c')
                    special_loop = False

            rewards_value = pyperclip.paste()

            if rewards_value == MOB_REWARD_CAP:
                mobile_keep_going = False
                pyautogui.alert(text='Got the loot for the day, goodnight', title='All Done!')
            else:
                mobile_count = 5

#################
#### Modules ####
#################

def AppLauncher(app):

    if app == EDGE:
        os.startfile('"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"')
    elif app == ANDR_STUD:
        os.startfile('"C:/Program Files/Android/Android Studio/bin/studio64.exe"')

def ExceptionHandler(obj, need_help, excption=0):

    flag = False
    try:
        obj_location = pyautogui.center(obj)
        flag = True
    except Exception:
        #TODO figure out logging lol 
        print()
    if excption >= 1:
        time.sleep(5)
    if flag:
        return obj_location
    elif excption >= 2 and not flag:
        pyautogui.alert(text= need_help, title='Looks like im lost, can you help me find.. ')
        return EMPTY
    else:
        return EMPTY

def JsonReader(desired_data, pic_data):
    list_of_data = []
    for data in pic_data:
        if data["Obj_Name"] == desired_data:
            list_of_data.append(data["File_Loc"])
            list_of_data.append(data["Description"])
            return list_of_data



def LetsGetRandom(word_list):
    """Probably going to be under a big ole Pyautogui class"""    
    pyautogui.typewrite(str(word_list[random.randint(0,10000)]))
    pyautogui.typewrite(['enter'])

def LookingForLocation(pic, need_help, special_flag=False):

    looking = True
    excption = 0 
    while looking:
        obj = pyautogui.locateOnScreen(pic, confidence=0.8)
        obj_location = ExceptionHandler(obj, need_help, excption)
        excption+=1
        if obj_location != EMPTY:
            return obj_location
        elif special_flag:
            return EMPTY


        
            






























main()













