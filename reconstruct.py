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
from matplotlib import pyplot as plt

# user-defined
from util import log
import calibrate
import ipt
import camera_matrix
import triangulate

def plot_3d(pts):
    """
    Generate a 3d plot of the given 3d points.
    
    @pre    : `pts` must be an array of 3-dimensional points
    @post   : a window with a plot of the point cloud will appear
    
    @param  : pts   : np.array[]    : array of 3-d points
    @return : none
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xs, ys, zs = zip(*pts)
    ax.scatter(xs, ys, zs, c='r', marker='o')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

def reconstruct(object_images, ref_images=None):
    """
    Attempts reconstruction of object.
    """
    ki = None
    cam_mat = None

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

    all_ip_kps, all_ip_desc, matching_ip = ipt.find_and_match_ip(object_images)
    
    # restrict things a bit
    all_ip = sorted(all_ip_kps)[:50]
    matching_ip = sorted(matching_ip)[:25]
    
    # log first 20 ip
    log(matching_ip[:20])

    ######################## 2. find camera matrice(s) ########################
    # find F (if ref images are given, find E)

    log(" image IP detection and matching ".center(80, '='))
    
    F = camera_matrix.calculate_F(all_ip[0], all_ip[1])
    cam_mat = camera_matrix.fromF(F)
    if ki is not None:
        # Find essential matrix
        E = ki.T @ F @ ki
        cam_mat = camera_matrix.fromE(E)
        
    ############################# 3. triangulation #############################
    # find the distance for ALL the image IPs to find object IPs
    
    if ki is None:
        all_ip = triangulate.from_ip(matching_ip, F=cam_mat)
    else:
        all_ip = triangulate.from_ip(matching_ip, E=cam_mat)

    ########################### 4. bundle adjustment ###########################
    # ayyyyy lmao

    # all_ip = all_ip

    ########################### 5. 3D reconstruction ###########################
    # Produce a sparse point cloud of the object and images
    plot_3d(all_ip)


def main():
    is_test = True
    obj_img_path = "images/object/*.JPG" if is_test else input("Enter the path to your object images.")
    ref_img_path = "images/board/*.JPG" if is_test else input("Enter the path to your board images.")
    
    obj_img = glob.glob(obj_img_path)
    ref_img = glob.glob(ref_img_path)
    reconstruct(obj_img, ref_img)

if __name__ == '__main__':
    main()
