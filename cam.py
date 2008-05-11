#! /usr/bin/env python

import sys

# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui

if __name__ == '__main__':
	print "HOWDY, welcome to the webcam proggy"

	# first, create the necessary windows
	highgui.cvNamedWindow('Camera', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('HUE', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('SATURATION', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('VALUE', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('RED', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('GREEN', highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow('BLUE', highgui.CV_WINDOW_AUTOSIZE)

	# move the new window to a better place
	highgui.cvMoveWindow('Camera', 0, 40)
	highgui.cvMoveWindow('HUE', 0, 400)
	highgui.cvMoveWindow('SATURATION', 330, 40)
	highgui.cvMoveWindow('VALUE', 330, 400)
	highgui.cvMoveWindow('RED', 660, 40)
	highgui.cvMoveWindow('GREEN', 660, 400)
	highgui.cvMoveWindow('BLUE', 990, 40)

	capture = highgui.cvCreateCameraCapture(0)

	# set the wanted image size from the camera
	highgui.cvSetCaptureProperty(capture, highgui.CV_CAP_PROP_FRAME_WIDTH, 320)
	highgui.cvSetCaptureProperty(capture, highgui.CV_CAP_PROP_FRAME_HEIGHT, 240)

	# check that capture device is OK
	if not capture:

		print "Error opening capture device"
		sys.exit (1)

	# capture the 1st frame to get some propertie on it
	frame = highgui.cvQueryFrame(capture)

	# get some properties of the frame
	frame_size = cv.cvGetSize(frame)

	# compute which selection of the frame we want to monitor
	selection = cv.cvRect(0, 0, frame.width, frame.height)

	hsv = cv.cvCreateImage(frame_size, 8, 3)
	hue = cv.cvCreateImage(frame_size, 8, 1)
	saturation = cv.cvCreateImage(frame_size, 8, 1)
	val_scale = cv.cvCreateImage(frame_size, 8, 1)
	value = cv.cvCreateImage(frame_size, 8, 1)
	red = cv.cvCreateImage(frame_size, 8, 1)
	green = cv.cvCreateImage(frame_size, 8, 1)
	blue = cv.cvCreateImage(frame_size, 8, 1)

	while 1:
		# 1. capture the current image
		frame = highgui.cvQueryFrame (capture)
		if frame is None:
			# no image captured... end the processing
			break

		# compute the hsv version of the image 
		cv.cvCvtColor(frame, hsv, cv.CV_BGR2HSV)

		# compute the hue/sat/value from the hsv image
		cv.cvSplit(hsv, hue, saturation, value, None)
		cv.cvSplit(frame, blue, green, red, None);
		cv.cvCvtScale(value, val_scale, 1/100.);
		cv.cvCvtScale(val_scale, value, 1);

		# handle events

		k = highgui.cvWaitKey (10)

		# we can now display the images
		highgui.cvShowImage('Camera', frame)
		highgui.cvShowImage('HUE', hue)
		highgui.cvShowImage('SATURATION', saturation)
		highgui.cvShowImage('VALUE', value)
		highgui.cvShowImage('RED', red)
		highgui.cvShowImage('GREEN', green)
		highgui.cvShowImage('BLUE', blue)

		if k == '\x1b':
			# user has press the ESC key, so exit
			break
