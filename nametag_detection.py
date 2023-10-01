
"""
    Description: ...
    Authors: Victor J. & Aiden A.
    Date: Summer 2023
"""

import numpy as np
import argparse
import cv2
import mahotas

def avg(lst):
    """
    Purpose: To return a list of all the words found in the dictionary file
    Parameters: The dictionary file path
    Returns: List of correct words found in dictionary file
    """
    return sum(lst) / len(lst)

def reject_outliers(data, m = 2.):
    """
    Purpose: To return a list of all the words found in the dictionary file
    Parameters: The dictionary file path
    Returns: List of correct words found in dictionary file
    """
    #copied off online, no clue how it works
    data = np.array(data)
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else np.zeros(len(d))
    return data[s<m]

def get_enemey_coords(image):
    """
    Purpose: To return a list of all the words found in the dictionary file
    Parameters: The dictionary file path
    Returns: List of correct words found in dictionary file
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #image = cv2.bitwise_and(image, image, mask = mask) # use this to skip BGR2GRAY (for testing)

    # Threshold for only extremely high contrast areas (which will almost always be only nametag)
    thresh = image.copy()
    thresh[thresh > 240] = 255 # using manual threshold because it needs to be constant so it always only recognizes nametag
    thresh[thresh < 255] = 0
    thresh = cv2.bitwise_not(thresh)

    canny = cv2.Canny(thresh, 30, 150)

    # Parse contours for coordinates
    (contours, _) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) < 1:
        return None

    xcoords = []
    ycoords = []
    for contour in contours:
        for coordinate in contour.tolist():
            xcoords.append(int(coordinate[0][0]))
            ycoords.append(int(coordinate[0][1]))

    # Cleaning up list
    xcoords.sort()
    ycoords.sort()
    xcoords = reject_outliers(xcoords)
    ycoords = reject_outliers(ycoords)

    # Fix detection when multiple players on screen (separates list of coords for only first nametag detected)
    # 260 is approximate (slightly arbitrary) list split value
    xcoords = xcoords[:260]
    ycoords = ycoords[:260]

    # Adjusting y offset for cursor based on size (distance) of nametag
    ydist = ycoords[len(ycoords) -1] - ycoords[0]
    yoffset = ydist * 2 # multiplying distance by 4 seemed to work to find the center of the player

    # Finding median of coords lists
    cursor_coords = (xcoords[len(xcoords) // 2], ycoords[len(ycoords) // 2] + yoffset)

    return cursor_coords

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required = True, help = "Path to the image")
    args = vars(ap.parse_args())

    image = cv2.imread(args["image"])

    # Masks arm to prevent accidental sleeve detection
    mask = np.zeros(image.shape[:2], dtype = "uint8")
    (cX, cY) = (image.shape[1] // 2, image.shape[0] // 2)
    cv2.rectangle(mask, (400, 400), (image.shape[1] - 400, image.shape[0] - 400), 255, -1)
    cv2.rectangle(mask, (cX -75, cY + 250), (cX + 500, image.shape[0]), 0, -1)
    masked_image = cv2.bitwise_and(image, image, mask = mask)

    cursor_coords = get_enemey_coords(masked_image)

    # For testing, display corners of nametag
    """
    image = cv2.circle(image, (xcoords[len(xcoords) -1], ycoords[len(ycoords) -1]), 2, (255,0,0), 5) # Top right
    image = cv2.circle(image, (xcoords[0], ycoords[0]), 2, (255,0,0), 5) # Top left
    """

    image = cv2.circle(image, cursor_coords, 5, (255,0,0), 5)
    cv2.imshow("Testing Player Detection...", image)

    cv2.waitKey(0)
