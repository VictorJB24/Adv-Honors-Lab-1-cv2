
"""
    Description: ...
    Authors: Victor J. & Aiden A. that rhymes
    Date: Summer 2023
"""

import numpy as np
import cv2
from mss import mss
from PIL import Image
from datetime import datetime

bounding_box = {'top': 100, 'left': 0, 'width': 400, 'height': 300}

screenshotter = mss()

while True:
    sct_img = screenshotter.grab(bounding_box)
    cv2.imshow('Krunker Window', np.array(sct_img))

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break

    if (cv2.waitKey(1) & 0xFF) == ord('p'):
        now = datetime.now().strftime("%H:%M:%S")
        cv2.imwrite(now+".jpg", np.array(sct_img))

def dimensions_check():
    pass
    # argparse numbers to check the screen's dimensions, display red box around i
    # lets user adjust their screen size
