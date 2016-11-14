"""
Triangulates 2D image points to create 3D object/world points.
"""

import cv2
import numpy as np

def from_ip(ip, E=None, F=None):
    """
    Calculates the distance from cam center to each point in IP.
    """
    l_cam_mat = [np.eye(3, 3), np.zeros(1, 3)]
    if E:
        rx, ry, rz, _  = cv2.triangulatePoints(l_cam_mat, E, ip[0], ip[1])
    elif F:
        rx, ry, rz, _  = cv2.triangulatePoints(l_cam_mat, F, ip[0], ip[1])
    else:
        raise Exception("Need either E or F to triangulate distance.")
    return [rx, ry, rz]

def main():
    pass
    
if __name__ == '__main__':
    main()
