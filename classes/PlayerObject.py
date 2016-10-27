from .RenderObject import *

#
# The player-type. There can only be one object of this type on a map, since
# it determines where the camera will be positioned.
#
# The class also handles the direction constants for the directions NORTH,
# EAST, SOUTH and WEST
#
class PlayerObject(RenderObject):

	# Direction-Constants
	NORTH = 0
	EAST  = 1
	SOUTH = 2
	WEST  = 3


	#
	# Constructor
	#
	# @param direction : One of the four possible directions the player can look
	# 					 into. Use the constants in this class.
	#
	def __init__(self, direction = NORTH):
		super(PlayerObject, self).__init__()
		self.setViewDirection(direction)


	#
	# Returns the direction in which this player-object is looking in form of
	# an integer.
	#
	def getViewDirection(self):
		return self.__direction


	#
	# Returns the direction in which the player looks as string of it's name.
	#
	def getViewDirectionString(self):
		if self.__direction == NORTH:
			return "North"
		elif self.__direction == EAST:
			return "East"
		elif self.__direction == SOUTH:
			return "South"
		elif self.__direction == WEST:
			return "West"
		else: # the direction is invalid
			return "Error"


	#
	# Sets the direction in which the player looks.
	#
	# @param direction : One of the four possible directions the player can look
	# 					 into. Use the constants in this class.
	#
	def setViewDirection(self, direction):
		self.__direction = direction % 4 # when 4 is given, set to 0 etc.
