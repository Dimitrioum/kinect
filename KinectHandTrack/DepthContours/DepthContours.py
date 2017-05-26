"""
DepthContours module detects contours of hand, closer than ACTIVE_TRACKING_DISTANCE,
initializes dynamic variables with active contours characters
"""

import cv2
from KinectHandTrack.constants import ACTIVE_TRACKING_DISTANCE
import unittest


class DepthContours(object):

    """
    DepthContours class gets depth-frame from kinect and finds necessary contours:
    active contour - contour of hand, that is located closer, that ACTIVE_TRACKING_DISTANCE
    """

    def __init__(self, depth):
        _, self.depth_thresh = cv2.threshold(depth, ACTIVE_TRACKING_DISTANCE,
                                             255, cv2.THRESH_BINARY_INV)
        _, self.contours_list, _ = cv2.findContours(self.depth_thresh,
                                                    cv2.RETR_EXTERNAL,
                                                    cv2.CHAIN_APPROX_SIMPLE)
        self.active_contour_count = 0  # number of active contours
        self.centroids_list = []  # list of contours' centroids
        self.convex_hull_list = []  # list of contours' convexes
        self.active_contours_list = []  # contour of hand, located closer than
        self.convex_hull_area = []  # area of convex
        self.active_contour_area = []  # area of active contour

    def contours_extracting(self):

        """
        contours_extracting function analyses depth-frame contours, finds active contours
        :return: lists of active contours' main parts
        """

        while self.contours_list:
            for i in range(len(self.contours_list)):
                if abs(cv2.contourArea(self.contours_list[
                                           i])) > 2000:  # searching for contours, that are made up of more than 2000 pix
                    contour_area = cv2.contourArea(self.contours_list[i])
                    self.active_contour_area.append(contour_area)
                    moments = cv2.moments(self.contours_list[i])
                    moment10 = moments['m10']
                    moment00 = moments['m00']
                    moment01 = moments['m01']
                    centroid_x = int(moment10 / moment00)
                    centroid_y = int(moment01 / moment00)
                    self.centroids_list.append((centroid_x, centroid_y))
                    convex_hull = cv2.convexHull(self.centroids_list[i])
                    self.convex_hull_area.append(convex_hull)
                    self.convex_hull_list.append(list(convex_hull))
                    self.active_contours_list.append(self.contours_list[i])
                    self.active_contour_count += 1



