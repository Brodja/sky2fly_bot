import cv2
import pyautogui
from PIL import ImageGrab
import threading
import time
import keyboard

pathImg = '/skybot/Pictures/bot/'
whileFlag = True
stop = 0
tree = 0
activ = 0
pause = 0
saw = 1
treeCenter = 0
sawNum = 0
full = 0
sky = False
die = 0
fic = 0
updateK = 0
ok = 1

def paused():
    global pause, activ
    while pause == 1 or pause == 0:
        if keyboard.is_pressed('0'):
            pause = 0
            activ = 1
        elif keyboard.is_pressed('1'):
            pause = 1

def goFromBase():
    temp = ImageGrab.grab(bbox=(800, 40, 1260, 255))
    temp.save('/Users'+pathImg+'temp.png')
    temp = cv2.imread('/Users'+pathImg+'temp.png')
    temp_seach = cv2.imread('/Users'+pathImg+'air_btn.png')
    result = cv2.matchTemplate(temp, temp_seach, cv2.TM_CCOEFF_NORMED)
    (min_x, max_y, minloc, maxloc) = cv2.minMaxLoc(result)
    pyautogui.click(x=maxloc[0] + 800 + 25, y=maxloc[1] + 40 + 15)
    time.sleep(1)
    temp = ImageGrab.grab(bbox=(275, 160, 1240, 800))
    temp.save('/Users'+pathImg+'temp.png')
    temp = cv2.imread('/Users'+pathImg+'temp.png')
    temp_seach = cv2.imread('/Users'+pathImg+'tonel1.png')
    #temp_seach = cv2.imread('/Users' + pathImg + 'ikarD.png')
    result = cv2.matchTemplate(temp, temp_seach, cv2.TM_CCOEFF_NORMED)
    (min_x, max_y, minloc, maxloc) = cv2.minMaxLoc(result)
    pyautogui.click(x=maxloc[0] + 275 + 5, y=maxloc[1] + 160 + 5)
    del temp, temp_seach

def goToTree():
    global tree
    temp = ImageGrab.grab(bbox=(270, 245, 1200, 780))
    temp.save('/Users'+pathImg+'temp.png')
    temp = cv2.imread('/Users'+pathImg+'temp.png')
    temp_seach = cv2.imread('/Users'+pathImg+'screen_tree.png')
    result = cv2.matchTemplate(temp, temp_seach, cv2.TM_CCOEFF_NORMED)
    (min_x, max_y, minloc, maxloc) = cv2.minMaxLoc(result)
    if max_y > 0.9:
        print('Нашел')
        tree = 1
        pyautogui.click(x=maxloc[0] + 270, y=maxloc[1] + 245, button='right')
        time.sleep(10)
    else:
        temp_seach = cv2.imread('/Users' + pathImg + 'screen_tree2.png')
        result = cv2.matchTemplate(temp, temp_seach, cv2.TM_CCOEFF_NORMED)
        (min_x, max_y, minloc, maxloc) = cv2.minMaxLoc(result)
        if max_y > 0.9:
            print('Нашел 2')
            tree = 1
            pyautogui.click(x=maxloc[0] + 270, y=maxloc[1] + 245, button='right')
            time.sleep(10)
        else:
            print('НЕТУ ДЕРЕВА')

    del temp, temp_seach

def goCenterTree():
    global treeCenter
    centerTree = cv2.imread('/Users'+pathImg+'centerTree.png')
    while treeCenter == 0:
        screen_sky = ImageGrab.grab(bbox=(300, 100, 1060, 780))
        screen_sky.save('/Users'+pathImg+'screen_sky.png')
        screen_sky = cv2.imread('/Users'+pathImg+'screen_sky.png')
        center = (50, 50)
        i = 0
        while i < 360:
            M = cv2.getRotationMatrix2D(center, i, 1.0)
            rotated = cv2.warpAffine(centerTree, M, (100, 100))
            crop_img = rotated[20:80, 20:80]
            result = cv2.matchTemplate(screen_sky, crop_img, cv2.TM_CCOEFF_NORMED)
            (min_x, max_y, minloc, maxloc) = cv2.minMaxLoc(result)
            if max_y > 0.7:
                print('CENTER')
                pyautogui.click(x=maxloc[0] + 300 + 30, y=maxloc[1] + 100 + 30, button='right')
                i = 360
                time.sleep(8)
                treeCenter = 1
                del screen_sky, centerTree
            else:
                treeCenter = 0
            i += 5
        if treeCenter == 0:
            print('Корректировка')
            pyautogui.click(x=700, y=450, button='right')
            time.sleep(7)

