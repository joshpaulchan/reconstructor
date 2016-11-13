#!/usr/bin/env python3
"""
Reconstructs an object digitally by matching interest points across object
images, deriving camera matrices, and triangulating the points.

Uses OpenCV3 + Python3
Written by Josh Paul A. Chan

@pre    : `object_images` must be the path to the folder of object images
@pre    : `ref_images`, if given, must be the path to the folder of
        checkedboard images
@post   : reconstruction will be attempted
@post   : [success] 3d sparse point cloud will be displayed

@param  : object_images : str   : path to images of object to reconstruct
@param  : ref_images    : str   : path to images of checkedboard for ref
@return : str   : displays a window of a 3d sparse point cloud of the object
"""

# system packages
import glob
import numpy as np

# user-defined
from util import log
import calibrate
import ipt
import triangulate

def reconstruct(object_images, ref_images=None):
    """
    Attempts reconstruction of object.
    """
    ki = None
    cam_matrix = None

    ########################## 0. camera calibration ##########################
    # if ref images are given, calibrate camera and find intrinsic matrices

    if ref_images is not None:
        log(" camera calibration ".center(80, '='))
        # calculate instrinsic
        ki = calibrate.intrinsic_matrix(object_images)
        # show output
        log(ki)

    #################### 1. image IP detection and matching ####################
    # detect image IPs (via SIFT) -> a set wll ALL IPs and a set with matching
    # IPs over the images

    log(" image IP detection and matching ".center(80, '='))

    # all_ip, matching_ip = ipt.find_and_match(object_images)
    # log first 20 ip
    # log(matching_ip[:20])

    ######################## 2. find camera matrice(s) ########################
    # find F (if ref images are given, find E)

    log(" image IP detection and matching ".center(80, '='))
    #
    # cam_matrix = F = svd(ip)
    # if ki is not None:
    #     cam_matrix = E = ki.transpose * F * ki

    ############################# 3. triangulation #############################
    # find the distance for ALL the image IPs to find object IPs

    # all_ip = triangulate.interest_points(matching_ip)

    ########################### 4. bundle adjustment ###########################
    # lmao

    # all_ip = all_ip

    ########################### 5. 3D reconstruction ###########################
    # Produce a sparse point cloud of the object and images


def main():
    obj_img_path = 'images/object/*.JPG' if True else input("Enter the path to your object images.")
    ref_img_path = 'images/board/*.JPG' if True else input("Enter the path to your board images.")
    
    obj_img = glob.glob(obj_img_path)
    ref_img = glob.glob(ref_img_path)
    reconstruct(obj_img, ref_img)

if __name__ == '__main__':
    main()
