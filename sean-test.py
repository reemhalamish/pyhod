#!/usr/bin/python

import sys
from opencv import cv
from opencv import highgui

vmin = 10
vmax = 256
smin = 30

hsv_min = cv.cvScalar(0, smin, vmin, 0)
hsv_max = cv.cvScalar(180, 256, vmax, 0)

def main(args):
	highgui.cvNamedWindow('Camera', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('Hue', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('Satuation', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('Value', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvMoveWindow('Camera', 10, 40)
	highgui.cvMoveWindow('Hue', 10, 200)
	highgui.cvMoveWindow('Satuation', 30, 40)
	highgui.cvMoveWindow('Value', 300, 200)

	print "grabbing camera"
	capture = highgui.cvCreateCameraCapture(0)
	print "found camera"
	highgui.cvSetCaptureProperty(capture,highgui.CV_CAP_PROP_FRAME_WIDTH, 320)
	highgui.cvSetCaptureProperty(capture,highgui.CV_CAP_PROP_FRAME_HEIGHT, 240)

	frame = highgui.cvQueryFrame(capture)
	frameSize = cv.cvGetSize(frame)

	hsv = cv.cvCreateImage(frameSize,8,3)
	mask = cv.cvCreateImage(frameSize,8,1)
	hue = cv.cvCreateImage(frameSize,8,1)
	satuation = cv.cvCreateImage(frameSize,8,1)
	value = cv.cvCreateImage(frameSize,8,1)
	
	while 1:
		frame = highgui.cvQueryFrame(capture)

		cv.cvCvtColor(frame, hsv, cv.CV_BGR2HSV)	
		#cv.cvInRangeS(hsv,hsv_min,hsv_max,mask)
		cv.cvSplit(hsv,hue,satuation,value,None)
	
		cv.cvInRangeS(hue,140,177,hue)

		highgui.cvShowImage('Camera',frame)
		highgui.cvShowImage('Hue',hue)
		highgui.cvShowImage('Satuation',satuation)
		highgui.cvShowImage('Value',value)

		highgui.cvWaitKey(10)

if __name__ == '__main__':
	main(sys.argv[1:]);
