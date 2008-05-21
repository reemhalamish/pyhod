#!/usr/bin/python

import sys
from opencv import cv
from opencv import highgui



iwidth = 320
iheight = 240 

hmin = 4 
hmax = 18 

vmin = 140 
vmax = 255 
smin = 147 
smax = 255


hsv_min = cv.cvScalar(0, smin, vmin, 0)
hsv_max = cv.cvScalar(180, 256, vmax, 0)

capture = None

def change_hmin(p):
	global hmin
	hmin = p

def change_hmax(p):
	global hmax
	hmax = p

def change_smin(p):
	global smin
	smin = p

def change_smax(p):
	global smax
	smax = p

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

def draw_target(img, x, y):
	width = 10
	color = cv.CV_RGB(0,255,0);

	size = cv.cvGetSize(img)

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
		return 0, 0

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

def main(args):
	global capture
	global hmax, hmin
	highgui.cvNamedWindow('Hue', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('Camera', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('Saturation', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('Value', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('Laser', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvMoveWindow('Camera', 0, 10)
	highgui.cvMoveWindow('Hue', 0, 350)
	highgui.cvMoveWindow('Saturation', 360, 10)
	highgui.cvMoveWindow('Value', 360, 350)
	highgui.cvMoveWindow('Laser', 700, 40)

	highgui.cvCreateTrackbar("Brightness Trackbar","Camera",0,255, change_brightness);
	highgui.cvCreateTrackbar("hmin Trackbar","Hue",hmin,180, change_hmin);
	highgui.cvCreateTrackbar("hmax Trackbar","Hue",hmax,180, change_hmax);
	highgui.cvCreateTrackbar("smin Trackbar","Saturation",smin,255, change_smin);
	highgui.cvCreateTrackbar("smax Trackbar","Saturation",smax,255, change_smax);
	highgui.cvCreateTrackbar("vmin Trackbar","Value",vmin,255, change_vmin);
	highgui.cvCreateTrackbar("vmax Trackbar","Value",vmax,255, change_vmax);

	print "grabbing camera"
	capture = highgui.cvCreateCameraCapture(0)
	print "found camera"
	highgui.cvSetCaptureProperty(capture,highgui.CV_CAP_PROP_FRAME_WIDTH, iwidth)
	highgui.cvSetCaptureProperty(capture,highgui.CV_CAP_PROP_FRAME_HEIGHT, iheight)

	frame = highgui.cvQueryFrame(capture)
	frameSize = cv.cvGetSize(frame)

	hsv = cv.cvCreateImage(frameSize,8,3)
	mask = cv.cvCreateImage(frameSize,8,1)
	hue = cv.cvCreateImage(frameSize,8,1)
	saturation = cv.cvCreateImage(frameSize,8,1)
	value = cv.cvCreateImage(frameSize,8,1)
	laser = cv.cvCreateImage(frameSize,8,1)
	
	while 1:
		frame = highgui.cvQueryFrame(capture)

		cv.cvCvtColor(frame, hsv, cv.CV_BGR2HSV)	
		#cv.cvInRangeS(hsv,hsv_min,hsv_max,mask)
		cv.cvSplit(hsv,hue,saturation,value,None)
	

		#print hmin, hmax
		cv.cvInRangeS(hue,cv.cvScalar(hmin),cv.cvScalar(hmax),hue)
		cv.cvInRangeS(saturation,cv.cvScalar(smin),cv.cvScalar(smax),saturation)
		cv.cvInRangeS(value,cv.cvScalar(vmin),cv.cvScalar(vmax),value)
		
		#cv.cvInRangeS(hue,cv.cvScalar(0),cv.cvScalar(180),hue)

        	cv.cvAnd(hue, value, laser)
        	#cv.cvAnd(laser, value, laser)
		
		# stupid filter
		#removeErrantPoints(laser)

		cenX,cenY =  averageWhitePoints(laser)
		#print cenX,cenY
		draw_target(frame,cenX,cenY)
		#draw_target(frame,200,1)
		
		highgui.cvShowImage('Hue',hue)
		highgui.cvShowImage('Camera',frame)
		highgui.cvShowImage('Saturation',saturation)
		highgui.cvShowImage('Value',value)
		highgui.cvShowImage('Laser',laser)

		highgui.cvWaitKey(10)

if __name__ == '__main__':
	main(sys.argv[1:]);
