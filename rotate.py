from __future__ import absolute_import, division, print_function
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import numpy
import cv2

# from: http://stackoverflow.com/questions/19987039/inverse-perspective-transformation

def CreateTransformationMatrix():

    # Create a rotation matrix
    view_x1 = (view_x-90) * (numpy.pi / 180)
    view_y1 = (view_y-90) * (numpy.pi / 180)
    view_z1 = (view_z-90) * (numpy.pi / 180)
    R_array = numpy.array([view_x1, view_y1, view_z1])

    R, jacobian = cv2.Rodrigues(R_array)
    R[0][2] = 0
    R[1][2] = 0
    R[2][2] = 1

    #Create and combine with translation matrix
    Trans_Mat = numpy.array([[1, 0, -im_w/2],
                        [0, 1, -im_h/2],
                        [0, 0, 1]])

    R_T_Mat = numpy.dot(R, Trans_Mat)
    R_T_Mat[2][2] += im_h

    #Create and combine with camera matriview_x
    Intrinsic_Mat = numpy.array([[im_h, 0, im_w/2],
                           [0, im_h, im_h/2],
                           [0, 0, 1]])

    print(Intrinsic_Mat.__class__.__name__, Intrinsic_Mat.shape, R_T_Mat.__class__.__name__, R_T_Mat.shape)
    rotation_matrix = numpy.dot(Intrinsic_Mat, R_T_Mat)
    return rotation_matrix

def RotateAndDisplayImage():
    M_Transformation_Matrix = CreateTransformationMatrix()
    print("M_Transformation_Matrix", M_Transformation_Matrix)
    persp = cv2.warpPerspective(im, M_Transformation_Matrix, (im_w, im_h))

    cv2.imshow("Distorted", im)
    cv2.imshow("undistorted", persp)

def ResetX(pos):
    global view_x
    view_x = float(pos)
    RotateAndDisplayImage()

def ResetY(pos):
    global view_y
    view_y = float(pos)
    RotateAndDisplayImage()

def ResetZ(pos):
    global view_z
    view_z = float(pos)
    RotateAndDisplayImage()

fn = "garden-2040714_640.jpg"

view_x = view_y = view_z = float(90)
im = cv2.imread(fn)
im_h, im_w, im_ch_ct = im.shape
cv2.namedWindow("Distorted")
cv2.namedWindow("undistorted")
cv2.createTrackbar("X axis", "undistorted", int(view_x),180, ResetX)
cv2.createTrackbar("Y axis", "undistorted", int(view_y),180, ResetY)
cv2.createTrackbar("Z axis", "undistorted", int(view_z),180, ResetZ)

RotateAndDisplayImage()

cv2.waitKey(0) & 0xff
cv2.destroyWindow("Distorted")
cv2.destroyWindow("undistorted")
