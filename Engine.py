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
					self.setCameraPosition(x, z, obj.getViewDirection())

		# Clear the OpenGL screen
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		# Display all RenderObjects in the map
		for x in range(len(self.__map)):
			for z in range(len(self.__map[0])):
				obj = self.__map[x][z]
				if not obj == None:
					if obj.getGroundNecessary(): # render ground under object
												 # if needed - has to be first
												 # to be overlapped by the
												 # object itself
						self.getGround().render(x, -1, z)

					obj.render(x, 0, z)
				else: # render ground underneath if no object
					self.getGround().render(x, -1, z)

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
	# @param x : The x-coordinate of the player to see in third-person.
	# @param z : The z-coordinate of the player to see in third-person.
	# @param direction : The direction the player to see in third-person is
	# 					 looking in.
	#
	def setCameraPosition(self, x, z, direction):
		print("Set Camera to " + str(x) + " : " + str(z) + " > " +
				str(direction))

		# --------------------
		# camera position
		eX = x + 7 + 0.5
		eY = 3
		eZ = z + 0.5

		# --------------------
		# looking at
		cY = eY - 1

		if direction == PlayerObject.NORTH:
			# looking at
			cX = eX - 5
			cZ = eZ
		elif direction == PlayerObject.SOUTH:
			# looking at
			cX = eX + 5
			cZ = eZ
		elif direction == PlayerObject.EAST:
			# looking at
			cX = eX
			cZ = eZ - 5
		elif direction == PlayerObject.WEST:
			# looking at
			cX = eX
			cZ = eZ + 5

		# --------------------
		# make it happen
		gluLookAt(eX, eY, eZ, cX, cY, cZ, 0, 1, 0)


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
