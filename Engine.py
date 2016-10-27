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
					# self.setCameraPosition(x, z, obj.getViewDirection())
					eyeV    = [0,0,0] # cam position
					centerV = [0,0,0] # lookat point
					upV     = [0,1,0] # up vector
					playerV = [x,0,z] # player position

					if not self.stopper:
						eyeV[0] = playerV[0] + 7.5
						eyeV[1] = playerV[1] + 3
						eyeV[2] = playerV[2] + 0.5
						centerV[0] = playerV[0] + 0.5
						centerV[1] = playerV[1] + 1
						centerV[2] = playerV[2] + 0.5

						self.stopper = True
					else:
						eyeV[0] = playerV[0] + 7.5
						eyeV[1] = playerV[1] + 3
						eyeV[2] = playerV[2] + 0.5
						centerV[0] = playerV[0] + 0.5
						centerV[1] = playerV[1] + 1
						centerV[2] = playerV[2] + 0.5

					# if obj.getViewDirection() == PlayerObject.NORTH:
					# elif obj.getViewDirection() == PlayerObject.SOUTH:
					# elif obj.getViewDirection() == PlayerObject.EAST:
					# elif obj.getViewDirection() == PlayerObject.WEST:

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
		# eyeV[0] = eyeV[0] - self.__camera[0][0]
		# eyeV[1] = eyeV[1] - self.__camera[0][1]
		# eyeV[2] = eyeV[2] - self.__camera[0][2]
		#
		# center[0] = center[0] - self.__camera[1][0]
		# center[1] = center[1] - self.__camera[1][1]
		# center[2] = center[2] - self.__camera[1][2]
		#
		# upV[0] = upV[0] - self.__camera[2][0]
		# upV[1] = upV[1] - self.__camera[2][1]
		# upV[2] = upV[2] - self.__camera[2][2]

		self.__camera = ((eyeV[0], eyeV[1], eyeV[2]),
						 (centerV[0], centerV[1], centerV[2]))
		print("Camera at pos : " +
			  str(eyeV[0]) + ":" + str(eyeV[1]) + ":" + str(eyeV[2]) + " | " +
			  str(centerV[0]) + ":" + str(centerV[1]) + ":" + str(centerV[2]))

		gluLookAt(eyeV[0], eyeV[1], eyeV[2],
				  centerV[0], centerV[1], centerV[2],
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
