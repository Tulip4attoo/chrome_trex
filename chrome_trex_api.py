# file nay xu ly cac file theo kieu hard code cac vi tri

import pyscreenshot as ImageGrab
import pyautogui
import time
import numpy as np
import cv2

from mss import mss, tools
from PIL import ImageOps, Image

#####
# SOME CONSTANTS
BLANK_BOX = 247000
GAMEOVER_RANGE = [620000, 660000]
TIME_BETWEEN_FRAMES = 0.01
TIME_BETWEEN_GAMES = 0.5



class Cordinates(object):
    """docstring for Cordinates"""
    # replay_pos = (390, 410)
    replay_pos = (520, 390)

def restart_game():
    pyautogui.click(Cordinates.replay_pos)

def press_up():
    pyautogui.keyDown("up") # press a key down
    time.sleep(0.02)
    # print("Jump")
    pyautogui.keyUp("up") # release a key

def check_catus():
    # cactus_box = {'left': 270, 'top': 420, 
    #               'width': 50, 'height': 20}
    cactus_box = {'left': 370, 'top': 400, 
                  'width': 50, 'height': 20}
    sct = mss()
    img = np.array(sct.grab(cactus_box))[:,:,:3]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray.sum()

def check_gameover(gameover_range = GAMEOVER_RANGE):
    result = False
    # gameover_box = {'left': 290, 'top': 360, 
    #               'width': 200, 'height': 15}
    gameover_box = {'left': 430, 'top': 345, 
                  'width': 200, 'height': 15}
    sct = mss()
    img = np.array(sct.grab(gameover_box))[:,:,:3]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    curr_state = gray.sum()
    if curr_state < GAMEOVER_RANGE[1] and curr_state > GAMEOVER_RANGE[0]:
        result = True
    return result

def main():
    while True:
        gameover_state = check_gameover()
        if gameover_state:
            time.sleep(TIME_BETWEEN_GAMES)
            print("Game over. Restart game")
            restart_game()
        cactus_state = check_catus()
        if cactus_state != BLANK_BOX:
            press_up()
        time.sleep(TIME_BETWEEN_FRAMES)

if __name__ == '__main__':
    main()
