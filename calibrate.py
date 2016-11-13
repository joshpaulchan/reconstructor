#!/usr/bin/env python3
"""
Calbrates a camera and finds its intrinsic parameters using
"""

# system packages
import numpy as np
import cv2

# user defined
from util import log

def intrinsic_matrix(ref_images):
    """
    Calibrates the intrinsic camera matrix.
    """
    # pylint: disable=no-member
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((7*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    
    for i, fname in enumerate(ref_images):
        log("[{}] {}".format(i, fname))
        img = cv2.imread(fname)
        img = cv2.resize(img, None, fx=0.25, fy=0.25)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        cv2.imshow(fname, gray)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, ( 7, 7 ), None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1,-1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (7, 7), corners2, ret)
            cv2.imshow('img', img)
            cv2.waitKey(500)
        else:
            log("Failed to find chessboard.")
    cv2.destroyAllWindows()
    
    ret, mtx, _, _, _ = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    return mtx

def main():
    """
    Test it
    """
    import glob
    
    images = glob.glob('images/board/*.JPG')
    ki = intrinsic_matrix(images)
    log(ki)

if __name__ == '__main__':
    main()
