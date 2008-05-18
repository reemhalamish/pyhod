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

		self.motor = Motor(self.bconn,PORT_A)

	def reset(self):
		update(self.bconn,self.motor,Update.RESET_COUNT)

	def rotate(self,degrees):
		self.reset()
		sign = 1
		if(degrees < 0):
			self.motor.power = -60
			sign = -1
		else:
			self.motor.power = 60

		self.motor.mode = MODE_MOTOR_ON
		self.motor.run_state = RUN_STATE_RUNNING
		self.motor.tacho_limit = sign*degrees
		self.regulation = REGULATION_MOTOR_SPEED
		self.motor.set_output_state()
	
		while(True):
			rot_count = self.motor.get_output_state()[7]
			print self.motor.get_output_state();
			if(sign*rot_count >= sign*degrees):
				break;
			time.sleep(0.1)

#turret = TurretControl()
#while(True):
#	turret.rotate(200)
#	turret.rotate(-200)
