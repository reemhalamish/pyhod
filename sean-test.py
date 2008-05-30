#!/usr/bin/python

import sys
from opencv import cv
from opencv import highgui
from math import *



iwidth = 320
iheight = 240 

hmin = 4 
hmax = 18 
red_hmin = 130
red_hmax = 180
green_hmin = 55
green_hmax = 100

vmin = 150
vmax = 255 
#smin = 147 
#smax = 255

stats = 1


hsv_min = cv.cvScalar(0, 0, vmin, 0)
hsv_max = cv.cvScalar(180, 255, vmax, 0)

capture = None

def change_hmin(p):
	global hmin
	hmin = p

def change_hmax(p):
	global hmax
	hmax = p

def change_red_hmin(p):
	global red_hmin
	red_hmin = p

def change_red_hmax(p):
	global red_hmax
	red_hmax = p

def change_green_hmin(p):
	global green_hmin
	green_hmin = p

def change_green_hmax(p):
	global green_hmax
	green_hmax = p

#def change_smin(p):
#	global smin
#	smin = p

#def change_smax(p):
#	global smax
#	smax = p

def change_vmin(p):
	global vmin
	vmin = p

def change_vmax(p):
	global vmax
	vmax = p

def change_brightness(p):
	global capture
	highgui.cvSetCaptureProperty(capture,highgui.CV_CAP_PROP_BRIGHTNESS, p)
	print "change brightness",p;	

def draw_target(img, x, y, color_name):

	width = 10
	if color_name == "GREEN":
		color = cv.CV_RGB(0,255,0)
	else:
		color = cv.CV_RGB(255,0,0)

	size = cv.cvGetSize(img)
	if x >= size.width or x < 0 or y >= size.height or y < 0:
		return

	#cv.cvSet2D(img,x,y,color);

	for i in range(width):
		for j in range(width):
			if i==0 or j==0 or j==9 or i==9:
				px = x + j - width/2
				py = y + i - width/2

				if px<0:
					px = 0
				if py<0:
					py = 0
				if px>=size.width:
					px = size.width-1
				if py>=size.height:
					py = size.height-1		

				cv.cvSet2D(img,py,px,color)

def averageWhitePoints(frame):
	xtotal = 0.0
	ytotal = 0.0
	count = 0;
	
	size = cv.cvGetSize(frame)
    
	for x in range(size.width):
        	for y in range(size.height):
			if(cv.cvGetReal2D(frame, y, x) > 200):
				xtotal = xtotal + x
				ytotal = ytotal + y
				count += 1
	if count == 0:
		return -1, -1

	return int(xtotal/count), int(ytotal/count)

def removeErrantPoints(frame):
    size = cv.cvGetSize(frame)
    
    for x in range(size.width):
        for y in range(size.height):
            if(cv.cvGetReal2D(frame, y, x) > 0):
                count = 0
                count += same2ndValue(frame, x-1, y)
                count += same2ndValue(frame, x+1, y)
                count += same2ndValue(frame, x, y-1)
                count += same2ndValue(frame, x, y+1)
                count += same2ndValue(frame, x-1, y-1)
                count += same2ndValue(frame, x-1, y+1)
                count += same2ndValue(frame, x+1, y-1)
                count += same2ndValue(frame, x+1, y+1)
                if count == 0:
                    cv.cvSet2D(frame, y, x, cv.cvScalar(0, 0, 0, 0))

def same2ndValue(frame, x, y):
    size = cv.cvGetSize(frame)
    if(x >= 0 and x < size.width and y >= 0 and y < size.height):
        if(cv.cvGetReal2D(frame, y, x) == 0):
            return 0
        else:
            return 1        #only return 1 if this pixel is also white
    else:
        return 0

def printStats(greenp, redp):
	outstring = ""
	if greenp[0] == -1:
		outstring += "Green fail | "
	if redp[0] == -1:
		outstring += "Red fail | "
	if greenp[0] != -1 and redp[0] != -1:
		xdiff = greenp[0] - redp[0]
		ydiff = greenp[1] - redp[1]
		distance = sqrt(xdiff*xdiff + ydiff*ydiff)
		outstring += "Distance = %003.02f | " % distance

	print outstring


def main(args):
	global capture
	global hmax, hmin
	global stats
#	highgui.cvNamedWindow('Hue', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('Camera', highgui.CV_WINDOW_AUTOSIZE)

#	highgui.cvNamedWindow('Hue', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('Red Hue', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('Green Hue', highgui.CV_WINDOW_AUTOSIZE)
#	highgui.cvNamedWindow('Saturation', highgui.CV_WINDOW_AUTOSIZE)

	highgui.cvNamedWindow('Value', highgui.CV_WINDOW_AUTOSIZE)
