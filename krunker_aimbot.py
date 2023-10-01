
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
from nametag_detection import get_enemey_coords
from pynput.keyboard import Key, Listener

pyautogui.FAILSAFE = True

# need to declare global to avoid UnboundLocalError from on_press
global AUTO_AIM_ON
AUTO_AIM_ON = False

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

def on_press(key):
    try:
        if key.char == ('a'):
            print("autoaim", AUTO_AIM_ON)
            AUTO_AIM_ON = not AUTO_AIM_ON
    except AttributeError:
        return

def main():
    """
    if not args["coordinates"]:
        top, left, krunker_window_width, krunker_window_height = calc_coordinates()
    else:
        ...
    """
    screen_width, screen_height = pyautogui.size()
    bounding_box = {'top': 100, 'left': 0, 'width': screen_width, 'height': screen_height-100}

    with Listener(on_press=on_press) as listener:
        listener.join()

        while True:

            if AUTO_AIM_ON:
                scrt_img = screenshotter.grab(bounding_box)

                krunker_frame = np.array(scrt_img)
                # cv2.imshow('Krunker Window', krunker_frame)

                # Masks arm to prevent accidental sleeve detection
                mask = np.zeros(krunker_frame.shape[:2], dtype = "uint8")
                (cX, cY) = (krunker_frame.shape[1] // 2, krunker_frame.shape[0] // 2)
                cv2.rectangle(mask, (400, 400), (krunker_frame.shape[1] - 400, krunker_frame.shape[0] - 400), 255, -1)
                cv2.rectangle(mask, (cX -75, cY + 250), (cX + 500, krunker_frame.shape[0]), 0, -1)
                masked_image = cv2.bitwise_and(krunker_frame, krunker_frame, mask = mask)

                cursor_coords = get_enemey_coords(masked_image)

                if not cursor_coords:
                    continue

                # pyautogui.dragTo(cursor_coords[0], cursor_coords[1], duration=.001)  # drag mouse to XY
                pyautogui.tripleClick(x=cursor_coords[0], y=cursor_coords[1])


main()

if __name__ == "__main__":

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()

    if (cv2.waitKey(1) & 0xFF) == ord('p'):
        now = datetime.now().strftime("%H:%M:%S")
        cv2.imwrite(now+".jpg", np.array(sct_img))
