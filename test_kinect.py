# import the necessary modules
import freenect
import cv2
import numpy as np
from Xlib import X, display
import Xlib.XK
import Xlib.error
import Xlib.ext.xtest

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


class MouseControl:
    def __init__(self, depth):  # Constructor. BW is a binary image in the form of a numpy array
        _, self.depth_thresh = cv2.threshold(depth, 100, 255, cv2.THRESH_BINARY_INV)
        _, contours_list, _ = cv2.findContours(self.depth_thresh,
                                               cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)  # Finds the contours
        counter = 0
        """
        These are dynamic lists used to store variables
        """
        centroid = []
        cHull = []
        contours = []
        cHullArea = []
        contourArea = []
        while contours_list:  # Iterate through the CvSeq, cs.
            for i in range(len(contours_list)):
                if abs(cv2.contourArea(
                        contours_list[i])) > 2000:  # Filters out contours smaller than 2000 pixels in area
                    contourArea.append(
                        cv2.contourArea(contours_list[i]))  # Appends contourArea with newest contour area
                    moments = cv2.moments(contours_list[i])  # Finds all of the moments of the filtered contour
                    m10 = moments['m10']  # Spatial moment m10
                    m00 = moments['m00']  # Spatial moment m00
                    m01 = moments['m01']  # Spatial moment m01
                    centroid.append((int(m10 / m00), int(
                        m01 / m00)))  # Appends centroid list with newest coordinates of centroid of contour
                    convexHull = cv2.convexHull(contours_list[i])  # Finds the convex hull of cs in type CvSeq
                    cHullArea.append(cv2.contourArea(convexHull))  # Adds the area of the convex hull to cHullArea list
                    cHull.append(list(convexHull))  # Adds the list form of the convex hull to cHull list
                    contours.append(list(contours_list[i]))  # Adds the list form of the contour to contours list
                    counter += 1  # Adds to the counter to see how many blobs are there

        """
        Below the variables are made into fields for referencing later
        """
        self.centroid = centroid
        self.counter = counter
        self.cHull = cHull
        self.contours = contours
        self.cHullArea = cHullArea
        self.contourArea = contourArea


# function to get RGB image from kinect
def get_video():
    array, _ = freenect.sync_get_video()
    array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
    return array


d = display.Display()


# function to get depth image from kinect
def get_depth():
    array, _ = freenect.sync_get_depth()
    # np.clip(array, 0, 2**10-1, array)
    # array >>= 2
    array = array.astype(np.uint8)
    return array


def cacheAppendMean(cache, val):
    cache.append(val)
    del cache[0]
    return np.mean(cache)


def move_mouse(x, y):  # Moves the mouse to (x,y). x and y are ints
    s = d.screen()
    root = s.root
    root.warp_pointer(x, y)
    d.sync()


def click_down(button):  # Simulates a down click. Button is an int
    Xlib.ext.xtest.fake_input(d, X.ButtonPress, button)
    d.sync()


def click_up(button):  # Simulates a up click. Button is an int
    Xlib.ext.xtest.fake_input(d, X.ButtonRelease, button)
    d.sync()


