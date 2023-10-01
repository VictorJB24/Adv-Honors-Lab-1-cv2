
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
    return sum(lst) / len(lst)

def reject_outliers(data, m = 2.):
    #copied off online, no clue how it works
    data = np.array(data)
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else np.zeros(len(d))
    return data[s<m]

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

# Masks arm to prevent accidental sleeve detection
mask = np.zeros(image.shape[:2], dtype = "uint8")
(cX, cY) = (image.shape[1] // 2, image.shape[0] // 2)
cv2.rectangle(mask, (400, 400), (image.shape[1] - 400, image.shape[0] - 400), 255, -1)
cv2.rectangle(mask, (cX -75, cY + 250), (cX + 500, image.shape[0]), 0, -1)
image = cv2.cvtColor(cv2.bitwise_and(image, image, mask = mask), cv2.COLOR_BGR2GRAY)
#image = cv2.bitwise_and(image, image, mask = mask) # use this to skip BGR2GRAY (for testing)

# Threshold for only extremely high contrast areas (which will almost always be only nametag)
thresh = image.copy()
thresh[thresh > 240] = 255 # using manual threshold because it needs to be constant so it always only recognizes nametag
thresh[thresh < 255] = 0
thresh = cv2.bitwise_not(thresh)

canny = cv2.Canny(thresh, 30, 150)

# Parse contours for coordinates
(cnts, _) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print("# of coins: {}",format(len(cnts)))
xcoords = []
ycoords= []
for contour in cnts:
    for coordinate in contour.tolist():
        xcoords.append(int(coordinate[0][0]))
        ycoords.append(int(coordinate[0][1]))

# Cleaning up list
xcoords.sort()
ycoords.sort()
xcoords = reject_outliers(xcoords)
ycoords = reject_outliers(ycoords)

# Fix detection when multiple players on screen (separates list of coords for only first nametag detected)
xcoords = xcoords[:260]
ycoords = ycoords[:260] 

# For testing, display corners of nametag
canny = cv2.circle(image, (xcoords[len(xcoords) -1], ycoords[len(ycoords) -1]), 2, (255,0,0), 5) # Top right 
canny = cv2.circle(image, (xcoords[0], ycoords[0]), 2, (255,0,0), 5) # Top left 

# Adjusting y offset for cursor based on size (distance) of nametag
ydist = ycoords[len(ycoords) -1] - ycoords[0]
yoffset = ydist * 4

# Display full color version
#canny = cv2.circle(blurred, (int(avg(xcoords)), int(avg(ycoords))), 3, (0,255,0), 5) # Mean
print(len(xcoords))
canny = cv2.circle(image, (xcoords[len(xcoords) // 2], ycoords[len(ycoords) // 2] + yoffset), 5, (255,0,0), 5) # Median (slightly better)
cv2.imshow("canny", canny)

cursorCoords = (xcoords[len(xcoords) // 2], ycoords[len(ycoords) // 2] + yoffset) # For vic
cv2.waitKey(0)
