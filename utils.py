
"""
    Description: Utilities, useful functions to support krunker_aimbot.py
    Authors: Victor J. & Aiden A.
    Date: Fall 2023
"""

import cv2
import argparse
import time
import numpy as np
from nametag_detection import create_mask, get_enemey_coords

current_time = time.strftime("%H_%M_%S", time.localtime())

def view_playback(frames_list = None, video_path = None):
    if frames_list:
        for frame in frames_list:
            cv2.imshow(f"Video footage {current_time}", frame)
            cv2.waitKey(0)

    elif video_path:
        # reading the input
        cap = cv2.VideoCapture(video_path)

        while True:
            ret, frame = cap.read()
            if ret:
                cv2.imshow(f"Video footage from {video_path}", frame)

        cap.release()

    cv2.destroyAllWindows()

def create_debug_video(vid_path: str = None, frames_list: list = None):
    """
    Purpose
    Parameters

    """
    new_vid_path = "krunker_vid_debug_" + current_time + ".avi"

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_writer = cv2.VideoWriter(new_vid_path, fourcc, 20.0, (640, 480))

    cap = cv2.VideoCapture(vid_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    i = 0
    while i < 250:
        ret, frame = cap.read()
        if ret:
            masked_image = create_mask(frame)
            cursor_coords = get_enemey_coords(masked_image)
            person_identified_frame = cv2.circle(frame, cursor_coords, 5, (255,0,0), 5)

            print("frame ", i, "/", frame_count, " ", cursor_coords)
            i+=1
            output_writer.write(person_identified_frame)

    cap.release()
    output_writer.release()
    print("\n\nDONE!!! ", new_vid_path)
    return new_vid_path

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", required = True,
                   help = "Path to the krunker playback")
    args = vars(ap.parse_args())

    #new_vid_path = create_debug_video(vid_path=args["video"])
    #view_playback(vid_path=new_vid_path)
    view_playback(args["video"])
