# Main TODOs
# - Make it work consistently lmao 
# - Add documentation 
# - Organize files with OOP structure 
# - Move to laptop (or any available compatible device)
# -- Setup web server (or API?? Would be a first for me) on laptop
# -- Allow for remote points making \(￣︶￣*\))
# - Attempt look at other ways to make points

import random
from typing import _SpecialForm
import pyautogui
import time
import pyperclip
import logging
import os
import json
import psutil
import signal

EMPTY = ""
PC_REWARD_CAP = "150"
MOB_REWARD_CAP = "100"
# How confident are you bruv?
VERY_CONFIDENT = 0.9
CONFIDENT = 0.8
SLIGHTLY_CONFIDENT = 0.7
SLIGHTLY_NOT_CONFIDENT = 0.6
NOT_CONFIDENT = 0.5
#TODO Enum probs
EDGE = 1
ANDR_STUD = 2 
# ya defo enums
FILE_LOC = 0
NEED_HELP = 1

# Debugging purposes only
DEBUG_MODE = False

# failsafes, drag mouse to top left corner of screen to quit app
pyautogui.PAUSE = 0.75
pyautogui.FAILSAFE = True

log_file = "biglog.log"
#Create and configure logger
logging.basicConfig(filename=log_file,
                    format='%(asctime)s %(message)s',
                    filemode='a')

# #Creating an object
# logger=logging.getLogger()

# #Setting the threshold of logger to ERROR
# logger.setLevel(logging.DEBUG)

