
"""
    Description: Utilities, useful functions to support krunker_aimbot.py
    Authors: Victor J. & Aiden A.
    Date: Fall 2023
"""

import cv2
import argparse
from mss import mss
import time
import numpy as np
from nametag_detection import create_mask, get_enemey_coords

current_time = time.strftime("%H_%M_%S", time.localtime())
screenshotter = mss()

def view_playback(frames_list = None, video_path = None, debug = False):
    """
    Purpose: Plays back the cv2 video (frame-by-frame if debug is turned on)
    Parameters: A provided list of cv2 frames, the path to an existing video, and
    a bool indicating whether debug playback is on
    Returns: None
    """
    if frames_list:
        for frame in frames_list:
            cv2.imshow(f"Krunker playback", frame)
            if debug:
                cv2.waitKey(0)
            # q key to break
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    elif video_path:
        # reading the input
        cap = cv2.VideoCapture(video_path)

        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret:
                cv2.imshow(f"Video footage from {video_path}", frame)
                if debug:
                    cv2.waitKey(0)
            # q key to break
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        cap.release()

    cv2.destroyAllWindows()

def save_video(frames_list):
    """
    Purpose: Creates a .avi video from a provided list of frames
    Parameters: The list of cv2 frames
    Returns: The path of the new video
    """
    new_vid_path = "krunker_vid_debug_" + current_time + ".avi"

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_writer = cv2.VideoWriter(new_vid_path, fourcc, 20.0, (640, 480))

    for frame in frames_list:
        output_writer.write(frame)

    output_writer.release()
    return new_vid_path

def set_custom_mask_coords(scst_bounding_box):
    """
    Purpose: Ability for user to set their own Krunker window coordinates
    Parameters: The bounding box for the screenshotter; the entire screen coords
    Returns: List of the custom krunker window dimensions
    """
    new_coords = None
    while True:
        scrt_img = screenshotter.grab(scst_bounding_box)
        krunker_frame = np.array(scrt_img)

        masked_image, current_mask_coords = create_mask(krunker_frame, custom_coords=new_coords)
        print("\nCurrent mask coords:", current_mask_coords)

        cv2.imshow('Masked Krunker Window - Any Key to Exit', masked_image)
        cv2.waitKey(0)

        prompt = "Enter 4 new desired mask coords separated by spaces (ex. 12 24 "
        prompt += "200 54) corresponding to top left x, y then bottom right x, y; "
        prompt += "enter any letter to exit and save new coords: "
        inputted_coords = input(prompt)

        check_str = lambda string: any(char.isalpha() for char in string)
        if check_str(inputted_coords):
            if new_coords:
                with open('mask_coords.txt', 'w') as output:
                    output.write(str(new_coords))
                print(f"\nNew coords {new_coords} have been savec to file.")
            cv2.destroyAllWindows()
            return new_coords

        else:
            coords_list = inputted_coords.split()
            try:
                top_l_tuple = (int(coords_list[0]), int(coords_list[1]))
                bottom_r_tuple = (int(coords_list[2]), int(coords_list[3]))
                new_coords = [top_l_tuple, bottom_r_tuple]
            except:
                print("\n[ERROR] Four valid integers are required to set the new coordinates")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", required = True,
                   help = "Path to the krunker playback file (.avi, .mp4., etc)")
    args = vars(ap.parse_args())

    print(args["video"])
    view_playback(video_path=args["video"], debug=True)
