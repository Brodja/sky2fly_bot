from glob import glob
import cv2
import pyautogui
# from PIL import ImageGrab
import pyscreenshot as ImageGrab
import threading
import time
import keyboard
import multiprocessing
from multiprocessing import Process, Value


main_flag = True



def f2():
    global main_flag
    while(main_flag):
        print('Second', main_flag)
        time.sleep(2)
def kill():
    global main_flag
    while main_flag:
        pyautogui.press('home')
        time.sleep(0.1)   
# def loot():
#     global main_flag # stop, activ, ok
#     take = cv2.imread('./icon/take.png')
#     shipX = 960 #730  # +-225
#     shipY = 480 #460  # 130
#     range = 160
#     arr = [
#         [range, 0, range + 5, -55, range + 40, -17, range - 15, + 45],
#         [0, range, 5, range - 55, 60 - 20, range - 17, -15, range + 45],
#         [-range, 0, -range + 5, -55, -range + 60 - 20, -17, -range - 15, + 45],
#         [0, -range, 5, -range - 55, 60 - 20, -range - 17, -15, -range + 45]]
#     while main_flag:
#         i = 0
#         # if activ == 1 and pause == 0 and sky is True and ok ==1:
#         while i < 4:
#             pyautogui.click(x=shipX + arr[i][0], y=shipY + arr[i][1])
#             time.sleep(0.2)
#             pyautogui.click(x=shipX + arr[i][6], y=shipY + arr[i][7])
#             screen_take_menu = ImageGrab.grab(bbox=(shipX + arr[i][2], shipY + arr[i][3], shipX + arr[i][4], shipY + arr[i][5]))
#             screen_take_menu.save('./temp_icon/screen_take_menu.png')
#             screen_take_menu = cv2.imread('./temp_icon/screen_take_menu.png')
#             result = cv2.matchTemplate(screen_take_menu, take, cv2.TM_CCOEFF_NORMED)
#             (min_x, max_y, minloc, maxloc) = cv2.minMaxLoc(result)
#             if max_y > 0.8:
#                 pyautogui.click(x=maxloc[0] + shipX + arr[i][2], y=maxloc[1] + shipY + arr[i][3])
#             i += 1
#             # time.sleep(0.2)

def loot():
    global main_flag # stop, activ, ok
    take = cv2.imread('./icon/take.png')
    shipX = 960 #730  # +-225
    shipY = 480 #460  # 130
    range = 140
    arr = [
        [range, 0, range + 5, -55, range + 40, -17, range - 15, + 45],
        [0, range, 5, range - 55, 60 - 20, range - 17, -15, range + 45],
        [-range, 0, -range + 5, -55, -range + 60 - 20, -17, -range - 15, + 45],
        [0, -range, 5, -range - 55, 60 - 20, -range - 17, -15, -range + 45]]
    start_time = time.time()
    while main_flag:
        i = 0
        # if activ == 1 and pause == 0 and sky is True and ok ==1:
        while i < 4:
            pyautogui.click(x=shipX + arr[i][0], y=shipY + arr[i][1])
            time.sleep(0.05)
            pyautogui.click(x=shipX + arr[i][6], y=shipY + arr[i][7])
            pyautogui.screenshot('./temp_icon/screen_take_menu.png',region=(shipX+arr[i][2],shipY+arr[i][3], 50, 50))
            screen_take_menu = cv2.imread('./temp_icon/screen_take_menu.png')
            result = cv2.matchTemplate(screen_take_menu, take, cv2.TM_CCOEFF_NORMED)
            (min_x, max_y, minloc, maxloc) = cv2.minMaxLoc(result)
            if max_y > 0.8:
                pyautogui.click(x=maxloc[0] + shipX + arr[i][2], y=maxloc[1] + shipY + arr[i][3])
            i += 1
            pyautogui.press('esc')
            # time.sleep(1)

processKill = 0
processLoot = 0
ACTIVE_STATUS = False
# p2=Process(target=f2)
num = Value('d', 0.0)
def startProcess():
    global processKill, processLoot
    processKill=Process(target=kill)
    processKill.start()
    processLoot=Process(target=loot)
    processLoot.start()

def stopProcess():
    global processKill, processLoot
    processKill.terminate()    
    processKill = 0
    processLoot.terminate()    
    processLoot = 0

def worker():
    global main_flag, ACTIVE_STATUS
    while main_flag:
        if keyboard.is_pressed('0'):
            if ACTIVE_STATUS == True:
                stopProcess()
                print('stop Process')
                ACTIVE_STATUS = False
            print('0')
        elif keyboard.is_pressed('1'):
            if ACTIVE_STATUS == False:
                startProcess()
                print('start Process')
                ACTIVE_STATUS = True
        time.sleep(2)     



if __name__=="__main__":
    worker()