# my main man
def main():

    # JSOOOOOOOOOOOOOOOOOOOOON
    with open("files/pic_data.json") as file:
        pic_data = json.load(file)

    # idk I made a dict of all the shit I needed, we'll see if it's needed lmao
    desired_data = {}
    for data in pic_data:
        desired_data.update({data["Order_Used"]:data["Obj_Name"]})
    # used to keep track of which pic to use in process from desired_data 
    pic_order = 0

    # get a bunch of words
    #TODO this list has some strange words, searches can vary, might clean that up lawl 
    word_dir = "files/word_list.txt"
    with open(word_dir, 'r') as fh:
        word_list = fh.readlines()
    this_word = ""
    word_count = 0
    for word in word_list:
        inner_count = 0 
        for letter in str(word):    
            #TODO which one is doing the thing lmao
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
    if not DEBUG_MODE:
        ClickMsftRewards(desired_data, pic_data)

    if not DEBUG_MODE:
        # going to bing.com
        pyautogui.hotkey('ctrl','t')
        pyautogui.typewrite('bing.com')
        pyautogui.typewrite(['enter'])
        pc_count = 1 
    else:
        pc_count = 30
    
    pc_keep_going = True
    while pc_keep_going:

        if not DEBUG_MODE:         
            LetsGetRandom(word_list)

            pyautogui.typewrite(['f6'])
            pyautogui.typewrite(['f6'])
            pyautogui.typewrite('bing.com')
            pyautogui.typewrite(['enter'])

        pc_count+=1

        if pc_count >= 30:
            
            
            #TODO better way to do this would be w/ "requests" lib and for security maybe "secrets", idek
            special_loop = True
            while special_loop:

                ClickMsftRewards(desired_data, pic_data)
        
                earnings_location = LookingForLocation(desired_data["1"], pic_data, special_loop, CONFIDENT, 1)
                if earnings_location != EMPTY:
                    pyautogui.doubleClick(earnings_location)
                    pyautogui.hotkey('ctrl','c')
                    special_loop = False

            
            if not DEBUG_MODE:
                rewards_value = pyperclip.paste()
                if rewards_value == PC_REWARD_CAP:
                    pc_keep_going = False
                    pyautogui.hotkey('alt','f4')
                # pyautogui.alert(text='Got the loot, onto the next task', title='All Done!')
                else:
                    pc_count = 25
            else:
                pyautogui.hotkey('alt','f4')
                pc_keep_going = False

    ###############################################
    # Functionality for mobile points starts here #
    ###############################################

    AppLauncher(ANDR_STUD)

    # clicking avd manager
    avd_mgr_location = LookingForLocation(desired_data["2"], pic_data)
    pyautogui.click(avd_mgr_location)
      
    
    # clicking play on vm
    as_vm_play_location = LookingForLocation(desired_data["3"], pic_data)
    pyautogui.click(as_vm_play_location)
      

    # clicking vm power button 
    as_vm_pwr_bttn_location = LookingForLocation(desired_data["4"], pic_data)
    pyautogui.click(as_vm_pwr_bttn_location)
      

    #TODO does this stop the "UI stop responsing" msg popup?
    time.sleep(1.5)

    # mama im coming hooOOOooomme (clicking home button on vm)
    special_loop = True
    while special_loop:
        as_vm_home_bttn_location = LookingForLocation(desired_data["5"], pic_data)
        pyautogui.click(as_vm_home_bttn_location)
          

        # flagging the problem child, plays loop back
        vm_chrome_app_location = LookingForLocation(desired_data["6"], pic_data)
        if vm_chrome_app_location != EMPTY:
            pyautogui.click(vm_chrome_app_location)
              
            special_loop = False
        else:
            pic_order-=1 

    #TODO just open a new tab and go to fking msft's site directly, dont give up, keep testing :,) 
    #UPDATE^: the file "potential_additon.py" has code that does that, just gotta implement 
    lets_not_be_too_hasty = True
    while lets_not_be_too_hasty:
        
        vm_mobile_search_link_location = LookingForLocation(desired_data["7"], pic_data, lets_not_be_too_hasty, NOT_CONFIDENT)
        if vm_mobile_search_link_location != EMPTY:
            pyautogui.click(vm_mobile_search_link_location)
        did_ui_msg_load = LookingForLocation(desired_data["8"], pic_data, lets_not_be_too_hasty)
        if did_ui_msg_load != EMPTY:
            pyautogui.click(did_ui_msg_load)
        did_search_load = LookingForLocation(desired_data["9"], pic_data, lets_not_be_too_hasty, NOT_CONFIDENT)
        if did_search_load != EMPTY:
            lets_not_be_too_hasty = False



    mobile_keep_going = True
    mobile_count = 0 
    while mobile_keep_going:

        #TODO sometimes a system ui pops up after clicking the mobile search link
        # ^doesnt happen everytime so wouldnt have the program freak out if it cant find it 
        # pic saved under pics/vm_systemui_msg
        # clicking search
        special_loop = True
        while special_loop: 
            time.sleep(.5)
            pyautogui.moveTo(100,100)
            vm_rewards_search_location = LookingForLocation(desired_data["9"], pic_data, special_loop)
            if vm_rewards_search_location != EMPTY:
                pyautogui.click(vm_rewards_search_location)
            pyautogui.moveTo(100,100)
            
            # click the x button that appears when you click on search; clears search
            vm_search_x_bttn_location = LookingForLocation(desired_data["10"], pic_data, special_loop)
            if vm_search_x_bttn_location != EMPTY:
                pyautogui.click(vm_search_x_bttn_location)
                special_loop = False

        #TODO does this stop VM from crashing lmao this is new 
        time.sleep(.5)
        LetsGetRandom(word_list)

        mobile_count +=1 
        if DEBUG_MODE:
            mobile_count = 20
        if mobile_count >= 20:
            
            AppLauncher(EDGE)
            special_loop = True
            while special_loop:

                ClickMsftRewards(desired_data, pic_data)

                mobile_earnings_location = LookingForLocation(desired_data["11"], pic_data, special_loop)
                if mobile_earnings_location != EMPTY:
                    pyautogui.doubleClick(mobile_earnings_location)
                    pyautogui.hotkey('ctrl','c')
                    special_loop = False

            rewards_value = pyperclip.paste()
            if rewards_value == MOB_REWARD_CAP:
                mobile_keep_going = False
                pyautogui.hotkey('alt','f4')
            else:
                pyautogui.hotkey('alt','f4')

                mobile_count = 15
    
    # cleanup crew
    vm_chrome_tab_switcher_location = LookingForLocation(desired_data["17"], pic_data)
    pyautogui.click(vm_chrome_tab_switcher_location)

    vm_tab_x_bttn_location = LookingForLocation(desired_data["18"], pic_data)
    pyautogui.click(vm_tab_x_bttn_location)

    as_vm_back_bttn_location = LookingForLocation(desired_data["19"], pic_data)
    pyautogui.click(as_vm_back_bttn_location)

    vm_mobile_search_link_location = LookingForLocation(desired_data["7"], pic_data, True)
    if vm_mobile_search_link_location == EMPTY:

        vm_chrome_home_bttn_location = LookingForLocation(desired_data["20"], pic_data)
        pyautogui.click(vm_chrome_home_bttn_location)

        vm_chrome_home_search_location = LookingForLocation(desired_data["21"], pic_data)
        pyautogui.click(vm_chrome_home_search_location)

        pyautogui.typewrite("rewards.microsoft")
        time.sleep(.25)
        pyautogui.typewrite(".com/points")
        pyautogui.typewrite("breakdown")
        time.sleep(.5)
        pyautogui.typewrite(['enter'])

    as_vm_pwr_bttn_location = LookingForLocation(desired_data["4"], pic_data)
    pyautogui.click(as_vm_pwr_bttn_location)

    pyautogui.hotkey('alt','f4')

    process_name = "studio64"
    pid = None

    for proc in psutil.process_iter():
        if process_name in proc.name():
            pid = proc.pid
    sig= signal.SIGTERM
    os.kill(pid, sig)

    # Start of daily points clicker
    # mini games research
    # ideally would like to have all their major games booked and studied so bot can squeeze out a few more pts
    
    AppLauncher(EDGE)

    time_delay = 1
    for x in range(3):

        ClickMsftRewards(desired_data, pic_data)

        pts10_extra_activity_location = LookingForLocation(desired_data["12"], pic_data, True, SLIGHTLY_CONFIDENT, time_delay)
        if pts10_extra_activity_location != EMPTY:
            pyautogui.click(pts10_extra_activity_location)
            pyautogui.hotkey('ctrl','f4')
            msft_rewards_location = LookingForLocation(desired_data["0"], pic_data)
            pyautogui.click(msft_rewards_location)
        
        pts5_extra_activity_location = LookingForLocation(desired_data["13"], pic_data, True, SLIGHTLY_CONFIDENT, time_delay)
        if pts5_extra_activity_location != EMPTY:
            pyautogui.click(pts5_extra_activity_location)
            pyautogui.hotkey('ctrl','f4')
        
    for x in range(3):

        special_loop = True
        while special_loop:

            ClickMsftRewards(desired_data, pic_data)

            more_activities_location = LookingForLocation(desired_data["14"], pic_data, special_loop)
            if more_activities_location != EMPTY:
                pyautogui.click(more_activities_location)
                special_loop = False

        
        pts10_extra_activity_location = LookingForLocation(desired_data["12"], pic_data, True, SLIGHTLY_CONFIDENT, time_delay)
        if pts10_extra_activity_location != EMPTY:
            pyautogui.click(pts10_extra_activity_location)
            pyautogui.hotkey('ctrl','f4')  

        pts5_extra_activity_location = LookingForLocation(desired_data["13"], pic_data, True, SLIGHTLY_CONFIDENT, time_delay)
        if pts5_extra_activity_location != EMPTY:
            pyautogui.click(pts5_extra_activity_location)
            pyautogui.hotkey('ctrl','f4')  
    
    special_loop = True
    while special_loop:
    
        msft_rewards_location = LookingForLocation(desired_data["0"], pic_data)
        pyautogui.click(msft_rewards_location)

        daily_poll_location = LookingForLocation(desired_data["15"], pic_data, True, SLIGHTLY_CONFIDENT, time_delay)
        if daily_poll_location != EMPTY:
            pyautogui.click(daily_poll_location)
            daily_poll_option_location = LookingForLocation(desired_data["16"], pic_data, False, SLIGHTLY_CONFIDENT)
            pyautogui.click(daily_poll_option_location)
            special_loop = False


