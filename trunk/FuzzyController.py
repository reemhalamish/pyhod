#!/usr/bin/python

import sys
from TurretControl import TurretControl

#Top left is assumed to be 0,0

class FuzzyTriangle:
	def __init__(self,a,b):
		self.alpha = a
		self.beta = b
		self.mid = (a+b)/2.0

	def membership(self,val):
		if val < self.alpha:
			return 0.0
		elif val < self.mid:
			return (val - self.alpha)/(self.mid - self.alpha)
		elif val <= self.beta:
			return (val - self.beta)/(self.mid-self.beta)
		else:
			return 0.0

class FuzzyLeftShoulder:
	def __init__(self,a,b):
		self.alpha = a
		self.beta = b
	
	def membership(self,val):
		if(val <= self.alpha):
			return 1.0
		elif(val < self.beta):
			return (val - self.alpha)/(self.beta - self.alpha)
		else:
			return 0.0

class FuzzyRightShoulder:
	def __init__(self,a,b):
		self.alpha = a
		self.beta = b
	
	def membership(self,val):
		if(val <= self.alpha):
			return 0.0
		elif(val < self.beta):
			return (val - self.beta)/(self.alpha - self.beta)
		else:
			return 1.0

class FuzzyController:

	def __init__(self, size_x, size_y):
		self.size_x = float(size_x)
		self.size_y = float(size_y)
		self.mid_x = float(size_x)/2.0
		self.mid_y = float(size_y)/2.0

		self.center = FuzzyTriangle(-0.2,0.2)

		self.slight_neg = FuzzyTriangle(-0.4,0.1)
		self.neg = FuzzyTriangle(-0.6,-0.2)
		self.far_neg = FuzzyLeftShoulder(-0.9,-0.3)
		
		self.slight_pos = FuzzyTriangle(0.1,0.4)
		self.pos = FuzzyTriangle(0.2,0.6)
		self.far_pos = FuzzyRightShoulder(0.3,0.9)

		self.tc = TurretControl()

	def update(self, x, y,allow_fire):
		self.tc.reset()

		x_val = (float(x) - self.mid_x)/self.mid_x
		y_val = (float(y) - self.mid_y)/self.mid_y
		
		x_result = self.__calcResult(x_val)
		y_result = self.__calcResult(y_val)

		print "X RESULT:",x_result
		print "Y RESULT:",y_result

		x_ok = False
		y_ok = False

		if(not (-0.05 < x_result and x_result < 0.05)):
			if(x_result < 0.0):
				self.tc.left(-45*x_result)
			else:
				self.tc.right(45*x_result)
		else:
			x_ok = True
		
		if(not (-0.2 < y_result and y_result < 0.2)):
			if(y_result < 0.0):
				self.tc.up(-20*y_result)
			else:
				self.tc.down(10*y_result)
		else:
			y_ok = True


	def __calcResult(self,val):

		"""
		print "fr:",self.far_pos.membership(val)
		print "r:",self.pos.membership(val)
		print "sr:",self.slight_pos.membership(val)
		print "cen:",self.center.membership(val)
		print "sl:",self.slight_neg.membership(val)
		print "l:",self.neg.membership(val)
		print "fl:",self.far_neg.membership(val)
		"""
		cen = self.center.membership(val)

		sn = self.slight_neg.membership(val)
		n = self.neg.membership(val)
		fn = self.far_neg.membership(val)
		
		sp = self.slight_pos.membership(val)
		p = self.pos.membership(val)
		fp = self.far_pos.membership(val)
	
		neg_value = -1*fn*fn + -0.5*n*n + -0.1*sn*sn	
		pos_value = 1*fp*fp + 0.5*p*p + 0.2*sp*sp	
		result = (neg_value + pos_value)/(fn*fn + n*n + sn*sn + cen*cen + sp*sp + p*p + fp*fp)
		
		return result


#bob = FuzzyController(240,320)
#bob.update(int(sys.argv[1]),int(sys.argv[2]),False)
