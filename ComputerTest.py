import cv2
import numpy as np

# This is program is based off of the code used to demo the robot
# Its purpose is to allow testing with laptop camera to compare results
# to Nao robot demo

def shapeDetection() :
    img = cv2.imread('capture.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(gray, (3, 3))

    # Apply Hough transform on the blurred image.(change peremeter when the distance changes)
    detected_circles = cv2.HoughCircles(gray_blurred,cv2.HOUGH_GRADIENT, 0.1, 500, param1 = 70,param2 = 30, minRadius = 1, maxRadius = 175)

    # Draw circles that are detected.
    if detected_circles is not None:

        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            # Draw the circumference of the circle.
            cv2.circle(img, (a, b), r, (0, 255, 0), 2)
            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
    print(detected_circles)
    cv2.imwrite('shapeDetection.png', img)

def main():
    capture = cv2.VideoCapture(0)

    while True:
        _, frame = capture.read()
        cv2.imshow('frame', frame)
        cv2.imwrite("capture.png", frame)
        shapeDetection()
        # Press q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()



