# -*- coding: utf-8 -*-
import cv2
from freenect import sync_get_depth
from freenect import sync_get_video
import numpy as np


def get_video():
    array, _ = sync_get_video()
    array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
    return array


def get_depth():
    array, _ = sync_get_depth()
    array = array.astype(np.uint8)
    return array

if __name__ == '__main__':
    while 1:
        depth = get_depth()
        _, depthThresh = cv2.threshold(depth, 100, 255, cv2.THRESH_MASK)
        cv2.imshow('depththresh', depthThresh)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()