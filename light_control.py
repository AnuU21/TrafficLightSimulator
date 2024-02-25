"""
state 1
vertical car lanes: straight
horizontal car lanes: stop
vertical pedestrian lanes: go
horizontal pedestrian lanes: stop

state 2
vertical car lanes: stop
horizontal car lanes: straight
vertical pedestrian lanes: stop
horizontal pedestrian lanes: go

state 3
vertical car lanes: right turn
horizontal car lanes: left turn
vertical pedestrian lanes: stop
horizontal pedestrian lanes: stop

state 4
vertical car lanes: left turn
horizontal car lanes: right turn
vertical pedestrian lanes: stop
horizontal pedestrian lanes: stop
"""

import time
from enum import Enum

yellowDuration = 3

class SignalColor(Enum):
	RED = 1
	YELLOW = 2
	STRAIGHT = 3
	RIGHT = 4
	LEFT = 5

class TrafficSignal:
	def __init__(self, signal: SignalColor):
		self.currentSignal = signal

	def switch_signal(self, newSignal):
		self.currentSignal = newSignal

	def get_signal(self):
		return self.currentSignal

class TrafficIntersectionController:
	ts1 = TrafficSignal(SignalColor.RED) # top
	ts2 = TrafficSignal(SignalColor.RED) # right
	ts3 = TrafficSignal(SignalColor.RED) # bottom
	ts4 = TrafficSignal(SignalColor.RED) # left

	def __init__(self):
		self.state = 1  # Initialize with state 1
		self.active = True

	def get_current_state(self):
		return self.state

	def switch_state(self, newState):
		self.state = newState

		match self.state:
			case 1:
				self.ts2.switch_signal(SignalColor.YELLOW)
				self.ts4.switch_signal(SignalColor.YELLOW)
				time.sleep(yellowDuration)
				self.ts2.switch_signal(SignalColor.RED)
				self.ts4.switch_signal(SignalColor.RED)
				self.ts1.switch_signal(SignalColor.STRAIGHT)
				self.ts3.switch_signal(SignalColor.STRAIGHT)
			case 2:
				self.ts1.switch_signal(SignalColor.YELLOW)
				self.ts3.switch_signal(SignalColor.YELLOW)
				time.sleep(yellowDuration)
				self.ts1.switch_signal(SignalColor.RED)
				self.ts3.switch_signal(SignalColor.RED)
				self.ts2.switch_signal(SignalColor.STRAIGHT)
				self.ts4.switch_signal(SignalColor.STRAIGHT)
			case 3:
				self.ts1.switch_signal(SignalColor.RIGHT)
				self.ts2.switch_signal(SignalColor.LEFT)
				self.ts3.switch_signal(SignalColor.RIGHT)
				self.ts4.switch_signal(SignalColor.LEFT)
			case 4:
				self.ts1.switch_signal(SignalColor.LEFT)
				self.ts2.switch_signal(SignalColor.RIGHT)
				self.ts3.switch_signal(SignalColor.LEFT)
				self.ts4.switch_signal(SignalColor.RIGHT)

"""
EXAMPLE USAGE:

controller = TrafficIntersectionController()
switch_interval = 3

def printTrafficLights():
	print(f"Top traffic light is {controller.ts1.get_signal()}")
	print(f"Right traffic light is {controller.ts2.get_signal()}")
	print(f"Bottom traffic light is {controller.ts3.get_signal()}")
	print(f"Left traffic light is {controller.ts4.get_signal()}")

while True:
	current_state = controller.get_current_state()
	print(f"Current State: {current_state}.", end="\n")
	# Example descriptions for each state (customize as needed)
	
	new_state = current_state % 4 + 1

	time.sleep(switch_interval)
	controller.switch_state(new_state)s
"""