def kill():
    global stop, activ, ok
    while whileFlag:
        if activ == 1 and pause == 0 and ok ==1:
            pyautogui.press('home')
            time.sleep(0.1)

def calc():
    global activ, pause, sawNum
    while whileFlag:
        if activ == 1 and pause == 0 and saw == 1:
            print(sawNum)
            if sawNum < 200:
                pyautogui.press('5')
                sawNum += 1
                time.sleep(10)

def loot():
    global stop, activ, ok
    take = cv2.imread('/Users' + pathImg + 'take.png')
    shipX = 730  # +-225
    shipY = 460  # 130
    range = 130
    arr = [
        [range, 0, range + 5, -55, range + 40, -17, range - 15, + 45],
        [0, range, 5, range - 55, 60 - 20, range - 17, -15, range + 45],
        [-range, 0, -range + 5, -55, -range + 60 - 20, -17, -range - 15, + 45],
        [0, -range, 5, -range - 55, 60 - 20, -range - 17, -15, -range + 45]]
    while whileFlag:
        i = 0
        if activ == 1 and pause == 0 and sky is True and ok ==1:
            while i < 4:
                pyautogui.click(x=shipX + arr[i][0], y=shipY + arr[i][1])
                screen_take_menu = ImageGrab.grab(
                    bbox=(shipX + arr[i][2], shipY + arr[i][3], shipX + arr[i][4], shipY + arr[i][5]))
                screen_take_menu.save('/screen_take_menu.png')
                screen_take_menu = cv2.imread('/screen_take_menu.png')
                result = cv2.matchTemplate(screen_take_menu, take, cv2.TM_CCOEFF_NORMED)
                (min_x, max_y, minloc, maxloc) = cv2.minMaxLoc(result)
                if max_y > 0.9:
                    pyautogui.click(x=maxloc[0] + shipX + arr[i][2], y=maxloc[1] + shipY + arr[i][3])
                # pyautogui.click(x=shipX + arr[i][6], y=shipY + arr[i][7])
                i += 1
                time.sleep(0.2)

def checkTarget():
    taret = cv2.imread('/Users' + pathImg + 'target.png')
    taretAlpha = cv2.imread('/Users' + pathImg + 'alfa.png')
    taretBeta = cv2.imread('/Users' + pathImg + 'beta.png')
    taretDelta = cv2.imread('/Users' + pathImg + 'delta.png')
    taretGamma = cv2.imread('/Users' + pathImg + 'gamma.png')
    global activ, stop
    while whileFlag:
        if activ == 1:
            screen_sky = ImageGrab.grab(bbox=(230, 35, 1000, 250))
            screen_sky.save('/Users' + pathImg + 'screen_sky.png')
            screen_sky = cv2.imread('/Users' + pathImg + 'screen_sky.png')
            targetResult = cv2.matchTemplate(screen_sky, taret, cv2.TM_CCOEFF_NORMED)
            (min_x, TargetMax_y, minloc, maxloc) = cv2.minMaxLoc(targetResult)
            if TargetMax_y > 0.9:
                AlphaResult = cv2.matchTemplate(screen_sky, taretAlpha, cv2.TM_CCOEFF_NORMED)
                (min_x, TargetAMax_y, minloc, maxloc) = cv2.minMaxLoc(AlphaResult)
                if TargetAMax_y < 0.9:
                    BetaResult = cv2.matchTemplate(screen_sky, taretBeta, cv2.TM_CCOEFF_NORMED)
                    (min_x, TargetBMax_y, minloc, maxloc) = cv2.minMaxLoc(BetaResult)
                    if TargetBMax_y < 0.9:
                        DeltaResult = cv2.matchTemplate(screen_sky, taretDelta, cv2.TM_CCOEFF_NORMED)
                        (min_x, TargetDMax_y, minloc, maxloc) = cv2.minMaxLoc(DeltaResult)
                        if TargetDMax_y < 0.9:
                            GammaResult = cv2.matchTemplate(screen_sky, taretGamma, cv2.TM_CCOEFF_NORMED)
                            (min_x, TargetGMax_y, minloc, maxloc) = cv2.minMaxLoc(GammaResult)
                            if TargetGMax_y < 0.9:
                                print('не червь')
                                pyautogui.press('4')
                                pyautogui.press('4')
                                activ = 0
                                pyautogui.press('4')
                                pyautogui.press('4')
                                pyautogui.press('down')
                                stop = 1
                                writeMe()