#################
#### Modules ####
#################

def AppLauncher(app):
    app_running = False
    while not app_running:
        if app == EDGE:
            try:
                os.startfile('"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"') 
                app_running = ProcessCheck("msedge")         
            except Exception:
                logging.error("This dood ran this as a standard user, oof")

        elif app == ANDR_STUD:
            try:
                os.startfile('"C:/Program Files/Android/Android Studio/bin/studio64.exe"')
                app_running = ProcessCheck("studio64")
            except Exception:
                logging.error("This dood ran this as a standard user, oof")

def ClickMsftRewards(desired_data, pic_data):
    # not sure, just do this a lot, refactoring will be something
    msft_rewards_location = LookingForLocation(desired_data["0"], pic_data)
    pyautogui.click(msft_rewards_location)
   

def ExceptionHandler(obj, need_help, excption):

    flag = False
    try:
        obj_location = pyautogui.center(obj)
        flag = True
    except Exception:
        logging.error("Error finding " + need_help)
    if excption >= 1:
        time.sleep(2.5)
    if flag:
        return obj_location
    elif excption == 4:
        logging.error(need_help + " taking too long")
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
    time.sleep(.5)
    pyautogui.typewrite(['enter'])

def LookingForLocation(desired_data, pic_data, special_flag=False, confidence_num=0.8, time_delay=0):
    
    list_of_data = JsonReader(desired_data, pic_data)

    excption = 0 
    looking = True
    while looking:
        time.sleep(time_delay)
        obj = pyautogui.locateOnScreen(list_of_data[FILE_LOC], confidence=confidence_num)
        obj_location = ExceptionHandler(obj, list_of_data[NEED_HELP], excption)
        excption+=1
        if obj_location != EMPTY:
            return obj_location
        elif special_flag:
            return EMPTY 

def ProcessCheck(process):
    """Check if there is any running process that contains the given name process."""

    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if process.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False
# main bish
main()













