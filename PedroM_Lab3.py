#Pedro Meran
#Lab 3

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import cv2
import numpy as np
import argparse
import copy
import os
import mmap
import struct
from Tkinter import *

def window():
# Create an PyQT4 application object.
    a = QApplication(sys.argv)

# The QWidget widget is the base class of all user interface objects in PyQt4.
    w = QWidget()

# Set window size.
    w.resize(200, 200)

# Set window title
    w.setWindowTitle("Z POSITION")
    	
    w.lineoutput = QLabel(w)
    w.lineoutput.move(32, 80)
    w.lineoutput.resize(200,140)
	
# Add a button
    w.btn = QPushButton('CALCULATE', w)
    
  
    w.L_path = 'C:\Users\meran\Desktop\lab3\images\left5.jpg'
    
    w.R_path = 'C:\Users\meran\Desktop\lab3\images\left0.jpg'
    
    L_coords = FindCircle(w.L_path)
    R_coords = FindCircle(w.R_path)
    xLeft = L_coords[0][0]
    yLeft = L_coords[0][1]
    xRight = R_coords[0][0]
    yRight = R_coords[0][1]
    
    w.btn.clicked.connect(lambda: w.lineoutput.setText(zposition(xLeft,yLeft,xRight, yRight)))
    w.btn.resize(w.btn.sizeHint())
    w.btn.move(50, 50)
	
    w.show()
    sys.exit(a.exec_())

def FindCircle(path):

    img = cv2.imread(path)
    output = copy.copy(img) 

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # detect circles in the image
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)
    # ensure at least some circles were found
    
    if circles is not None:
	# convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        coords = []
	# loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
            coords.append([x,y])
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
        yNumPix = 480
        coords[0][1] = abs(yNumPix-coords[0][1])
        return(coords)
    
def zposition(xL, yL, xR, yR):
    xLeft = int(xL)
    yLeft = int(yL)
    xRight = int(xR)
    yRight = int(yR)
    b = 60
    f = 6
    ps = .006
    xNumPix = 752
    yNumPix = 480
    cxLeft = xNumPix/2
    cyLeft = yNumPix/2
    cxRight = xNumPix/2
    cyRight = yNumPix/2
    d = (abs((xLeft-cxLeft)-(xRight-cxRight))*ps) 
    Z = (b * f)/d 
    X = (Z*(xLeft-cxLeft)*ps)/f
    Y = (Z*(yLeft-cyLeft)*ps)/f
    
    xVal = "{:.2f}".format(X)
    yVal = "{:.2f}".format(Y)
    zVal = "{:.2f}".format(Z)
    
    return('X: ' + str(xVal)    + 'mm\nY: ' + str(yVal) + 'mm\nZ: ' + str(zVal) + 'mm')
	
if __name__ == '__main__':
    window()
    
   