def writeMe():
    pyautogui.click(x=400, y=1000)
    time.sleep(2)
    tempInter = ImageGrab.grab(bbox=(30, 50, 1100, 950))
    tempInter.save('/Users/' + pathImg + 'tempInter.png')
    tempInter = cv2.imread('/Users' + pathImg + 'tempInter.png')
    tempBtn = cv2.imread('/Users' + pathImg + 'me.png')
    result = cv2.matchTemplate(tempInter, tempBtn, cv2.TM_CCOEFF_NORMED)
    (min_x, max_y, minloc, maxloc) = cv2.minMaxLoc(result)
    pyautogui.click(x=maxloc[0] + 35, y=maxloc[1] + 55)

    time.sleep(2)
    tempInter = ImageGrab.grab(bbox=(30, 50, 1100, 950))
    tempInter.save('/Users/' + pathImg + 'tempInter.png')
    tempInter = cv2.imread('/Users' + pathImg + 'tempInter.png')
    tempBtn = cv2.imread('/Users' + pathImg + 'smile.png')
    result = cv2.matchTemplate(tempInter, tempBtn, cv2.TM_CCOEFF_NORMED)
    (min_x, max_y, minloc, maxloc) = cv2.minMaxLoc(result)
    pyautogui.click(x=maxloc[0] + 35, y=maxloc[1] + 55)

def goToTonelFromTree():
    take = cv2.imread('/Users'+pathImg+'hand_base.png')
    shipX = 760  # +-225
    shipY = 460  # 130
    range = 300
    rangeM = 220
    arr = [
        [range, 0, range - 60, -60, range + 60, 60, range - 60, -60],
        [0, range, -60, range - 60, 60, range + 60, -60, range - 60],
        [-range, 0, -range - 60, -60, -range + 60, 60, -range - 60, -60],
        [0, -range, -60, -range - 60, 60, -range + 60, -60, -range - 60],
        [-rangeM, -rangeM, -rangeM - 60, -rangeM - 60, -rangeM + 60, -rangeM + 60, -rangeM - 60, -rangeM - 60],
        [rangeM, -rangeM, rangeM - 60, -rangeM - 60, rangeM + 60, -rangeM + 60, rangeM - 60, -rangeM - 60],
        [rangeM, rangeM, rangeM - 60, rangeM - 60, rangeM + 60, rangeM + 60, rangeM - 60, rangeM - 60],
        [-rangeM, rangeM, -rangeM - 60, rangeM - 60, -rangeM + 60, rangeM + 60, -rangeM - 60, rangeM - 60]]
    i = 0
    while i < 8:
        pyautogui.click(x=shipX + arr[i][0], y=shipY + arr[i][1])
        screen_take_menu = ImageGrab.grab(
            bbox=(shipX + arr[i][2], shipY + arr[i][3], shipX + arr[i][4], shipY + arr[i][5]))
        screen_take_menu.save('/Users/'+pathImg+'screen_take_menu2.png')
        screen_take_menu = cv2.imread('/Users'+pathImg+'screen_take_menu2.png')
        resultXP = cv2.matchTemplate(screen_take_menu, take, cv2.TM_CCOEFF_NORMED)
        (min_x, max_y, minlocXP, maxlocXP) = cv2.minMaxLoc(resultXP)
        if max_y > 0.9:
            pyautogui.click(x=shipX, y=shipY)
            time.sleep(1.5)
            pyautogui.click(x=maxlocXP[0] + shipX + arr[i][6], y=maxlocXP[1] + shipY + arr[i][7], button='right')
            i = 8

        i += 1
        time.sleep(0.2)

    time.sleep(10)
    temp = ImageGrab.grab(bbox=(360, 150, 1030, 770))
    temp.save('/Users'+pathImg+'temp.png')
    temp = cv2.imread('/Users'+pathImg+'temp.png')
    temp_seach = cv2.imread('/Users'+pathImg+'close.png')
    result = cv2.matchTemplate(temp, temp_seach, cv2.TM_CCOEFF_NORMED)
    (min_x, max_y, minloc, maxloc) = cv2.minMaxLoc(result)
    if max_y > 0.8:
        pyautogui.click(x=maxloc[0] + 363, y=maxloc[1] + 153)
    del take, temp, temp_seach, result, screen_take_menu, resultXP, arr

