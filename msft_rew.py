# Main TODOs
# - Make it work consistently lmao 
# - Add clean list to new doc, delete old list (verify contents are clean)
# - Move random word generator to new class
# - Potentially have a smart setup for the timers on here that can adapt 
# -- Would have timer configs in a separate file, would have time be controlled by Computer class
# - Other crackpot organizational/efficient things
# - Add documentation 
# - Move to laptop (or any available compatible device)

import random
import pyautogui
import time
import json
from classes.computer import Computer
from classes.image_handler import ImageHandler

EMPTY = ""
PC_REWARD_CAP = "150"
MOB_REWARD_CAP = "100"
# How confident are you bruv?
VERY_CONFIDENT = 0.9
CONFIDENT = 0.8 # default 
SLIGHTLY_CONFIDENT = 0.7
SLIGHTLY_NOT_CONFIDENT = 0.6
NOT_CONFIDENT = 0.5
#TODO Enum probs
EDGE = 1
ANDR_STUD = 2 
# Debugging purposes only
DEBUG_MODE = False

# my main man
def main():

    # JSOOOOOOOOOOOOOOOOOOOOON
    with open("files/pic_data.json") as file:
        pic_data = json.load(file)

    image_handler = ImageHandler(pic_data)
    edge = "edge"
    andr_studio = "andr_studio"

    # idk I made a dict of all the shit I needed, we'll see if it's needed lmao
    desired_data = {}
    for data in pic_data:
        desired_data.update({data["Order_Used"]:data["Obj_Name"]})

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
    
    Computer.launchApp(Computer,edge)
    if not DEBUG_MODE:
        image_handler.imgHandler(desired_data["0"])

    if not DEBUG_MODE:
        # going to bing.com
        Computer.ctrlT()
        Computer.write('bing.com')
        Computer.write('enter',True)
        pc_count = 1 
    else:
        pc_count = 30
    
    pc_keep_going = True
    while pc_keep_going:

        if not DEBUG_MODE:         
            LetsGetRandom(word_list)

            Computer.write('f6', True)
            Computer.write('f6', True)
            Computer.write('bing.com')
            Computer.write('enter', True)

        pc_count+=1
        if pc_count >= 30:
            #TODO better way to do this would be w/ "requests" lib and for security maybe "secrets", idek
            special_loop = True
            time_delay = 1
            while special_loop:

                image_handler.imgHandler(desired_data["0"])
                earnings_location = image_handler.imgHandler(desired_data["1"], False, special_loop, CONFIDENT, time_delay)
                if earnings_location != EMPTY:
                    special_loop = False
  
            if not DEBUG_MODE:
                rewards_value = Computer.getClipboardItem()
                if rewards_value == PC_REWARD_CAP:
                    pc_keep_going = False
                    Computer.altF4()
                else:
                    pc_count = 25
            else:
                Computer.altF4()
                pc_keep_going = False

    ###############################################
    # Functionality for mobile points starts here #
    ###############################################

    Computer.launchApp(Computer, andr_studio)

    # clicking avd manager
    image_handler.imgHandler(desired_data["2"])

    # clicking play on vm
    image_handler.imgHandler(desired_data["3"])  

    # clicking vm power button 
    image_handler.imgHandler(desired_data["4"])

    #TODO does this stop the "UI stop responsing" msg popup?
    # ^Seems like it does
    time.sleep(1.5)

    # mama im coming hooOOOooomme (clicking home button on vm)
    special_loop = True
    while special_loop:
        image_handler.imgHandler(desired_data["5"])
        
        # flagging the problem child, plays loop back
        vm_chrome_app_location = image_handler.imgHandler(desired_data["6"], True, special_loop)
        if vm_chrome_app_location != EMPTY:
            special_loop = False

    special_loop = True
    while special_loop:      
        image_handler.imgHandler(desired_data["7"], True, special_loop, NOT_CONFIDENT)
        image_handler.imgHandler(desired_data["8"], True, special_loop)
        did_search_load = image_handler.imgHandler(desired_data["9"], True, special_loop, NOT_CONFIDENT)
        if did_search_load != EMPTY:
            special_loop = False

    mobile_keep_going = True
    mobile_count = 0 
    while mobile_keep_going:
        special_loop = True
        counter = 0 
        while special_loop: 

            time.sleep(.5)
            Computer.moveMouse()
            image_handler.imgHandler(desired_data["9"], True, special_loop)
            Computer.moveMouse()
            
            # click the x button that appears when you click on search; clears search
            vm_search_x_bttn_location = image_handler.imgHandler(desired_data["10"], True, special_loop)
            if vm_search_x_bttn_location != EMPTY:
                special_loop = False

        #TODO does this stop VM from crashing lmao this is new 
        time.sleep(.5)
        LetsGetRandom(word_list)

        mobile_count +=1 
        if DEBUG_MODE:
            mobile_count = 20
        if mobile_count >= 20:
            
            Computer.launchApp(Computer, edge)
            special_loop = True
            while special_loop:

                image_handler.imgHandler(desired_data["0"])
                mobile_earnings_location = image_handler.imgHandler(desired_data["11"], False, special_loop)
                if mobile_earnings_location != EMPTY:
                    special_loop = False

            rewards_value = Computer.getClipboardItem()
            if rewards_value == MOB_REWARD_CAP:
                mobile_keep_going = False
                Computer.altF4()
            else:
                Computer.altF4()
                mobile_count = 15
    
    # cleanup crew
    image_handler.imgHandler(desired_data["17"])
    image_handler.imgHandler(desired_data["18"])
    image_handler.imgHandler(desired_data["19"])
    image_handler.imgHandler(desired_data["20"])
    image_handler.imgHandler(desired_data["21"])
    time.sleep(.25)
    Computer.write("rewards.microsoft")
    time.sleep(.25)
    Computer.write(".com/points")
    Computer.write("breakdown")
    time.sleep(.5)
    Computer.write('enter', True)

    image_handler.imgHandler(desired_data["4"])
    Computer.altF4()

    process_name = "studio64"
    Computer.killApp(process_name)

    # Start of daily points clicker
    # mini games research
    # ideally would like to have all their major games booked and studied so bot can squeeze out a few more pts
    
    Computer.launchApp(Computer, edge)
    counter = 0 
    time_delay = 1.5
    special_loop = True
    while special_loop:
        
        image_handler.imgHandler(desired_data["0"])
        daily_poll_location = image_handler.imgHandler(desired_data["15"], True, True, SLIGHTLY_CONFIDENT, time_delay)
        if daily_poll_location != EMPTY:
            image_handler.imgHandler(desired_data["16"], True, True, SLIGHTLY_CONFIDENT, time_delay)
            special_loop = False
        
        counter+=1
        if counter >= 10:
            special_loop = False

    for x in range(3):

        image_handler.imgHandler(desired_data["0"])

        pts10_extra_activity_location = image_handler.imgHandler(desired_data["12"], True, True, SLIGHTLY_CONFIDENT, time_delay)
        if pts10_extra_activity_location != EMPTY:
            Computer.ctrlF4()
            image_handler.imgHandler(desired_data["0"])
        
        pts5_extra_activity_location = image_handler.imgHandler(desired_data["13"], True, True, SLIGHTLY_CONFIDENT, time_delay)
        if pts5_extra_activity_location != EMPTY:
            Computer.ctrlF4()
        
    for x in range(3):

        special_loop = True
        while special_loop:

            image_handler.imgHandler(desired_data["0"])
            more_activities_location = image_handler.imgHandler(desired_data["14"], True, special_loop)
            if more_activities_location != EMPTY:
                special_loop = False
  
        pts10_extra_activity_location = image_handler.imgHandler(desired_data["12"], True, True, SLIGHTLY_CONFIDENT, time_delay)
        if pts10_extra_activity_location != EMPTY:
            Computer.ctrlF4() 

        pts5_extra_activity_location = image_handler.imgHandler(desired_data["12"], True, True, SLIGHTLY_CONFIDENT, time_delay)
        if pts5_extra_activity_location != EMPTY:
            Computer.ctrlF4()  
    
    

    Computer.ctrlF4()

#################
#### Modules ####
#################
def LetsGetRandom(word_list):
    """Probably going to be under a big ole Pyautogui class"""    
    pyautogui.typewrite(str(word_list[random.randint(0,10000)]))
    time.sleep(.5)
    pyautogui.typewrite(['enter'])

# main bish
main()













