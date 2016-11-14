"""
Functions for calculating the essential matrix (E), fundamental matrix (F), and 
the corresponding camera matrices from each.
"""
import numpy as np

def calculate_F(l_pts, r_pts):
    """
    Computes the Fundamental matrix F from matching points in left and right 
    images.
    """
    # compute A from interest points
    A = np.empty([len(l_pts), len(l_pts[0])])
    for l_pt, r_pt in zip(l_pts, r_pts):
        # 3x3 matrix
        tt = l_pt.T * r_pt
        
        # form the matrix for Aq = 0, where q is 9x1 the elements of F
        A.append([tt[1,:], tt[2,:], tt[3,:]])
    
    # compute F from A
    _, _, V = np.linalg.svd(A)
    F = V[:,9]
    F.reshape(3, 3)
    
    # pts1 = np.int32(l_pts)
    # pts2 = np.int32(r_pts)
    # F, mask = cv2.findFundamentalMat(pts1,pts2,cv2.FM_LMEDS)
    # 
    # # We select only inlier points
    # pts1 = pts1[mask.ravel()==1]
    # pts2 = pts2[mask.ravel()==1]
    return F

def fromE(E):
    """
    Computes the camera matrix P from the Essential matrix E
    """
    # initialize W and Z matrices
    W = np.array([
        [0, -1, 0],
        [1,  0, 0],
        [0,  0, 1]
        ])
    Z = np.array([
        [ 0, 1, 0],
        [-1, 0, 0],
        [ 0, 0 ,0]
        ])
    # compute svd of E
    U, S, V = np.linalg.svd(E)

    # solve for S, R, t
    S = U * Z * U.T
    R = U * W * V.T
    Ro = U * W.T * V.T
    t = U[:, 3]

    # 4 choices
    # P = [R t]
    # P = [R -t]
    P = [Ro, t]
    # P = [Ro -t]
    return P

def fromF(F):
    """
    Computes the camera matrix P from the Fundamental matrix F
    """
    # locate the epipoles from F
    _, _, V = np.linalg.svd(F)
    # V = V'
    e = V[:, 3]

    ex = np.cross(e.reshape(1, 3), np.eye(3, 3))
    exf = ex * F
    P = np.array([ exf, e ])
    return P
