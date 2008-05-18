#!/usr/bin/python

from opencv import cv
from opencv import highgui

class IntegralImage:

	def __init__(self,image):
		self.origImage = image
		print "start.."
		self.integralImage = self.__calculate()
		print "done"

	def getOriginalImage(self):
		return self.origImage

	def __calculate(self):
		print "I want to calculate an image"
		size = cv.cvGetSize(self.origImage)
		
		result = cv.cvCreateMat(size.height,size.width,cv.CV_32FC1)
		row_sums = cv.cvCreateMat(size.height,size.width,cv.CV_32FC1)
		for i in range(size.height):
			for j in range(size.width):
				image_value = cv.cvGet2D(self.origImage,i,j)
				image_value = image_value[1]
				prev_row_sum = 0

				if(i == 0):
					cv.cvmSet(row_sums,i,j,image_value)
				else:
					prev_row_sum = cv.cvmGet(row_sums,i-1,j)
					cv.cvmSet(row_sums,i,j,image_value+prev_row_sum)
				
				if(j == 0):	
					cv.cvmSet(result,i,j,prev_row_sum+image_value)
				else:
					prev_result = cv.cvmGet(result,i,j-1)
					cv.cvmSet(result,i,j,prev_row_sum+image_value+prev_result)
		
		return result

image = highgui.cvLoadImage("Screenshot-Camera.png",1)
highgui.cvNamedWindow("Original",1)
highgui.cvShowImage("Original",image)
iimg = IntegralImage(image)

size = cv.cvGetSize(image)
"""
for i in range(size.height):
	for j in range(size.width):
		print cv.cvmGet(iimg.integralImage,i,j)
"""
highgui.cvWaitKey()
