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
			[(-1,0,0), (200,0,0)], # vertices
			[(0,1)], # edges
			[], # no faces
			(1,0,0) # color : red
			),
		# y-axis
		RenderObject(
			[(0,-1,0), (0,200,0)], # vertices
			[(0,1)], # edges
			[], # no faces
			(0,1,0) # color : green
			),
		# z-axis
		RenderObject(
			[(0,0,-1), (0,0,200)], # vertices
			[(0,1)], # edges
			[], # no faces
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
		self.__camera = ((0, 0, 0), # eX eY eZ
						 (0, 0, 0)) # cX cY cZ


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

		# things in the back are covered by things in front of them
		glEnable(GL_DEPTH_TEST)


	#
	# This function renders the current map with the RenderObject it contains
	# and sets the camera to the position of the last PlayerObject it can find.
	# To avoid unwanted behaviour please only include one PlayerObject.
	#
	def render(self):
		# Clear OpenGL
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		# glMatrixMode(GL_PROJECTION)
		# glLoadIdentity()
		# set Camera position
		self.setCamera3rdPerson()

		# glMatrixMode(GL_MODELVIEW)
		# render the objects in the map and ground where needed
		self.renderAllObjects()

		#
		# update is better, but does not work.
		# flip sadly produces an error on closing, but that is acceptable,
		# as the user does not notice this.
		#
		# pygame.display.update()
		pygame.display.flip()


	#
	# Sets the camera to the correct position depending on where the player is
	#
	def setCamera3rdPerson(self):
		# find player and set camera accordingly
		# !inefficient!
		for x in range(len(self.__map)):
			for z in range(len(self.__map[0])):
				obj = self.__map[x][z]
				# print("+1 lookup")
				if isinstance(obj, PlayerObject):
					self.setCameraPosition(x, z, obj.getViewDirection())


	#
	# Renders the objects in the current map to OpenGL and ground where needed.
	#
	def renderAllObjects(self):
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

		# # camera position
		# eY = 3 - self.__camera[0][1]
		#
		# # looking at
		# cY = eY - 1 - self.__camera[1][1] # slightly downwards
		#
		# if direction == PlayerObject.NORTH:
		# 	# camera position
		# 	eX = x + 7.5 - self.__camera[0][0]
		# 	eZ = z + 0.5 - self.__camera[0][2]
		#
		# 	# looking at
		# 	cX = eX - 5 - self.__camera[1][0]
		# 	cZ = eZ - self.__camera[1][2]
		# elif direction == PlayerObject.SOUTH:
		# 	# camera position
		# 	eX = x - 7.5 - self.__camera[0][0]
		# 	eZ = z + 0.5 - self.__camera[0][2]
		#
		# 	# looking at
		# 	cX = eX + 5 - self.__camera[1][0]
		# 	cZ = eZ - self.__camera[1][2]
		# elif direction == PlayerObject.EAST:
		# 	# camera position
		# 	eX = x + 0.5 - self.__camera[0][0]
		# 	eZ = z + 7.5 - self.__camera[0][2]
		#
		# 	# looking at
		# 	cX = eX - self.__camera[1][0]
		# 	cZ = eZ - 5 - self.__camera[1][2]
		# elif direction == PlayerObject.WEST:
		# 	# camera position
		# 	eX = x + 0.5 - self.__camera[0][0]
		# 	eZ = z - 7.5 - self.__camera[0][2]
		#
		# 	# looking at
		# 	cX = eX - self.__camera[1][0]
		# 	cZ = eZ + 5 - self.__camera[1][2]

		if not self.stopper:
			eX = 12 + 7.5
			eY = 0 + 3
			eZ = 1 + 0.5
			cX = 12 + 0.5
			cY = 0 + 1
			cZ = 1 + 0.5

			self.stopper = True
		else:
			# eX = 0
			# eY = 0
			# eZ = 0
			# cX = 0
			# cY = 0
			# cZ = 0

			eX = 12 + 7.5
			eY = 0 + 3
			eZ = 1 + 0.5
			cX = 12 + 0.5
			cY = 0 + 1
			cZ = 1 + 0.5

		# --------------------
		# make it happen
		self.__camera = ((eX, eY, eZ),
						 (cX, cY, cZ))
		print(str(eX) + " " + str(eY) + " " + str(eZ) + " " + str(cX) + " " +
				str(cY) + " " + str(cZ))

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