def goBaseFromTonel():
    pyautogui.press('down')
    take = cv2.imread('/Users' + pathImg + 'hand_base.png')
    shipX = 760  # +-225
    shipY = 460  # 130
    range = 100
    rangeM = 70
    arr = [
        [range, 0, range - 60, -60, range + 60, 60, range - 60, -60],
        [0, range, -60, range - 60, 60, range + 60, -60, range - 60],
        [-range, 0, -range - 60, -60, -range + 60, 60, -range - 60, -60],
        [0, -range, -60, -range - 60, 60, -range + 60, -60, -range - 60],
        [-rangeM, -rangeM, -rangeM - 60, -rangeM - 60, -rangeM + 60, -rangeM + 60, -rangeM - 60, -rangeM - 60],
        [rangeM, -rangeM, rangeM - 60, -rangeM - 60, rangeM + 60, -rangeM + 60, rangeM - 60, -rangeM - 60],
        [rangeM, rangeM, rangeM - 60, rangeM - 60, rangeM + 60, rangeM + 60, rangeM - 60, rangeM - 60],
        [-rangeM, rangeM, -rangeM - 60, rangeM - 60, -rangeM + 60, rangeM + 60, -rangeM - 60, rangeM - 60]]
    i = 0
    while i < 8:
        pyautogui.click(x=shipX + arr[i][0], y=shipY + arr[i][1])
        screen_take_menu = ImageGrab.grab(bbox=(shipX + arr[i][2], shipY + arr[i][3], shipX + arr[i][4], shipY + arr[i][5]))
        screen_take_menu.save('/Users/' + pathImg + 'screen_take_menu2.png')
        screen_take_menu = cv2.imread('/Users' + pathImg + 'screen_take_menu2.png')
        resultXP = cv2.matchTemplate(screen_take_menu, take, cv2.TM_CCOEFF_NORMED)
        (min_x, max_y, minlocXP, maxlocXP) = cv2.minMaxLoc(resultXP)
        if max_y > 0.9:
            pyautogui.click(x=maxlocXP[0] + shipX + arr[i][6], y=maxlocXP[1] + shipY + arr[i][7])
            i = 8

        i += 1
        time.sleep(0.2)

    time.sleep(0.5)
    temp = ImageGrab.grab(bbox=(360, 150, 1030, 770))
    temp.save('/Users'+pathImg+'temp.png')
    temp = cv2.imread('/Users'+pathImg+'temp.png')
    temp_seach = cv2.imread('/Users'+pathImg+'goBaseFromSky.png')
    result = cv2.matchTemplate(temp, temp_seach, cv2.TM_CCOEFF_NORMED)
    (min_x, max_y, minloc, maxloc) = cv2.minMaxLoc(result)
    pyautogui.click(x=maxloc[0] + 370, y=maxloc[1] + 155)
    del temp, temp_seach, screen_take_menu, take


