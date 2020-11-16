from naoqi import ALProxy
from imutils import paths
from PIL import Image
import cv2
import math
import numpy as np
import time
import imutils

IP = "192.168.137.246"  # ROBOT IP
PORT = 9559
motionProxy = ALProxy("ALMotion", IP, PORT)

def getNaoImage(IP, PORT):
    camProxy = ALProxy("ALVideoDevice", IP, PORT)
    resolution = 2    # VGA
    colorSpace = 11   # RGB

    videoClient = camProxy.subscribe("python_client", resolution, colorSpace, 5)
    t0 = time.time()

    # Get a camera image.
    # image[6] contains the image data passed as an array of ASCII chars.
    naoImage = camProxy.getImageRemote(videoClient)

    t1 = time.time()

    # Time the image transfer.
    print "acquisition delay ", t1 - t0

    camProxy.unsubscribe(videoClient)

    # Now we work with the image returned and save it as a PNG  using ImageDraw
    # package.

    # Get the image size and pixel array.
    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    array = naoImage[6]

    # Create a PIL Image from our pixel array.
    im = Image.frombytes("RGB", (imageWidth, imageHeight), array)

    # Save the image.
    im.save("camImage.png", "PNG")

def shapeDetection() :
    img = cv2.imread('camImage.png')
    cv2.imshow('camImage.png', img)
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

def shapeDetection2():

    img = cv2.imread('camImage.png')
    cv2.imshow('camImage.png', img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(gray, (3, 3))

    thresh = cv2.adaptiveThreshold(gray_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 205, 1)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # ret,thr=cv2.threshold(img,210,255,cv2.THRESH_BINARY)
    # _, contours, _ = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #dictionary of all contours
    # contours = {}
    # #array of edges of polygon
    # approx = []
    for cnt in contours:
        # approx = cv2.approxPolyDP(contours[cnt],cv2.arcLength(contours[cnt],True)*0.02,True)
        # if(len(approx) == 3):
        #     x,y,w,h = cv2.boundingRect(contours[cnt])
        #     cv2.putText(frame,'TRI',(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)

        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        cv2.drawContours(img, [approx], 0, (0), 5)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        if len(approx) == 3:
            cv2.putText(img, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0))
        elif len(approx)== 4:
            x,y,w,h = cv2.boundingRect(approx)
            if w == h :
                cv2.putText(img, "SQUARE" ,(x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
            else:
                cv2.putText(img, "RECTANGLE" ,(x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
        elif len(approx)== 5:
            cv2.putText(img, "PENTAGON" ,(x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
        elif len(approx)== 6:
            cv2.putText(img, "HEXAGON" ,(x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
        elif len(approx)== 7:
            cv2.putText(img, "HEPTAGON" ,(x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
        elif len(approx)== 8:
            cv2.putText(img, "OCTAGON" ,(x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
        elif len(approx) == 10:
            cv2.putText(img, "STAR", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
    cv2.imwrite("result.png", img)


def calcTheLocate():
    img = cv2.imread('camImage.png')
    col = np.ones(640)
    row = np.ones(480)
    colsum = []
    rowsum = []
    x = 0
    xw = 0 # w:west
    xe = 0 # e:est
    y = 0
    yn = 0 #n:north
    ys = 0 #s:south
    for i in range(0, 480):
        product = np.dot(col, img[i][:])
        colsum.append(product)

    for i in range(0, 480):
        if (colsum[i] == max(colsum)):
            y = i
            val = max(colsum) / 255
            yn = i - val
            ys = i + val
            break
    for i in range(0, 640):
        product = np.dot(row, img[:, i])
        rowsum.append(product)
    for i in range(0, 640):
        if (rowsum[i] == max(rowsum)):
            x = i
            val = max(colsum) / 255
            xw = val - i
            xe = val + i
            break
    print("locate  x: ", x, xw, xe, "........ locate y :", y, yn, ys)

    return x, y

def getHeadAngle(IP, PORT):

    actuator = ["HeadYaw", "HeadPitch"]
    useSensor = False
    headAngle = motionProxy.getAngles(actuator, useSensor)

    return headAngle

def setHeadAngle(alpha, beta):
    # motionProxy = ALProxy("ALMotion", IP, PORT)
    motionProxy.setStiffnesses("Head", 1.0)
    maxSpeedFraction = 0.3
    names = ["HeadYaw", "HeadPitch"]
    angles = [alpha, beta]
    motionProxy.angleInterpolationWithSpeed(names, angles, maxSpeedFraction)

    motionProxy.setStiffnesses("Head", 0.0)

def getHeadPitchAngle(IP, PORT):
    # motionProxy = ALProxy("ALMotion",IP,PORT)
    actuator = "HeadPitch"
    useSensor = False
    headAngle = motionProxy.getAngles(actuator, useSensor)
    return headAngle

def getDistanse(x, y, cameraID):

    x = x - 320
    y = y - 240
    alpha = ((-x / 640) * 60.97) * math.pi / 180  # rads
    beta = ((y / 480) * 47.64) * math.pi / 180  # rads
    headAngle = getHeadAngle(IP, PORT)
    # alpha = alpha + headAngle[0]
    beta = beta + headAngle[1]

    print("alpha", alpha, "beta", beta)
    print("alpha", alpha / math.pi * 180, "beta", beta / math.pi * 180)

    setHeadAngle(alpha, beta)
    motionProxy.setStiffnesses("Head", 0.0)

    H = 495
    cameraAngle = 1.2 * math.pi / 180
    if cameraID == 0:
        H = 495
        cameraAngle = 1.2 * math.pi / 180
    elif cameraID == 1:
        H = 477.33
        cameraAngle = 39.7 * math.pi / 180

    h = H - 210 - 105 / 2
    headPitchAngle = getHeadPitchAngle(IP, PORT)
    # s = (h-100)/math.tan(cameraAngle + headPitchAngle[0])
    s = h / math.tan(cameraAngle + headPitchAngle[0])
    # s = h/math.tan(cameraAngle +beta)
    x = s * math.cos(alpha) / 1000
    y = s * math.sin(alpha) / 1000

    return x, y, alpha

if __name__ == '__main__':
    naoImage = getNaoImage(IP, PORT)
    shapeDetection()
    # shapeDetection2()
    # x,y=calcTheLocate()
    # getDistanse(410, 76, 0)

