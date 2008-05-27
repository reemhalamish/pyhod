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
				image_value = image_value[0]
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
	
				if(i == 0 and j == 0):
					print "image_value:",image_value
					print "prev_row_sum:",prev_row_sum	
		return result

image = highgui.cvLoadImage("Screenshot-Camera.png",1)
iimg = IntegralImage(image)

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

def calcBox(iimg, x, y, size):
	point1 =  cv.cvmGet(iimg,x,y)
	point2 =  cv.cvmGet(iimg,x+size,y+size)
	point3 =  cv.cvmGet(iimg,x,y+size)
	point4 =  cv.cvmGet(iimg,x+size,y)
	return (point1+point2)-(point3+point4)

size = cv.cvGetSize(image)
sum = 0
for i in range(1,5):#size.height):
	for j in range(1,5):
		sum = sum + cv.cvGet2D(image,i,j)[0]

print sum
#print cv.cvmGet(iimg.integralImage,size.height-1,size.width-1)
print calcBox(iimg.integralImage,1,1,4)

boxSize = 16
bestValue = -999999.9
best_i = 0
best_j = 0
for i in range(size.height-boxSize):
	for j in range(size.width-boxSize):
		box1 = calcBox(iimg.integralImage,i,j,boxSize)
		box2 = calcBox(iimg.integralImage,i+6,j+6,4)
		value = box2*box2/box1
		if(value > bestValue):
			bestValue = value
			best_i = i
			best_j = j

print "Best I",best_i,"Best j",best_j

draw_target(image,best_i,best_j)

print calcBox(iimg.integralImage,160,230,16)
print calcBox(iimg.integralImage,152,222,32)
highgui.cvNamedWindow("Original",1)
highgui.cvShowImage("Original",image)
highgui.cvWaitKey()