def update():
    global fic, updateK
    fic += 1
    updateK = 1

    tempBaseFull = ImageGrab.grab(bbox=(280, 100, 1255, 970))
    tempBaseFull.save('/Users/' + pathImg + 'tempBaseFull.png')
    tempBaseFull = cv2.imread('/Users' + pathImg + 'tempBaseFull.png')
    tempBase = cv2.imread('/Users' + pathImg + 'close.png')
    resultXP = cv2.matchTemplate(tempBaseFull, tempBase, cv2.TM_CCOEFF_NORMED)
    (min_x, max_y, minlocXP, maxlocXP) = cv2.minMaxLoc(resultXP)
    pyautogui.click(x=maxlocXP[0] + 283, y=maxlocXP[1] + 103)

    time.sleep(0.5)

    tempBaseFull = ImageGrab.grab(bbox=(280, 100, 1255, 970))
    tempBaseFull.save('/Users/' + pathImg + 'tempBaseFull.png')
    tempBaseFull = cv2.imread('/Users' + pathImg + 'tempBaseFull.png')
    tempBase = cv2.imread('/Users' + pathImg + 'sklad.png')
    resultXP = cv2.matchTemplate(tempBaseFull, tempBase, cv2.TM_CCOEFF_NORMED)
    (min_x, max_y, minlocXP, maxlocXP) = cv2.minMaxLoc(resultXP)
    pyautogui.click(x=maxlocXP[0] + 283, y=maxlocXP[1] + 103)

    time.sleep(0.5)

    tempBaseFull = ImageGrab.grab(bbox=(280, 100, 1255, 970))
    tempBaseFull.save('/Users/' + pathImg + 'tempBaseFull.png')
    tempBaseFull = cv2.imread('/Users' + pathImg + 'tempBaseFull.png')
    tempBase = cv2.imread('/Users' + pathImg + 'toSklad.png')
    resultXP = cv2.matchTemplate(tempBaseFull, tempBase, cv2.TM_CCOEFF_NORMED)
    (min_x, max_y, minlocXP, maxlocXP) = cv2.minMaxLoc(resultXP)
    pyautogui.click(x=maxlocXP[0] + 283, y=maxlocXP[1] + 103)

    time.sleep(0.5)

    tempBaseFull = ImageGrab.grab(bbox=(280, 100, 1255, 970))
    tempBaseFull.save('/Users/' + pathImg + 'tempBaseFull.png')
    tempBaseFull = cv2.imread('/Users' + pathImg + 'tempBaseFull.png')
    tempBase = cv2.imread('/Users' + pathImg + 'goOut.png')
    resultXP = cv2.matchTemplate(tempBaseFull, tempBase, cv2.TM_CCOEFF_NORMED)
    (min_x, max_y, minlocXP, maxlocXP) = cv2.minMaxLoc(resultXP)
    pyautogui.click(x=maxlocXP[0] + 283, y=maxlocXP[1] + 103)

    time.sleep(0.5)

    tempBaseFull = ImageGrab.grab(bbox=(280, 100, 1255, 970))
    tempBaseFull.save('/Users/' + pathImg + 'tempBaseFull.png')
    tempBaseFull = cv2.imread('/Users' + pathImg + 'tempBaseFull.png')
    tempBase = cv2.imread('/Users' + pathImg + 'servise.png')
    resultXP = cv2.matchTemplate(tempBaseFull, tempBase, cv2.TM_CCOEFF_NORMED)
    (min_x, max_y, minlocXP, maxlocXP) = cv2.minMaxLoc(resultXP)
    pyautogui.click(x=maxlocXP[0] + 283, y=maxlocXP[1] + 103)

    time.sleep(0.5)

    tempBaseFull = ImageGrab.grab(bbox=(280, 100, 1255, 970))
    tempBaseFull.save('/Users/' + pathImg + 'tempBaseFull.png')
    tempBaseFull = cv2.imread('/Users' + pathImg + 'tempBaseFull.png')
    tempBase = cv2.imread('/Users' + pathImg + 'serviseDl.png')
    resultXP = cv2.matchTemplate(tempBaseFull, tempBase, cv2.TM_CCOEFF_NORMED)
    (min_x, max_y, minlocXP, maxlocXP) = cv2.minMaxLoc(resultXP)
    pyautogui.click(x=maxlocXP[0] + 283, y=maxlocXP[1] + 113)

    time.sleep(0.5)

    tempBaseFull = ImageGrab.grab(bbox=(280, 100, 1255, 970))
    tempBaseFull.save('/Users/' + pathImg + 'tempBaseFull.png')
    tempBaseFull = cv2.imread('/Users' + pathImg + 'tempBaseFull.png')
    tempBase = cv2.imread('/Users' + pathImg + 'doki.png')
    resultXP = cv2.matchTemplate(tempBaseFull, tempBase, cv2.TM_CCOEFF_NORMED)
    (min_x, max_y, minlocXP, maxlocXP) = cv2.minMaxLoc(resultXP)
    pyautogui.click(x=maxlocXP[0] + 283, y=maxlocXP[1] + 103)

    time.sleep(0.5)

    tempBaseFull = ImageGrab.grab(bbox=(280, 100, 1255, 970))
    tempBaseFull.save('/Users/' + pathImg + 'tempBaseFull.png')
    tempBaseFull = cv2.imread('/Users' + pathImg + 'tempBaseFull.png')
    tempBase = cv2.imread('/Users' + pathImg + 'korBtn.png')
    resultXP = cv2.matchTemplate(tempBaseFull, tempBase, cv2.TM_CCOEFF_NORMED)
    (min_x, max_y, minlocXP, maxlocXP) = cv2.minMaxLoc(resultXP)
    pyautogui.click(x=maxlocXP[0] + 283, y=maxlocXP[1] + 103)

    time.sleep(0.5)

    tempBaseFull = ImageGrab.grab(bbox=(280, 100, 1255, 970))
    tempBaseFull.save('/Users/' + pathImg + 'tempBaseFull.png')
    tempBaseFull = cv2.imread('/Users' + pathImg + 'tempBaseFull.png')
    tempBase = cv2.imread('/Users' + pathImg + 'tex.png')
    resultXP = cv2.matchTemplate(tempBaseFull, tempBase, cv2.TM_CCOEFF_NORMED)
    (min_x, max_y, minlocXP, maxlocXP) = cv2.minMaxLoc(resultXP)
    pyautogui.click(x=maxlocXP[0] + 283, y=maxlocXP[1] + 103)

    time.sleep(0.5)

    tempBaseFull = ImageGrab.grab(bbox=(280, 100, 1255, 970))
    tempBaseFull.save('/Users/' + pathImg + 'tempBaseFull.png')
    tempBaseFull = cv2.imread('/Users' + pathImg + 'tempBaseFull.png')
    tempBase = cv2.imread('/Users' + pathImg + 'bedMatros.png')
    resultXP = cv2.matchTemplate(tempBaseFull, tempBase, cv2.TM_CCOEFF_NORMED)
    (min_x, max_y, minlocXP, maxlocXP) = cv2.minMaxLoc(resultXP)
    pyautogui.moveTo(maxlocXP[0] + 283, maxlocXP[1] + 203)
    pyautogui.dragTo(500, 60, button='left')

    time.sleep(5)

    tempBaseFull = ImageGrab.grab(bbox=(280, 100, 1255, 970))
    tempBaseFull.save('/Users/' + pathImg + 'tempBaseFull.png')
    tempBaseFull = cv2.imread('/Users' + pathImg + 'tempBaseFull.png')
    tempBase = cv2.imread('/Users' + pathImg + 'buySaw.png')
    resultXP = cv2.matchTemplate(tempBaseFull, tempBase, cv2.TM_CCOEFF_NORMED)
    (min_x, max_y, minlocXP, maxlocXP) = cv2.minMaxLoc(resultXP)
    if max_y > 0.9:
        pyautogui.click(x=maxlocXP[0] + 283, y=maxlocXP[1] + 103)
    time.sleep(0.5)

    tempBaseFull = ImageGrab.grab(bbox=(280, 100, 1255, 970))
    tempBaseFull.save('/Users/' + pathImg + 'tempBaseFull.png')
    tempBaseFull = cv2.imread('/Users' + pathImg + 'tempBaseFull.png')
    tempBase = cv2.imread('/Users' + pathImg + 'slot.png')
    resultXP = cv2.matchTemplate(tempBaseFull, tempBase, cv2.TM_CCOEFF_NORMED)
    (min_x, max_y, minlocSlot, maxlocSlot) = cv2.minMaxLoc(resultXP)

    time.sleep(0.5)

    tempBaseFull = ImageGrab.grab(bbox=(280, 100, 1255, 970))
    tempBaseFull.save('/Users/' + pathImg + 'tempBaseFull.png')
    tempBaseFull = cv2.imread('/Users' + pathImg + 'tempBaseFull.png')
    tempBase = cv2.imread('/Users' + pathImg + 'newSaw.png')
    resultXP = cv2.matchTemplate(tempBaseFull, tempBase, cv2.TM_CCOEFF_NORMED)
    (min_x, max_y, minlocXP, maxlocXP) = cv2.minMaxLoc(resultXP)
    pyautogui.moveTo(maxlocXP[0] + 290, maxlocXP[1] + 110)
    pyautogui.dragTo(maxlocSlot[0] + 290, maxlocSlot[1] + 110, button='left')

    time.sleep(0.5)

    if fic % 3 == 0:
        tempBaseFull = ImageGrab.grab(bbox=(280, 100, 1255, 970))
        tempBaseFull.save('/Users/' + pathImg + 'tempBaseFull.png')
        tempBaseFull = cv2.imread('/Users' + pathImg + 'tempBaseFull.png')
        tempBase = cv2.imread('/Users' + pathImg + 'fic1.png')
        resultXP = cv2.matchTemplate(tempBaseFull, tempBase, cv2.TM_CCOEFF_NORMED)
        (min_x, max_y, minlocXP, maxlocXP) = cv2.minMaxLoc(resultXP)
        pyautogui.click(x=maxlocXP[0] + 283, y=maxlocXP[1] + 103)

        time.sleep(0.5)

        tempBaseFull = ImageGrab.grab(bbox=(280, 100, 1255, 970))
        tempBaseFull.save('/Users/' + pathImg + 'tempBaseFull.png')
        tempBaseFull = cv2.imread('/Users' + pathImg + 'tempBaseFull.png')
        tempBase = cv2.imread('/Users' + pathImg + 'nextContr.png')
        resultXP = cv2.matchTemplate(tempBaseFull, tempBase, cv2.TM_CCOEFF_NORMED)
        (min_x, max_y, minlocXP, maxlocXP) = cv2.minMaxLoc(resultXP)
        pyautogui.click(x=maxlocXP[0] + 283, y=maxlocXP[1] + 103)

        time.sleep(0.5)

        tempBaseFull = ImageGrab.grab(bbox=(280, 100, 1255, 970))
        tempBaseFull.save('/Users/' + pathImg + 'tempBaseFull.png')
        tempBaseFull = cv2.imread('/Users' + pathImg + 'tempBaseFull.png')
        tempBase = cv2.imread('/Users' + pathImg + 'dlMoney.png')
        resultXP = cv2.matchTemplate(tempBaseFull, tempBase, cv2.TM_CCOEFF_NORMED)
        (min_x, max_y, minlocXP, maxlocXP) = cv2.minMaxLoc(resultXP)
        pyautogui.click(x=maxlocXP[0] + 283, y=maxlocXP[1] + 103)

        time.sleep(0.5)

        tempBaseFull = ImageGrab.grab(bbox=(280, 100, 1255, 970))
        tempBaseFull.save('/Users/' + pathImg + 'tempBaseFull.png')
        tempBaseFull = cv2.imread('/Users' + pathImg + 'tempBaseFull.png')
        tempBase = cv2.imread('/Users' + pathImg + 'fic2.png')
        resultXP = cv2.matchTemplate(tempBaseFull, tempBase, cv2.TM_CCOEFF_NORMED)
        (min_x, max_y, minlocXP, maxlocXP) = cv2.minMaxLoc(resultXP)
        pyautogui.click(x=maxlocXP[0] + 283, y=maxlocXP[1] + 103)

        time.sleep(0.5)

        tempBaseFull = ImageGrab.grab(bbox=(280, 100, 1255, 970))
        tempBaseFull.save('/Users/' + pathImg + 'tempBaseFull.png')
        tempBaseFull = cv2.imread('/Users' + pathImg + 'tempBaseFull.png')
        tempBase = cv2.imread('/Users' + pathImg + 'nextContr.png')
        resultXP = cv2.matchTemplate(tempBaseFull, tempBase, cv2.TM_CCOEFF_NORMED)
        (min_x, max_y, minlocXP, maxlocXP) = cv2.minMaxLoc(resultXP)
        pyautogui.click(x=maxlocXP[0] + 283, y=maxlocXP[1] + 103)

        time.sleep(0.5)

        tempBaseFull = ImageGrab.grab(bbox=(280, 100, 1255, 970))
        tempBaseFull.save('/Users/' + pathImg + 'tempBaseFull.png')
        tempBaseFull = cv2.imread('/Users' + pathImg + 'tempBaseFull.png')
        tempBase = cv2.imread('/Users' + pathImg + 'dlMoney.png')
        resultXP = cv2.matchTemplate(tempBaseFull, tempBase, cv2.TM_CCOEFF_NORMED)
        (min_x, max_y, minlocXP, maxlocXP) = cv2.minMaxLoc(resultXP)
        pyautogui.click(x=maxlocXP[0] + 283, y=maxlocXP[1] + 103)
    updateK = 0

