
"""
    Description: Image detection using CV2 to actually detect the nametags, and,
    by proxy, the Krunker players themselves
    Authors: Victor J. & Aiden A.
    Date: Summer 2023
"""

import numpy as np
import argparse
import cv2

def get_enemey_coords(image):
    """
    Purpose: Return the coordinates of the found enemy, if there is one detected
    Parameters: The image where the detection needs to occur
    Returns: A tuple of the found coordinates; else, None
    """
    # Making the image greyscale allows for better contrast detection (not based on color)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold for only extremely high contrast areas (which will almost always be only nametag)
    thresh = image.copy()
    # using manual threshold because it needs to be constant so it always only recognizes nametag
    thresh[thresh > 240] = 255
    thresh[thresh < 255] = 0
    thresh = cv2.bitwise_not(thresh)

    canny = cv2.Canny(thresh, 30, 150) # Detects edges on high contrast image

    # Parse contours for coordinates
    (contours, _) = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Case for no enemy found (returns no location)
    if len(contours) < 1:
        return None

    coords = []
    # Get coordinates of left-most contour found
    for coordinate in contours[0].tolist():
        coords.append([int(coordinate[0][0]), int(coordinate[0][1])])

    # Adjusting y offset for cursor based on size of nametag, which automatically
    # adjusts based on the distance from the player to the nametag
    yoffset = (coords[len(coords) - 1][1] - coords[0][1]) * 2

    # Finding median of coords lists and adjust offset to go from nametag (the area actually detected) to acutal enemy
    medianCoords = coords[len(coords) // 2]
    cursor_coords = (medianCoords[0], medianCoords[1] + yoffset)

    return cursor_coords

def create_mask(frame, custom_coords = None):
    """
    Purpose: Returns masked image where mask covers everything that is not the krunker
    screen
    Parameters: The frame (image) to be masked, and an optional variable for custom
    masking coodinates
    Returns: The masked cv2 image
    """
    # Masks screen so this program only reads info from the game itself
    sideMask = np.zeros(frame.shape[:2], dtype = "uint8")

    # The numbers in else statement have been found through trial and error,
    # and remove all on the screen but a portion of the game window itself
    if custom_coords:
        rect_coords = custom_coords
        cv2.rectangle(sideMask, rect_coords[0], rect_coords[1], 255, -1)
    else:
        (cX, cY) = (frame.shape[1], frame.shape[0])
        rect_coords = [(cX//4, cY//5), (cX - cX//5, cY - cY//4)]
        cv2.rectangle(sideMask, (cX//4, cY//5), (cX - cX//5, cY - cY//4), 255, -1)

    masked_image = cv2.bitwise_and(frame, frame, mask = sideMask)

    return masked_image, rect_coords

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required = True, help = "Path to the image")
    args = vars(ap.parse_args())

    image = cv2.imread(args["image"])

    masked_image, _ = create_mask(image)
    enemy_coords = get_enemey_coords(masked_image)

    print("Player found at coords: ", enemy_coords)

    # For testing, display corners of nametag
    # image = cv2.circle(image, (xcoords[len(xcoords) -1], ycoords[len(ycoords) -1]), 2, (255,0,0), 5) # Top right
    # image = cv2.circle(image, (xcoords[0], ycoords[0]), 2, (255,0,0), 5) # Top left

    image = cv2.circle(image, enemy_coords, 5, (255,0,0), 20)
    cv2.imshow("Testing Player Detection...", image)

    cv2.waitKey(0)
