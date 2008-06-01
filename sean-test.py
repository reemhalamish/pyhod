#!/usr/bin/python

import sys
from opencv import cv
from opencv import highgui
from math import sqrt
from time import time

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

# global statistics variables
stats = True
frameCount = 0
redFailCount = 0
greenFailCount = 0
startTime = time()

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

def printRunningStats(greenp, redp):
	global frameCount, redFailCount, greenFailCount
	frameCount += 1
	outstring = "Frame " + str(frameCount) + " | "
	if greenp[0] == -1:
		greenFailCount += 1
		outstring += "Green fail | "
	if redp[0] == -1:
		redFailCount += 1
		outstring += "Red fail | "
	if greenp[0] != -1 and redp[0] != -1:
		xdiff = greenp[0] - redp[0]
		ydiff = greenp[1] - redp[1]
		outstring += "Distance = %3.02f | " % sqrt(xdiff*xdiff + ydiff*ydiff)

	print outstring

def printTotalStats():
	global frameCount, redFailCount, greenFailCount, startTime
	endTime = time()
	table = {"fc": frameCount, "gf" : greenFailCount/(frameCount*1.0), "rf" : redFailCount/(frameCount*1.0), "fps" : frameCount/(endTime-startTime)}
	print "Total Frames: %(fc)d | Green Failure: %(gf)1.02f |  Red Failure: %(rf)1.02f | Frames/Sec: %(fps)2.02f" % table
	frameCount = 0
	redFailCount = 0
	greenFailCount = 0

def main(args):
	global capture
	global hmax, hmin
	global stats, startTime

	highgui.cvNamedWindow('Camera', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('Red Hue', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('Green Hue', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('Value', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('Red Laser', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('Green Laser', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvMoveWindow('Camera', 0, 10)
	highgui.cvMoveWindow('Value', 10, 420)
	highgui.cvMoveWindow('Red Laser', 360, 10)
	highgui.cvMoveWindow('Green Laser', 360, 360)
	highgui.cvMoveWindow('Red Hue',700, 10 )
	highgui.cvMoveWindow('Green Hue',700, 420) 

	highgui.cvCreateTrackbar("Brightness Trackbar","Camera",0,255, change_brightness);
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
	red_hue = cv.cvCreateImage(frameSize,8,1)
	green_hue = cv.cvCreateImage(frameSize,8,1)
	saturation = cv.cvCreateImage(frameSize,8,1)
	value = cv.cvCreateImage(frameSize,8,1)
	red_laser = cv.cvCreateImage(frameSize,8,1)
	green_laser = cv.cvCreateImage(frameSize,8,1)

	while 1:
		frame = highgui.cvQueryFrame(capture)

		cv.cvCvtColor(frame, hsv, cv.CV_BGR2HSV)	
		cv.cvSplit(hsv,red_hue,saturation,value,None)
		cv.cvSplit(hsv,green_hue,saturation,value,None)
	
		cv.cvInRangeS(red_hue,red_hmin,red_hmax,red_hue)
		cv.cvInRangeS(green_hue, green_hmin, green_hmax, green_hue)
		cv.cvInRangeS(value,vmin,vmax,value)

		cv.cvAnd(red_hue, value, red_laser)
		cv.cvAnd(green_hue, value, green_laser)

		green_cenX,green_cenY =  averageWhitePoints(green_laser)
		draw_target(frame, green_cenX, green_cenY, "GREEN")
		red_cenX, red_cenY = averageWhitePoints(red_laser)
		draw_target(frame, red_cenX, red_cenY, "RED")
		
		highgui.cvShowImage('Camera',frame)
		highgui.cvShowImage('Red Hue', red_hue)
		highgui.cvShowImage('Green Hue', green_hue)
		highgui.cvShowImage('Value',value)
		highgui.cvShowImage('Red Laser',red_laser)
		highgui.cvShowImage('Green Laser',green_laser)

		if stats:
			printRunningStats((green_cenX, green_cenY), (red_cenX, red_cenY))

		k = highgui.cvWaitKey(10)
		if k == '\x1b' or k == 'q':
			sys.exit()
		if k == 'p':
			if stats:
				printTotalStats()
				stats = False
			else:
				startTime = time()
				stats = True

if __name__ == '__main__':
	main(sys.argv[1:]);
