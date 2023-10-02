
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
import keyboard
from nametag_detection import get_enemey_coords
from utils import view_playback

pyautogui.FAILSAFE = True

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

    AUTO_AIM_ON = False
    DEBUG_VIDEO = False
    DISPLAY_DEBUG = False

    debug_frames = {}

    while True:

        key_event = keyboard.read_event(suppress=True)
        if key_event.event_type == keyboard.KEY_DOWN and key_event.name == 'o':
            AUTO_AIM_ON = not AUTO_AIM_ON
            print("Autoaim: ", AUTO_AIM_ON)

        elif key_event.event_type == keyboard.KEY_DOWN and key_event.name == 'b':
            DEBUG_VIDEO = not DEBUG_VIDEO
            DISPLAY_DEBUG = True
            print("Debugging: ", DEBUG_VIDEO)

        elif key_event.event_type == keyboard.KEY_DOWN and key_event.name == 'm':
            break

        print("here")
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
                print("NO cursor coords")
                continue

            # pyautogui.dragTo(cursor_coords[0], cursor_coords[1], duration=.001)  # drag mouse to XY
            pyautogui.tripleClick(x=cursor_coords[0], y=cursor_coords[1])

            if DEBUG_VIDEO:
                print("saving krunker frame")
                debug_frames.append(krunker_frame)


    if DISPLAY_DEBUG:
        if "p" in input("Enter p to watch playback: "):
            print("Press q to exit...")
            print("LENGTH Of DEBUG: ", len(debug_frames))
            view_playback(frames_list=debug_frames, draw_coords=)
            frame = cv2.circle(frame, cursor_coords, 5, (255,0,0), 5)

        accepted_inputs = ["yes", "y", "ye"]
        if input("Save video playback? y/N: ").lower() in accepted_inputs:
            # Define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*"MP4V")
            output_writer = cv2.VideoWriter("krunker_debug.mp4", fourcc, 30, (512,512))
            frame = cv2.circle(frame, cursor_coords, 5, (255,0,0), 5)
            output_writer.write(krunker_frame)

    output_writer.release()

    # Closes all the frames
    cv2.destroyAllWindows()


if __name__ == "__main__":

    main()

    """
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()

    if (cv2.waitKey(1) & 0xFF) == ord('p'):
        now = datetime.now().strftime("%H:%M:%S")
        cv2.imwrite(now+".jpg", np.array(sct_img))

    """
