from .RenderObject import *

class PlayerObject(RenderObject):


	# Directions
	NORTH = 0
	EAST  = 1
	SOUTH = 2
	WEST  = 3


	def __init__(self, direction = NORTH):
		super(PlayerObject, self).__init__()
		self.setViewDirection(direction)


	def getViewDirection(self):
		return self.__direction


	def getViewDirectionString(self):
		if self.__direction == NORTH:
			return "North"
		elif self.__direction == EAST:
			return "East"
		elif self.__direction == SOUTH:
			return "South"
		elif self.__direction == WEST:
			return "West"
		else:
			return "Error"


	def setViewDirection(self, direction):
		self.__direction = direction % 4 # when 4 is given, set to 0 etc.
