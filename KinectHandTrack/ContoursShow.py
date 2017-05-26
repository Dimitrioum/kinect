"""
ContoursShow module shows RGB-video and active contours
"""

from freenect import sync_get_video, sync_get_depth
import cv2
import numpy as np
from KinectHandTrack.DepthContours.DepthContours import DepthContours
from KinectHandTrack.constants import GREEN, YELLOW, PURPLE


def get_video():

    """
    Getting rgb-frames from kinect
    :return: rgb-frame
    """

    bgr_array, _ = sync_get_video()
    rgb_array = cv2.cvtColor(bgr_array, cv2.COLOR_BGR2RGB)
    return rgb_array


def get_depth():

    """
    Getting depth-frame from kinect
    :return: depth-frame
    """

    depth_array, _ = sync_get_depth()
    depth_array = depth_array.astype(np.uint8)
    return depth_array


def drawing_contours(rgb_frame, contours_instance):

    """
    :param rgb_frame: RGB-frame from kinect
    :param contours_instance: DrawContours class instance
    :return: RGB-frame with drawn contours
    """
    
    cv2.drawContours(rgb_frame, contours_instance.active_contours_list,
                     -1, GREEN, 2)

    for i in range(len(contours_instance.convex_hull_list)):
        cv2.drawContours(rgb_frame, contours_instance.convex_hull_list[i],
                         -1, YELLOW, 5)

    for i in range(len(contours_instance.centroids_list)):
        cv2.circle(rgb_frame, contours_instance.centroids_list[i],
                   10, PURPLE, 2)

    cv2.imshow('Frame Contours', rgb_frame)

if __name__ == '__main__':
    while True:
        kinect_frame = get_video()
        kinect_depth = get_depth()
        depth_contours = DepthContours(kinect_depth)

        try:
            drawing_contours(kinect_frame, depth_contours)
            del kinect_depth
            del kinect_frame
        except TypeError:
            cv2.imshow('Frame Contours', kinect_frame)
            del kinect_depth
            del kinect_frame
        finally:
            del kinect_depth
            del kinect_frame

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()