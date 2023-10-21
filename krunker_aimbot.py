
"""
    Description: Aimbot for Krunker.io using OpenCV; detection occurs in
    nametag_detection.py
    Authors: Victor J. & Aiden A.
    Date: Summer 2023
"""

import argparse
import numpy as np
import cv2
from mss import mss
from PIL import Image
from pynput import keyboard
from nametag_detection import create_mask, get_enemey_coords
from utils import create_debug_video, view_playback

try:
    import pydirectinput as pymouseutil # For Windows
except AttributeError:
    import pyautogui as pymouseutil     # For Mac

# able to slam cursor to top left and the script ends; prevents crazy cursor
pymouseutil.FAILSAFE = True

# need to be global so they can be accessed in on_release function; necessasry for pynput
AUTO_AIM_ON = False
DEBUG_VIDEO = False
DISPLAY_DEBUG = False
RUN_SCREEN_DETECTION = True

ap = argparse.ArgumentParser()
ap.add_argument("-w", "--window_set", required = False,
               help = "Set custom coordinates for screenshotter window",
               action="store_true") # no input is required for argument; just the flag
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
    """
    Purpose: Ability for user to set their own Krunker window coordinates
    Parameters: The bounding box for the screenshotter; the entire screen coords
    Returns: List of the custom krunker window dimensions
    """
    scrt_img = screenshotter.grab(scst_bounding_box)
    krunker_frame = np.array(scrt_img)

    masked_image = create_mask(krunker_frame)
    cv2.imshow('Masked Krunker Window', masked_image)
    cv2.waitKey(0)

    cv2.destroyAllWindows()

def main():
    #Automatically get screen size and set screenshot dimensions
    screen_width, screen_height = pymouseutil.size()
    screenshotter_bounding_box = {'top': 0, 'left': 0,
                                  'width': screen_width,
                                  'height': screen_height}
    
    # Coords for center of screen (used later)
    cX = screen_width // 2
    cY = screen_height // 2

    if args["window_set"]:
        # used to set the masking which our image detection will focus in on
        mask_dimensions = set_custom_window_coords(screenshotter_bounding_box)

    # saving all of the video frames here
    debug_frames = []

    print("\nPremiere Krunkie Aimbot v.1.0\n© 2023 Krunkie Plays Corp.\n\n")
    print("Usage:\n1. 'p' to toggle the detection\n2. 'v' to toggle the screen recording\
           \n3. 'm' to quit the program and watch playback if a recording was taken\
           \n\nAimbot is running...")
    
    while RUN_SCREEN_DETECTION:

        if AUTO_AIM_ON:
            scrt_img = screenshotter.grab(screenshotter_bounding_box)

            krunker_frame = np.array(scrt_img) # Convert image to numpy array
            masked_image = create_mask(krunker_frame) # Mask unecessary parts of screen
            cursor_coords = get_enemey_coords(masked_image)

            # debug video will only be saved if aimbot is on
            if DEBUG_VIDEO:
                # drawing blue circle on enemy; will work even if cursor_coords is None
                krunker_frame = cv2.circle(masked_image, cursor_coords, 5, (255,0,0), 5)

                # drawing green circle on current mouse position
                krunker_frame = cv2.circle(masked_image, pymouseutil.position(), 5, (0,255,0), 5)
                debug_frames.append(krunker_frame)

            if not cursor_coords: # No enemy detected
                # Release mouse (stop shooting) if no enemy detected
                pymouseutil.mouseUp()
            else: # enemy detected

                # Distance from center of screen to desired coordinates
                newX = cursor_coords[0] - cX
                newY = cursor_coords[1] - cY

                pymouseutil.mouseDown() # click mouse (start shooting)

                # Moves the center of the screen to the coordinates, thus aligning the crosshair
                # (at the center of the screen) with the enemy
                pymouseutil.move(newX, newY)


    if DISPLAY_DEBUG:
        print("\nLENGTH OF RECORDING: ", len(debug_frames))
        view_playback(frames_list=debug_frames)

if __name__ == "__main__":
    #view_playback(video_path="krunker_test.mov")
    main()
