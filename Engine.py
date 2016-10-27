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
			[(0,1,0)], # edges
			[], # no faces
			[(1,0,0)] # color : red
			),
		# y-axis
		RenderObject(
			[(0,-1,0), (0,200,0)], # vertices
			[(0,1,0)], # edges
			[], # no faces
			[(0,1,0)] # color : green
			),
		# z-axis
		RenderObject(
			[(0,0,-1), (0,0,200)], # vertices
			[(0,1,0)], # edges
			[], # no faces
			[(0,0,1)] # color : blue
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

		# Set projection matrix
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()

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

		# set up model-view matrix
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		# set Camera position
		# TODO: inefficient - use parameter?
		for z in range(len(self.__map)):
			for x in range(len(self.__map[0])):
				obj = self.__map[z][x]
				# print("+1 lookup")
				if isinstance(obj, PlayerObject):
					self.setCamera3rdPerson(x, z, obj.getViewDirection())

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
	# Renders the objects in the current map to OpenGL and ground where needed.
	#
	def renderAllObjects(self):
		# Display all RenderObjects in the map
		for z in range(len(self.__map)):
			for x in range(len(self.__map[0])):
				obj = self.__map[z][x]
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
	# Sets the camera to the correct position depending on where the player is
	#
	def setCamera3rdPerson(self, x, z, direction):
		dY = 1
		dBack = 3

		# initialize vars
		playerV = [x,0,z] # player position
		eyeV    = playerV[:] # cam position (moving it starts at the player)
		centerV = playerV[:] # lookat point (is player)
		upV     = [0,1,0] # up vector

		eyeV[1] += dY

		if direction == PlayerObject.NORTH:
			eyeV[2] += dBack
		elif direction == PlayerObject.EAST:
			eyeV[0] -= dBack
		elif direction == PlayerObject.SOUTH:
			eyeV[2] -= dBack
		elif direction == PlayerObject.WEST:
			eyeV[0] += dBack

		self.setCameraPosition(eyeV, centerV, upV)


	#
	# Moves the camera to the desired absolute position in space.
	#
	# @param x : The x-coordinate of the player to see in third-person.
	# @param z : The z-coordinate of the player to see in third-person.
	# @param direction : The direction the player to see in third-person is
	# 					 looking in.
	#
	def setCameraPosition(self, eyeV, centerV, upV):
		print("Camera at pos : " +
			  str(eyeV[0]) + ":" + str(eyeV[1]) + ":" + str(eyeV[2]) + " | " +
			  str(centerV[0]) + ":" + str(centerV[1]) + ":" + str(centerV[2]))

		gluLookAt(eyeV[0] + .5, eyeV[1] + .5, eyeV[2] + .5,
				  centerV[0] + .5, centerV[1] + .5, centerV[2] + .5,
				  upV[0], upV[1], upV[2])


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
