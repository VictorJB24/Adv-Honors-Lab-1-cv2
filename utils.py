
"""
    Description:
    Authors:
    Date:
"""

import cv2
import argparse

def view_playback(vid_path: str = None, frames_list: list = None,
                 draw_coords: list = None) -> None:

    if vid_path:
        print("Reading from video path: ", vid_path)
        # reading the input
        cap = cv2.VideoCapture(vid_path)

        # iterator for draw_coords; need to use while loop for VideoCapture
        i = 0
        while(True):
            ret, frame = cap.read()
            if(ret):

                #if draw_coords
                # adding rectangle on each frame
                cv2.rectangle(frame, (100, 100), (500, 500), (0, 255, 0), 3)

                # writing the new frame in output
                output.write(frame)
                cv2.imshow("output", frame)
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    break

    cv2.destroyAllWindows()
    output.release()
    cap.release()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--coordinates",
                    nargs=2,
                    required = False,
                    help = "Manually set coordinates of Krunker window (top left, bottom right)",
                    metavar=('t_left', 'b_right')
                    )
    # possibly? ap.add_argument("-i", "--image", required = False, help = "Path to the image")
    ap.add_argument("-v", "--video", required = False, help = "Path to the video")
    args = vars(ap.parse_args())

    view_playback("krunker_test.mov")
