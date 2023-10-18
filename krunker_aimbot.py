
"""
    Description: Aimbot for Krunker.io using OpenCV; detection occurs in
    nametag_detection.py
    Authors: Victor J. & Aiden A. that rhymes
    Date: Summer 2023
"""

import argparse
import numpy as np
import cv2
from mss import mss
from PIL import Image
from pynput import keyboard
from nametag_detection import create_mask, get_enemey_coords
from utils import create_debug_video, test_view_playback
import time

try:
    import pydirectinput
except AttributeError:
    import pyautogui

# able to slam cursor to top left and the script ends; prevents crazy cursor
pyautogui.FAILSAFE = True

# need to be global so they can be accessed in on_release function; necessasry for pynput
AUTO_AIM_ON = False
DEBUG_VIDEO = False
DISPLAY_DEBUG = False
RUN_SCREEN_DETECTION = True

ap = argparse.ArgumentParser()
ap.add_argument("-w", "--window_set", required = False,
               help = "Set custom coordinates for screenshotter window")
args = vars(ap.parse_args())

screenshotter = mss()

# needs to be defined up here for keyboard.Listener(on_release)
def on_release(key):
    key = str(key).strip("'")

    if key == 'p':
        global AUTO_AIM_ON
        AUTO_AIM_ON = not AUTO_AIM_ON
        print("Autoaim state: ", AUTO_AIM_ON)

    if key == 'v':
        global DEBUG_VIDEO
        global DISPLAY_DEBUG

        DEBUG_VIDEO = not DEBUG_VIDEO
        DISPLAY_DEBUG = True
        print("Debug video state: ", DEBUG_VIDEO)

    if key == 'm':
        global RUN_SCREEN_DETECTION
        RUN_SCREEN_DETECTION = False

    return

listener = keyboard.Listener(on_release=on_release)
listener.start()

def set_custom_window_coords(scst_bounding_box):
    scrt_img = screenshotter.grab(scst_bounding_box)
    krunker_frame = np.array(scrt_img)

    masked_image = create_mask(krunker_frame)
    cv2.imshow('Masked Krunker Window', masked_image)
    cv2.waitKey(0)

def main():
    screen_width, screen_height = pyautogui.size()
    print("Screen width: ", screen_width)
    print("Screen height: ", screen_height)
    screenshotter_bounding_box = {'top': 0, 'left': 0,
                                  'width': screen_width,
                                  'height': screen_height}


    if args["window_set"]:
        # used to set the masking which our image detection will focus in on
        # mask_top, mask_left, mask_width, mask_height = set_custom_window_coords(screenshotter_bounding_box)
        set_custom_window_coords(screenshotter_bounding_box)

    print(screen_width, " ", screen_height)

    debug_frames = []

    while RUN_SCREEN_DETECTION:

        if AUTO_AIM_ON:
            scrt_img = screenshotter.grab(screenshotter_bounding_box)

            krunker_frame = np.array(scrt_img)
            # cv2.imshow('Krunker Window', krunker_frame)

            masked_image = create_mask(krunker_frame)
            cursor_coords = get_enemey_coords(masked_image)

            if DEBUG_VIDEO:
                #print("saving krunker frame")
                krunker_frame = cv2.circle(masked_image, cursor_coords, 5, (255,0,0), 5)
                krunker_frame = cv2.circle(masked_image, pyautogui.position(), 5, (0,255,0), 5)
                debug_frames.append(krunker_frame)

            if not cursor_coords:
                print("NO cursor coords found")
                # pyautogui.mouseUp()
                continue

            cX = masked_image.shape[1] // 2
            cY = masked_image.shape[0] // 2

            newX = cursor_coords[0] - cX
            newY = cursor_coords[1] - pcY
            pyautogui.moveTo(newX, newY)

            # divide by two because krunker_frame is scaled to twice the pydirectinput
            # coordinates
            # pydirectinput.mouseDown()

            #pydirectinput.move(abs(cX//2 - cursor_coords[0]//2), abs(cY//2 - cursor_coords[1]//2))
            """
            newX = cursor_coords[0] - cX
            newY = cursor_coords[1] - cY
            pydirectinput.move(newX, newY)
            #pydirectinput.moveTo(cursor_coords[0], cursor_coords[1])
            #print("X: {} Y: {}".format(cursor_coords[0], cursor_coords[1]))
            #print(pyautogui.position())
            """

            """
            TODO
            FPS counter in top left, confidence interval counter top left
            confidence interval to calculate how confident the script is of it being a person
            Need above certain confidence interval threshold to actually fire
            """

    if DISPLAY_DEBUG:
        print("LENGTH Of DEBUG: ", len(debug_frames))
        # create_debug_video(frames_list=debug_frames)
        test_view_playback(debug_frames)

if __name__ == "__main__":
    main()
