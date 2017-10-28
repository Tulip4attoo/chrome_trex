import pyscreenshot as ImageGrab
import pyautogui
import time
import numpy as np
import cv2
import os

import chrome_trex_api
import trex_nn

from mss import mss, tools
from PIL import ImageOps, Image



def find_game_position(sct, threshold):
    dino_template = cv2.imread(os.path.join('templates', 'dino.png'), 0)
    w, h = dino_template.shape[::-1]
    landscape_template = cv2.imread(os.path.join('templates', 'dino_landscape.png'), 0)
    lw, lh = landscape_template.shape[::-1]

    landscape = {}
    # mac dinh la se hien thi o screenshot 1, du chung ta co 1 hay nhieu man hinh
    monitor = sct.monitors[1]
    image = np.array(sct.grab(monitor))[:,:,:3]
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray_image, dino_template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    if len(loc[0]):
        pt = next(iter(zip(*loc[::-1])))
        landscape = dict(monitor, height=lh, left=pt[0], top=pt[1] - lh + h, width=lw)
    return landscape

def get_game_landscape_and_set_focus_or_die(sct, threshold=0.7):
    landscape = find_game_position(sct, threshold)
    if not landscape:
        print("Can't find the game!")
        exit(1)
    pyautogui.click(landscape["left"], landscape['top'] + landscape['height'])
    return landscape

def compute_region_of_interest(landscape):
    # tu thong tin ve landscape, ta lay ra duoc 1 vung chua day du cac vat the can
    # xem xet, nhung lai nho hon landscape (do do giam duoc khoi luong tinh toan)
    ground_height = 12
    y1 = landscape['height'] - 44
    y2 = landscape['height'] - ground_height
    x1 = 44 + 24
    x2 = landscape['width'] - 1
    return x1, x2, y1, y2

def reset_game():
    pyautogui.hotkey('ctrl', 'r')
    time.sleep(1)

def start_game():
    pyautogui.press('space')
    time.sleep(1.5)

def compute_distance_and_size(roi, max_distance):
    """
    minh chi check vung region_of_interest thoi
    vung nay chi co xuong rong --> co mau la thi` minh se biet do la co 
    xuong rong. Lay vung do thoi.
    Doan nay hard code de co size.
    Khong hay lam, nhung cung chap nhan duoc
    """
    obstacle_found = False
    distance = max_distance
    roi_mean_color = np.floor(roi.mean())
    last_column = distance
    for column in np.unique(np.where(roi < roi_mean_color)[1]):
        if not obstacle_found:
            distance = column
            obstacle_found = True
        elif column > last_column + 4:
            break
        last_column = column
    return distance, last_column - distance


def compute_speed(distance_array, last_distance, last_speed, loop_time, max_speed_step = 15):
    """
    tinh dua theo ca quang duong va thoi gian no di tren ca quang duong day
    boi vi co vai lag nen doi khi speed se bi noi ra rat rong, nen ta can co
    1 max_speed_step de gioi han
    """
    speed = (distance_array[0] - last_distance) / loop_time
    return max(min(speed, last_speed + max_speed_step), last_speed - max_speed_step)

BLANK_BOX = 247000
GAMEOVER_RANGE = [630000, 650000]
TIME_BETWEEN_FRAMES = 0.01
TIME_BETWEEN_GAMES = 0.5

MAX_SPEED_STEP = 15
INIT_SPEED = 270
N_X = 3
N_H = 3
N_Y = 1



def play_game(parameters_set):
    with mss() as sct:
        chrome_trex_api.restart_game()
        time.sleep(0.5)
        landscape = get_game_landscape_and_set_focus_or_die(sct, .8)

        gameover_template = cv2.imread(os.path.join('templates', 'dino_gameover.png'), 0)
        last_distance = landscape['width']
        x1, x2, y1, y2 = compute_region_of_interest(landscape)
        speed = INIT_SPEED
        start_time = None
        distance_array = []
        count_cactus = 0

        while True:
            image = np.array(sct.grab(landscape))[:,:,:3]
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray_image += np.abs(247 - gray_image[0, x2])
            roi = gray_image[y1:y2, x1:x2] # roi la tam anh region_of_interest thoi
            distance, size = compute_distance_and_size(roi, x2)
            input_set = [distance, speed, size]
            trex_nn.wrap_model(input_set, parameters_set, N_X)
            if distance == x2:
                continue
            elif distance < 40 or distance > last_distance: # co the thay bang so khac, tuy nhien ko qua can thiet hehe
                if len(distance_array):
                    end_time = time.time()
                    if start_time:
                        loop_time = end_time - start_time
                        speed = compute_speed(distance_array, distance, 
                            speed, loop_time, max_speed_step = MAX_SPEED_STEP)
                    start_time = time.time()
                    count_cactus += 1
                    print(count_cactus)
                distance_array = []
            else:
                distance_array.append(distance)
            gameover_state = chrome_trex_api.check_gameover()
            if gameover_state:
                print("Game over. Restart game")
                return count_cactus
            last_distance = distance
            time.sleep(TIME_BETWEEN_FRAMES)