#	highgui.cvNamedWindow('Laser', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('Red Laser', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('Green Laser', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvMoveWindow('Camera', 0, 10)
#	highgui.cvMoveWindow('Hue', 10, 350)
#	highgui.cvMoveWindow('Saturation', 360, 10)
	highgui.cvMoveWindow('Value', 10, 420)
	#highgui.cvMoveWindow('Laser', 700, 40)
	highgui.cvMoveWindow('Red Laser', 360, 10)
	highgui.cvMoveWindow('Green Laser', 360, 360)
	highgui.cvMoveWindow('Red Hue',700, 10 )
	highgui.cvMoveWindow('Green Hue',700, 420) 

	highgui.cvCreateTrackbar("Brightness Trackbar","Camera",0,255, change_brightness);
#	highgui.cvCreateTrackbar("hmin Trackbar","Hue",hmin,180, change_hmin);
#	highgui.cvCreateTrackbar("hmax Trackbar","Hue",hmax,180, change_hmax);
#	highgui.cvCreateTrackbar("smin Trackbar","Saturation",smin,255, change_smin);
#	highgui.cvCreateTrackbar("smax Trackbar","Saturation",smax,255, change_smax);
	highgui.cvCreateTrackbar("vmin Trackbar","Value",vmin,255, change_vmin);
	highgui.cvCreateTrackbar("vmax Trackbar","Value",vmax,255, change_vmax);
	highgui.cvCreateTrackbar("red hmin Trackbar","Red Hue",red_hmin,180, change_red_hmin);
	highgui.cvCreateTrackbar("red hmax Trackbar","Red Hue",red_hmax,180, change_red_hmax);
	highgui.cvCreateTrackbar("green hmin Trackbar","Green Hue",green_hmin,180, change_green_hmin);
	highgui.cvCreateTrackbar("green hmax Trackbar","Green Hue",green_hmax,180, change_green_hmax);

	print "grabbing camera"
	capture = highgui.cvCreateCameraCapture(0)
	print "found camera"
	highgui.cvSetCaptureProperty(capture,highgui.CV_CAP_PROP_FRAME_WIDTH, iwidth)
	highgui.cvSetCaptureProperty(capture,highgui.CV_CAP_PROP_FRAME_HEIGHT, iheight)

	frame = highgui.cvQueryFrame(capture)
	frameSize = cv.cvGetSize(frame)

	hsv = cv.cvCreateImage(frameSize,8,3)
	mask = cv.cvCreateImage(frameSize,8,1)
#	hue = cv.cvCreateImage(frameSize,8,1)
	red_hue = cv.cvCreateImage(frameSize,8,1)
	green_hue = cv.cvCreateImage(frameSize,8,1)
	saturation = cv.cvCreateImage(frameSize,8,1)
	value = cv.cvCreateImage(frameSize,8,1)
#	laser = cv.cvCreateImage(frameSize,8,1)
	red_laser = cv.cvCreateImage(frameSize,8,1)
	green_laser = cv.cvCreateImage(frameSize,8,1)
	
	while 1:
		frame = highgui.cvQueryFrame(capture)

		cv.cvCvtColor(frame, hsv, cv.CV_BGR2HSV)	
		#cv.cvInRangeS(hsv,hsv_min,hsv_max,mask)
		cv.cvSplit(hsv,red_hue,saturation,value,None)
		cv.cvSplit(hsv,green_hue,saturation,value,None)
	
		cv.cvInRangeS(red_hue,red_hmin,red_hmax,red_hue)
		cv.cvInRangeS(green_hue, green_hmin, green_hmax, green_hue)
#		cv.cvInRangeS(saturation,smin,smax,saturation)
		cv.cvInRangeS(value,vmin,vmax,value)
		#cv.cvInRangeS(hue,0,180,hue)

		cv.cvAnd(red_hue, value, red_laser)
		cv.cvAnd(green_hue, value, green_laser)
        #cv.cvAnd(laser, value, laser)

		#removeErrantPoints(laser)

		green_cenX,green_cenY =  averageWhitePoints(green_laser)
		#print cenX,cenY
		draw_target(frame, green_cenX, green_cenY, "GREEN")
		#draw_target(frame,200,1)
		red_cenX, red_cenY = averageWhitePoints(red_laser)
		draw_target(frame, red_cenX, red_cenY, "RED")
		
#		highgui.cvShowImage('Hue',hue)
		highgui.cvShowImage('Camera',frame)

#		highgui.cvShowImage('Hue',hue)
		highgui.cvShowImage('Red Hue', red_hue)
		highgui.cvShowImage('Green Hue', green_hue)
#		highgui.cvShowImage('Saturation',saturation)

		highgui.cvShowImage('Value',value)
#		highgui.cvShowImage('Laser',laser)
		highgui.cvShowImage('Red Laser',red_laser)
		highgui.cvShowImage('Green Laser',green_laser)

		if stats:
			printStats((green_cenX, green_cenY), (red_cenX, red_cenY))

		k = highgui.cvWaitKey(10)
		if k == '\x1b' or k == 'q':
			sys.exit()
		if k == 'p':
			stats = (stats+1) % 2

if __name__ == '__main__':
	main(sys.argv[1:]);
