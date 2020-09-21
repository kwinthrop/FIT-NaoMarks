# Python code to find minimum area rectangle around the
# square, and print the angle and width/height

# References: GeeksForGeeks and OpenCV library

import numpy as np
import cv2

# Read image and convert to grayscale
img = cv2.imread('square.png', cv2.IMREAD_GRAYSCALE)

# Converting to binary image
_, threshold = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY)

# Find contours in the image
contours, _= cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Loop through contours
for cnt in contours:
    # Find min area rectangle for each contour found
    # Then print important info
    rect = cv2.minAreaRect(cnt)
    (x, y), (width, height), angle = rect
    print(f'Angle: {angle:.3f} degrees')
    print(f'Width: {width:.3f}')
    print(f'Height: {height:.3f}')


