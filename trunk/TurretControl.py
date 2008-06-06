#!/usr/bin/env python
import sys
import time
import nxt.locator
from nxt.motor import *

class Update(object):
	MODE = 0x01
	SPEED = 0x02
	TACHO_LIMIT = 0x04
	RESET_COUNT = 0x08
	PID_VALUES = 0x10
	RESET_BLOCK_COUNT = 0x20
	RESET_ROTATION_COUNT = 0x40
	PENDING = 0x80

def update(bconn,motor,value):
	bconn.write_io_map(131073,motor.port+18,str(value))

def set_PID(bconn,motor,P,I,D):
	"""
	Change the PID parameters
	>>> set_PID(motor,"\x78","\x78","\x78")
	Use only hexadecimal number in string !
	"""

	bconn.write_io_map(131073,motor.port*32+22,P)
	bconn.write_io_map(131073,motor.port*32+23,I)
	bconn.write_io_map(131073,motor.port*32+24,D)
	update(bconn,motor,Update.PID_VALUES)	

class TurretControl:

	def __init__(self):
		self.brick = nxt.locator.find_one_brick()
		self.bconn = None
		self.motor = None
	
		if self.brick:
			self.bconn = self.brick.connect()
		else:
			print 'No NXT bricks found'

		self.x_motor = Motor(self.bconn,PORT_A)
		self.y_motor = Motor(self.bconn,PORT_B)
		self.trigger = Motor(self.bconn,PORT_C)

	def fire(self):
		self.__rotate(-10,self.trigger,90)
		time.sleep(0.5)
		self.__rotate(5,self.trigger,60)
		
	def left(self,degrees):
		self.__rotate(degrees,self.x_motor,75)

	def right(self,degrees):
		self.__rotate(-1*degrees,self.x_motor,75)

	def up(self,degrees):
		self.__rotate(-1*degrees,self.y_motor,75)
	
	def down(self,degrees):
		self.__rotate(degrees,self.y_motor,75)

	def reset(self):
		update(self.bconn,self.x_motor,Update.RESET_COUNT)
		update(self.bconn,self.y_motor,Update.RESET_COUNT)

	def __rotate(self,degrees,motor, power):

		if(degrees == 0):
			degrees = 1

		#self.reset()
		#print "START",self.motor.get_output_state();
		
		sign = 1
		if(degrees < 0):
			motor.power = -1*power
			sign = -1
		else:
			motor.power = power

		motor.mode = MODE_MOTOR_ON
		motor.run_state = RUN_STATE_RUNNING
		motor.tacho_limit = sign*degrees
		self.regulation = REGULATION_MOTOR_SPEED
		motor.set_output_state()
		
		#print motor.get_output_state();

#turret = TurretControl()
#turret.reset()
#turret.fire()
"""
x_axis = int(sys.argv[1])
y_axis = int(sys.argv[2])

turret.left(45)
turret.up(y_axis)
"""
