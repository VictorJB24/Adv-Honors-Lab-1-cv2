
"""
    Description: ...
    Authors: Victor J. & Aiden A. that rhymes
    Date: Summer 2023
"""

import argparse
import numpy as np
import cv2
from mss import mss
from PIL import Image
from datetime import datetime
import pyautogui

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--coordinates",
                nargs=2,
                required = False,
                help = "Manually set coordinates of Krunker window (top left, bottom right)",
                metavar=('t_left', 'b_right')
                )
args = vars(ap.parse_args())

screenshotter = mss()

def calc_coordinates():
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
    if not args["coordinates"]:
        top, left, krunker_window_width, krunker_window_height = calc_coordinates()
    else:
        ...

    bounding_box = {'top': 100, 'left': 0, 'width': 400, 'height': 300}

    while True:
        sct_img = screenshotter.grab(bounding_box)
        cv2.imshow('Krunker Window', np.array(sct_img))

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break

        if (cv2.waitKey(1) & 0xFF) == ord('p'):
            now = datetime.now().strftime("%H:%M:%S")
            cv2.imwrite(now+".jpg", np.array(sct_img))

main()