def checkKoord():
    global sky, treeCenter, pause, activ, saw, die, sawNum,ok
    activSaw = cv2.imread('/Users' + pathImg + 'activSaw.png')
    while whileFlag:
        if sky is True and activ == 1 and pause == 0:
            screen_btns = ImageGrab.grab(bbox=(1190, 380, 1300, 700))
            screen_btns.save('/Users' + pathImg + 'screen_btns.png')
            screen_btns = cv2.imread('/Users' + pathImg + 'screen_btns.png')
            resultS = cv2.matchTemplate(screen_btns, activSaw, cv2.TM_CCOEFF_NORMED)
            (min_xS, max_yS, minlocS, maxlocS) = cv2.minMaxLoc(resultS)
            if max_yS < 0.8 and ok == 1:
                print('пропал пила')
                ok = 0
                writeMe()
            if max_yS > 0.8 and ok == 0:
                print('нашлась')
                ok = 1
            if max_yS > 0.8 and ok == 1:
                if saw == 1:
                    if sawNum < 200:
                        pyautogui.press('5')
                        sawNum += 1
                        print(sawNum)
                        time.sleep(11)
        time.sleep(2)

pauseP = threading.Thread(target=paused, args=())
killP = threading.Thread(target=kill, args=())
lootP = threading.Thread(target=loot, args=())
calcP = threading.Thread(target=calc, args=())
checkTargetP = threading.Thread(target=checkTarget, args=())
checkKoordP = threading.Thread(target=checkKoord, args=())

