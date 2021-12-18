import pyautogui
import os
import signal
import psutil
import pyperclip

pyautogui.PAUSE = 0.75
pyautogui.FAILSAFE = True

class Computer():
    def __init__(self) -> None:
        pass

    def altF4():
        pyautogui.hotkey('alt','f4')
    
    def appStatus(process):
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

    def click(location):
        pyautogui.click(location)

    def copy():
        pyautogui.hotkey('ctrl','c')

    def ctrlF4():
        pyautogui.hotkey('ctrl','f4')
    
    def ctrlT():
        pyautogui.hotkey('ctrl','t')

    def doubleClick(location):
        pyautogui.doubleClick(location)

    def getClipboardItem():
        clipboard_item = pyperclip.paste()
        return clipboard_item
        
    def killApp(process_name):
        pid = None
        for proc in psutil.process_iter():
            if process_name in proc.name():
                pid = proc.pid
        sig= signal.SIGTERM
        os.kill(pid, sig)
        
    def launchApp(self, app):
        app_running = False
        while not app_running:
            if app == "edge":
                try:
                    os.startfile('"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"') 
                    app_running = self.appStatus("msedge")         
                except Exception:
                    pass
            elif app == "andr_studio":
                try:
                    os.startfile('"C:/Program Files/Android/Android Studio/bin/studio64.exe"')
                    app_running = self.appStatus("studio64")
                except Exception:
                    pass

    def moveMouse():
        pyautogui.moveTo(100,100)

    def write(text, key=False):
        if not key:
            pyautogui.typewrite(text)
        else:
            pyautogui.typewrite([text])