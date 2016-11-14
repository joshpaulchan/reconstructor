#!/usr/bin/env python3
"""
Finds, detects, and matches interest points.
"""
import cv2

from util import log

sift = cv2.xfeatures2d.SIFT_create() # pylint: disable=no-member
bf = cv2.BFMatcher() # pylint: disable=no-member

############################ FINDING AND DETECTION ############################

def _find_ip_via_sift_(img_names):
    # pylint: disable=no-member
    """
    Finds the interest points (IP) of the given images.
    
    @pre  : `img_names` must be an iterable of all the image names
    
    @param  : img_names : iterable  : iterable of all the file names
    @return : kps       : list of keypoint coordinates (for each image)
    @return : ip_des    : list of ip descriptors for every image
    """
    kps = []
    ip_des = []
    for i, fname in enumerate(img_names):
        log("[{}] {}".format(i, fname))
        img = cv2.imread(fname)
        img = cv2.resize(img, None, fx=0.25, fy=0.25)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        img_kps, img_kp_des = sift.detectAndCompute(img, None)
        kps.append(img_kps)
        ip_des.append(img_kp_des)
        
        # show image with keypoints
        # img = cv2.drawKeypoints(img, img_kps, img)
        # cv2.imshow('sift_' + fname, img)
        # cv2.waitKey(500)
    # cv2.destroyAllWindows()
    return kps, ip_des
    
def find_ip(images, method=None):
    """
    Wrapper for finding the interest points in an image.
    """
    if method is None or method == "SIFT":
        return _find_ip_via_sift_(images)

def find_and_match_ip(images, method=None):
    """
    Uses
    """
    all_ip_kp, all_ip_des = find_ip(images, method)
    return all_ip_kp, all_ip_des, match_ip(all_ip_des)

################################### MATCHING ###################################

def _match_ip_via_BF(ip_des):
    """
    Matches IP (follows an IP through the frames) using a B
    
    @param  : ip_des    : iterable  : list of lists of the ip_descriptors in 
    each image
    @return : list      : 
    """
    good = []
    
    first_image_ip_descriptors = ip_des[0]
    
    for ip_descriptors in ip_des[1:]:
        matches = bf.knnMatch(first_image_ip_descriptors, ip_descriptors, k=2)
        
        # Apply ratio test
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append([m])
    
    return good

def _match_ip_via_FLANN_(matches):
    good = []
    pts1 = []
    pts2 = []

    # ratio test as per Lowe's paper
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.8*n.distance:
            good.append(m)
            pts2.append(kp2[m.trainIdx].pt)
            pts1.append(kp1[m.queryIdx].pt)

def match_ip(ips):
    pass

def main():
    # pylint: disable=no-member
    """
    Test ipt
    """
    import glob
    from matplotlib import pyplot as plt
    
    images = glob.glob("images/object/*.JPG")[:10]
    all_ip_kps, all_ip_des = find_ip(images)
    matching_ip = match_ip(all_ip_des)
    
    im0 = cv2.imread(images[0])
    im1 = cv2.imread(images[1])
   
    # cv2.drawMatchesKnn expects list of lists as matches
    img3 = cv2.drawMatchesKnn(
        im0,
        all_ip_kps[0],
        im1,
        all_ip_kps[1],
        matching_ip[:10],
        None,
        flags=2)
    
    plt.imshow(img3)
    plt.show()
    
    cv2.waitkeyPress()

if __name__ == '__main__':
    main()
