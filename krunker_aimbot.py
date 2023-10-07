
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
import pyautogui
from pynput import keyboard
from nametag_detection import create_mask, get_enemey_coords
from utils import create_debug_video, test_view_playback

# able to slam cursor to top left and the script ends; prevents crazy cursor
pyautogui.FAILSAFE = True

# need to be global so they can be accessed in on_release function; necessasry for pynput
AUTO_AIM_ON = False
DEBUG_VIDEO = False
DISPLAY_DEBUG = False
RUN_SCREEN_DETECTION = True

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

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--coordinates",
                nargs=2,
                required = False,
                help = "Manually set coordinates of Krunker window (top left, bottom right)",
                metavar=('t_left', 'b_right')
                )
args = vars(ap.parse_args())

screenshotter = mss()

listener = keyboard.Listener(on_release=on_release)
listener.start()

def calc_coordinates():
    """
    Purpose: To return a list of all the words found in the dictionary file
    Parameters: The dictionary file path
    Returns: List of correct words found in dictionary file
    """
    screen_width, screen_height = pyautogui.size()
    top = screen_height / 9
    left = screen_width / 5

    krunker_window_width = int(screen_width * .7)
    krunker_window_height = int(screen_height * .6)

    canvas = np.zeros((krunker_window_width, krunker_window_height, 3), dtype = "uint8")
    cv2.imshow("Canvas", canvas)
    cv2.waitKey(0)

    return top, left, krunker_window_width, krunker_window_height

def main():
    """
    if not args["coordinates"]:
        top, left, krunker_window_width, krunker_window_height = calc_coordinates()
    else:
        ...
    """
    screen_width, screen_height = pyautogui.size()
    bounding_box = {'top': 100, 'left': 0, 'width': screen_width, 'height': screen_height-100}

    debug_frames = []

    while RUN_SCREEN_DETECTION:

        if AUTO_AIM_ON:
            scrt_img = screenshotter.grab(bounding_box)

            krunker_frame = np.array(scrt_img)
            # cv2.imshow('Krunker Window', krunker_frame)

            masked_image = create_mask(krunker_frame)
            cursor_coords = get_enemey_coords(masked_image)

            if not cursor_coords:
                print("NO cursor coords found")
                continue

            pyautogui.tripleClick(x=cursor_coords[0], y=cursor_coords[1])

            """
            TODO
            FPS counter in top left, confidence interval counter top left
            confidence interval to calculate how confident the script is of it being a person
            Need above certain confidence interval threshold to actually fire
            """

            if DEBUG_VIDEO:
                print("saving krunker frame")
                krunker_frame = cv2.circle(krunker_frame, cursor_coords, 5, (255,0,0), 5)
                debug_frames.append(krunker_frame)

    if DISPLAY_DEBUG:
        print("LENGTH Of DEBUG: ", len(debug_frames))
        # create_debug_video(frames_list=debug_frames)
        test_view_playback(debug_frames)

if __name__ == "__main__":
    main()
