# Python code to find minimum area rectangle around the
# square, and display the angle and width/height

# References: Stack Overflow, GeeksForGeeks, OpenCV library

import numpy as np
import cv2

# Read image and convert to grayscale
img = cv2.imread('square.png', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('square.png', cv2.IMREAD_UNCHANGED)
img_height, img_width = img.shape

# Convert to binary image and invert
_, threshold = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY)
invert = (255 - threshold)

# Find contours in the inverted image
contours, _= cv2.findContours(invert.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Loop through contours
for cnt in contours:
    # Find min area rectangle for each contour found
    # Draw onto image
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(img2, [box], 0, (0, 0, 255), 2)

    # Get dimensions from min area rectangle
    (x, y), (width, height), angle = rect
   
    # Print important info onto image
    position = (int(img_width/2), int(img_height/2))
    text = 'Angle: ' + str(np.round(angle, 2)) + '\n' + 'Width: ' + str(np.round(width, 2)) + '\n' + 'Height: ' + str(np.round(height, 2))
    font_scale = 0.75
    color = (0, 0, 255)
    thickness = 2
    font = cv2.FONT_HERSHEY_SIMPLEX
    line_type = cv2.LINE_AA

    text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
    line_height = text_size[1] + 5
    x, y0 = position
    for i, line in enumerate(text.split('\n')):
        y = y0 + i * line_height
        cv2.putText(img2,
                    line,
                    (x, y),
                    font,
                    font_scale,
                    color,
                    thickness,
                    line_type)

# Resize image
imgRS = cv2.resize(img2, (398, 600)) 

# Show image
cv2.imshow("Image", imgRS)
cv2.waitKey(0)
cv2.destroyAllWindows()