# pauseP.start()
killP.start()
lootP.start()
# calcP.start()
checkTargetP.start()
checkKoordP.start()


while whileFlag:
    if sawNum == 0 and sky is False and full == 0 and die == 0:
        print('Летим с базы')
        goFromBase()
        time.sleep(3)
        pyautogui.press('num2')
        time.sleep(2)
        sky = True

    if stop == 1 and sawNum == 0 and sky is True and full == 0 and die == 0:
        print('На карте опасно, назад на базу')
        goBaseFromTonel()
        time.sleep(15)
        sky = False

    if stop == 0 and sawNum == 0 and sky is True and tree == 0 and treeCenter == 0 and full == 0 and die == 0:
        print('На карте всё ок, ищем дерево')
        goToTree()
        time.sleep(3)
        if tree == 0:
            print('Дерево не нашел, назад на базу')
            goBaseFromTonel()
            time.sleep(15)
            sky = False

    if stop == 0 and sawNum == 0 and sky is True and tree == 1 and treeCenter == 0 and full == 0 and die == 0:
        print('Дерево нашел, ищу центр')
        goCenterTree()
    if stop == 0 and sawNum == 0 and sky is True and tree == 1 and treeCenter == 1 and full == 0 and die == 0:
        print('start saw')
        pyautogui.press('num7')
        pyautogui.press('num9')
        activ = 1
        saw = 1
        time.sleep(3)

    if stop == 0 and sawNum == 200 and sky is True and tree == 1 and treeCenter == 1 and full == 0 and die == 0:
        print('end saw')
        saw = 0
        time.sleep(20)
        activ = 0
        full = 1
    if full == 1 or stop == 1 and die == 0:
        saw = 0
        time.sleep(15)
        activ = 0
        print('full')
        time.sleep(5)
        print('ищем тонель')
        goToTonelFromTree()
        tree = 0
        treeCenter = 0
        time.sleep(13)
        print('летим на базу')
        goBaseFromTonel()
        time.sleep(15)
        sky = False
        full = 0
        # time.sleep(15)
        print('перезарядка')
        update()
        time.sleep(1)
        print('END')
        sawNum = 0
        saw = 1
        stop = 0
    time.sleep(2)