constList = lambda length, val: [val for _ in range(length)]
if __name__ == "__main__":

    # screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
    while 1:
        contours = []
        contour = []
        centroid = []
        cHull = []
        cHullArea = []
        contourArea = []
        cHullAreaCache = constList(5, 12000)  # Blank cache list for convex hull area
        areaRatioCache = constList(5, 1)
        # screen.fill(BLACK)
        # get a frame from RGB camera
        frame = get_video()
        # get a frame from depth sensor
        depth = get_depth()

        # display RGB image
        # cv2.imshow('RGB image', frame)
        # display depth image
        _, depthThresh = cv2.threshold(depth, 30, 255, cv2.THRESH_BINARY_INV)
        # depthThresh = cv2.adaptiveThreshold(depth, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
        #                                     cv2.THRESH_BINARY, 11, 10)
        _, contours_list, _ = cv2.findContours(depthThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        try:
            for i in range(len(contours_list)):
                if abs(cv2.contourArea(contours_list[i])) > 2000:
                    contourArea.append(
                        cv2.contourArea(contours_list[i]))  # Filters out contours smaller than 2000 pixels in area
                    moments = cv2.moments(contours_list[i])  # Finds all of the moments of the filtered contour
                    m10 = moments['m10']  # Spatial moment m10
                    m00 = moments['m00']  # Spatial moment m00
                    m01 = moments['m01']  # Spatial moment m01
                    centroid.append((int(m10 / m00), int(
                        m01 / m00)))  # Appends centroid list with newest coordinates of centroid of contour
                    convexHull = cv2.convexHull(contours_list[i])  # Finds the convex hull of cs in type CvSeq
                    cHullArea.append(cv2.contourArea(convexHull))
                    cHull.append(list(convexHull))  # Adds the list form of the convex hull to cHull list
                    contours.append(list(contours_list[i]))
            cv2.drawContours(frame, contours, -1, GREEN, 2)
            # print(type(cHull), type(cHull[0]))
            for i in range(len(cHull)):
                cv2.drawContours(frame, cHull[i], -1, YELLOW, 5)
            for i in range(len(centroid)):
                cv2.circle(frame, centroid[i], 10, PURPLE, 2)
        except:
            for i in range(len(cHull)):
                cv2.drawContours(frame, cHull[i], -1, GREEN, 2)
            for i in range(len(centroid)):
                cv2.circle(frame, centroid[i], 10, PURPLE, 2)
            cv2.drawContours(frame, contours_list, -1, RED, 2)
        dummy = True
        print(centroid)
        try:
            centroidX = centroid[0][0]
            centroidY = centroid[0][1]
            strX = centroidX  # Makes the new starting X of mouse to current X of newest centroid
            strY = centroidY
            if dummy:
                mousePtr = display.Display().screen().root.query_pointer()._data  # Gets current mouse attributes
                dX = centroidX - centroid[0][0]  # Finds the change in X
                dY = centroid[0][1] - centroidY  # Finds the change in Y
                # # if abs(dX) > 1 & abs(dY):  # If there was a change in X greater than 1...
                mouseX = mousePtr["root_x"] - 2 * dX  # New X coordinate of mouse
                mouseY = mousePtr["root_y"] - 2 * dY  # New Y coordinate of mouse
                move_mouse(centroidX, centroidY)  # Moves mouse to new location
                # strX = centroidX  # Makes the new starting X of mouse to current X of newest centroid
                # strY = centroidY  # Makes the new starting Y of mouse to current Y of newest centroid
                cArea = cacheAppendMean(cHullAreaCache,
                                        cHullArea[0])  # Normalizes (gets rid of noise) in the convex hull area
                areaRatio = cacheAppendMean(areaRatioCache, contourArea[
                    0] / cArea)  # Normalizes the ratio between the contour area and convex hull area
                if cArea < 5000 and areaRatio > 0.82:  # Defines what a click down is. Area must be small and the hand must look like a binary circle (nearly)
                    click_down(1)
                else:
                    click_up(1)
            else:
                strX = centroidX  # Initializes the starting X
                strY = centroidY  # Initializes the starting Y
                dummy = True  # Lets the function continue to the first part of the if statement
        except:
            dummy = False  # Waits for a new starting point

        # for i in range(MouseControl.counter):
        #     cv2.circle(frame, MouseControl.centroid[i], 10, BLUE)
        #     cv2.drawContours(frame, MouseControl.cHull, -1, (255, 0, 0), 2)
        #     cv2.drawContours(frame, MouseControl.contours[i], -1, (0, 0, 255), 2)

        cv2.imshow('Depth image', frame)
        del depth
        del frame

        # quit program when 'esc' key is pressed
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()
