# Main TODOs
# - Create json file for pictures and descriptions 
# - Get words from local vs internet (would be faster/less expensive)
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
import requests
import pyperclip
import logging
import os

EMPTY = ""
PC_REWARD_CAP = "150"
MOB_REWARD_CAP = "100"
#TODO Enum probs
EDGE = 1
ANDR_STUD = 2 

# failsafes, drag mouse to top left corner of screen to quit app
pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True

def main():

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

    # waiting on browser (can adjust)
    time.sleep(2)

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
            
            #TODO put all the pic info w description in json file
            pic_rewards = "pics/rewards_icon.png"
            need_help = "msft rewards button"
            msft_rewards_location = LookingForLocation(pic_rewards, need_help)
            pyautogui.click(msft_rewards_location)
            
            pic_earnings = "pics/pc_earnings_icon.png"
            need_help = "the area in rewards extension"
            earnings_location = LookingForLocation(pic_earnings, need_help)
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
    pic_avd = "pics/as_avd_manager.png"
    need_help = "avd manager"
    avd_mgr_location = LookingForLocation(pic_avd, need_help)
    pyautogui.click(avd_mgr_location)
    
    # clicking play on vm
    pic_as_vm_play = "pics/as_vm_play.png"
    need_help = "the play button in avd manager"
    as_vm_play_location = LookingForLocation(pic_as_vm_play, need_help)
    pyautogui.click(as_vm_play_location)

    # clicking vm power button 
    pic_as_vm_pwr_bttn = "pics/as_vm_pwr_bttn.png"
    need_help = "power button on phone vm"
    as_vm_pwr_bttn_location = LookingForLocation(pic_as_vm_pwr_bttn, need_help)
    pyautogui.click(as_vm_pwr_bttn_location)

    # mama im coming hooOOOooomme (clicking home button on vm)
    special_loop = True
    while special_loop:
        pic_as_vm_home_bttn = "pics/as_vm_home_bttn.png"
        need_help = "home button a few buttons below power button"
        as_vm_home_bttn_location = LookingForLocation(pic_as_vm_home_bttn, need_help)
        pyautogui.click(as_vm_home_bttn_location)

        # flagging the problem child, plays loop back
        pic_vm_chrome_app = "pics/vm_chrome_app.png"
        need_help = "the chrome app on vm"
        vm_chrome_app_location = LookingForLocation(pic_vm_chrome_app, need_help, special_loop)
        if vm_chrome_app_location != EMPTY:
            pyautogui.click(vm_chrome_app_location)
            special_loop = False

    # clicking mobile search link
    pic_vm_mobile_search_link = "pics/vm_mobile_search_link.png"
    need_help = "the mobile rewards link on points breakdown"
    vm_mobile_search_link_location = LookingForLocation(pic_vm_mobile_search_link, need_help)
    pyautogui.click(vm_mobile_search_link_location)

    mobile_keep_going = True
    mobile_count = 0 
    while mobile_keep_going:

        # clicking search
        pic_vm_rewards_search = "pics/vm_rewards_search.png"
        need_help = "the search area after you click on rewards link"
        vm_rewards_search_location = LookingForLocation(pic_vm_rewards_search, need_help)
        pyautogui.click(vm_rewards_search_location)
        
        # click the x button that appears when you click on search; clears search
        pic_vm_search_x_bttn = "pics/vm_search_x_bttn.png"
        need_help = "the 'x' that appears after clicking on search box"
        vm_search_x_bttn_location = LookingForLocation(pic_vm_search_x_bttn, need_help)
        pyautogui.click(vm_search_x_bttn_location)

        LetsGetRandom(word_list)

        mobile_count +=1 

        if mobile_count >= 10:
            
            AppLauncher(EDGE)
            special_loop = True
            while special_loop:
                pic_rewards = "pics/rewards_icon.png"
                need_help = "msft rewards button"
                msft_rewards_location = LookingForLocation(pic_rewards, need_help)
                pyautogui.click(msft_rewards_location)

                # potential problem child
                pic_mobile_earnings = "pics/mobile_earnings_icon.png"
                need_help = "the rewards ext area"
                mobile_earnings_location = LookingForLocation(pic_mobile_earnings, need_help, special_loop)
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













