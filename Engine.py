import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from classes.PlayerObject import *

#
# The interface to create a 3D representation of objects in a space.
#
# All interactions with this engine should work with this class.
#
class Engine(object):


	#
	# The three axis (x, y, z) defined as RenderObjects.
	#
	# Helpful for debugging and visualization.
	#
	__axis = (
		# x-axis
		RenderObject(
			((-200,0,0), (200,0,0)), # vertices
			((0,1), (1,0)), # edges (two, because else it isn't correct syntax)
			(), # no faces
			(1,0,0) # color : red
			),
		# y-axis
		RenderObject(
			((0,-200,0), (0,200,0)), # vertices
			((0,1), (1,0)), # edges (two, because else it isn't correct syntax)
			(), # no faces
			(0,1,0) # color : green
			),
		# z-axis
		RenderObject(
			((0,0,-200), (0,0,200)), # vertices
			((0,1), (1,0)), # edges (two, because else it isn't correct syntax)
			(), # no faces
			(0,0,1) # color : blue
			)
		)


	#
	# Constructor for an engine to display 3D objects in space. Create an object
	# of this class to interact with a 3D OpenGL view displayed with pygame.
	#
	# @param display : The size of the window and view. A list of two integers.
	# 				   Default: (800, 600)
	# @param p_map : A 2D-map of RenderObjects to display.
	# 				 Default: ((None, None, None),
	# 						   (None, PlayerObject(), None),
	# 						   (None, None, None))
	#
	def __init__(self, display = (800, 600),
					   p_map = ((None, None, None),
					   			(None, PlayerObject(), None),
								(None, None, None))):
		# initialize vars by params
		self.__map = p_map
		self.__display = display

		# initialize vars by standards
		self.debug = False
		self.__cameraPosition = (0, 0, 0)
		self.__rotation = PlayerObject.NORTH


	#
	# This function initializes pygame and OpenGL. Call before rendering
	# anything.
	#
	def startUp(self):
		pygame.init()
		pygame.display.set_mode(self.__display, DOUBLEBUF|OPENGL)

		# set the perspective
		fieldOfView = 45 # degrees
		aspectRatio = self.__display[0] / self.__display[1]
		gluPerspective(fieldOfView, aspectRatio, 0.1, 50.0)

		self.setCameraPosition(0, 0, 0)
		self.turnCameraInDirection(PlayerObject.NORTH)


	#
	# This function renders the current map with the RenderObject it contains
	# and sets the camera to the position of the last PlayerObject it can find.
	# To avoid unwanted behaviour please only include one PlayerObject.
	#
	def render(self):
		# find player and set camera accordingly
		# !inefficient!
		for x in range(len(self.__map)):
			for z in range(len(self.__map[0])):
				obj = self.__map[x][z]
				# print("+1 lookup")
				if (not obj == None) and isinstance(obj, PlayerObject):
					self.setCameraPosition(x, -2, z)
					self.turnCameraInDirection(obj.getViewDirection())

		# Clear the OpenGL screen
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		# get the current position of the camera to position objects
		# accordingly.
		camPos = self.getCameraPosition()

		# Display all RenderObjects in the map
		for x in range(len(self.__map)):
			for z in range(len(self.__map[0])):
				obj = self.__map[x][z]
				if not obj == None:
					if obj.getGroundNecessary(): # render ground under object
												 # if needed - has to be first
												 # to be overlapped by the
												 # object itself
						self.getGround().render(x - camPos[0], -1 - camPos[1], z - camPos[2])

					obj.render(x - camPos[0], 0 - camPos[1], z - camPos[2])
				else: # render ground underneath if no object
					self.getGround().render(x - camPos[0], -1 - camPos[1], z - camPos[2])

		# in case debug is set to true, display the axis (x, y, z)
		if self.debug:
			for axis in Engine.__axis:
				axis.setRenderAsEdges()
				axis.setGroundNecessary(False)
				axis.render(0, 0, 0)

		#
		# update is better, but does not work.
		# flip sadly produces an error on closing, but that is acceptable,
		# as the user does not notice this.
		#
		# pygame.display.update()
		pygame.display.flip()


	#
	# Moves the camera to the desired absolute position in space.
	#
	# @param x : The x-coordinate to move the camera to.
	# @param y : The y-coordinate to move the camera to.
	# @param z : The z-coordinate to move the camera to.
	def setCameraPosition(self, x, y, z):
		print("Set Camera to " + str(x) + " : " + str(y) + " : " + str(z))

		# reset camera to 0, 0, 0
		oldPos = self.getCameraPosition()
		glTranslatef(-oldPos[0], -oldPos[1], -oldPos[2]) # minus 'cause it moves back

		# move camera to given coords
		glTranslatef(x, y, z)


	#
	# Return the camera's position as coordinate-list: (x, y, z)
	#
	def getCameraPosition(self):
		return self.__cameraPosition


	#
	# Turn the camera in the desired direction. This takes care of angling the
	# camera slightly downwards etc. for looking at the player in third-person
	# perspective.
	#
	# @param direction : One of the four directions specified as constants in
	# 					 PlayerObject. (NORTH, EAST, SOUTH, WEST)
	#
	def turnCameraInDirection(self, direction):
		direction = direction % 4 # make sure it's a valid direction
		print("Turning camera in direction: " + str(direction))


	#
	# Set the map that is to be rendered by the engine, containing the
	# required RenderObjects.
	#
	# @param p_map : A 2D-list containing one PlayerObject, the required amount
	# 				 of RenderObjects and None-s to display the current game's
	# 				 state.
	#
	def setMap(self, p_map):
		self.__map = p_map


	#
	# The ground that is currently being used to display under objects that
	# need a ground underneath them because they don't cover the whole field.
	# (RenderObject)
	#
	def getGround(self):
		return self.__ground


	#
	# Set the ground to be used to display under objects that need a ground
	# underneath them because they don't cover the whole field.
	#
	# @param ground : A RenderObject to display.
	#
	def setGround(self, ground):
		self.__ground = ground
