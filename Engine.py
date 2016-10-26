import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from classes.PlayerObject import *

class Engine(object):


	# the three axis - helpful for debugging and visualization.
	__axis = (
		# x-axis
		RenderObject(
			((-200,0,0), (200,0,0)),
			((0,1), (1,0)),
			(),
			(1,0,0) # red
			),
		# y-axis
		RenderObject(
			((0,-200,0), (0,200,0)),
			((0,1), (1,0)),
			(),
			(0,1,0) # green
			),
		# z-axis
		RenderObject(
			((0,0,-200), (0,0,200)),
			((0,1), (1,0)),
			(),
			(0,0,1) # blue
			)
		)


	def __init__(self, display = (800, 600), p_map = ((None, None, None), (None, None, None), (None, None, None))):
		# initialize vars by params
		self.__map = p_map
		self.__display = display

		# initialize vars by standards
		self.__cameraPosition = (0, 0, 0)
		self.__rotation = PlayerObject.NORTH


	def startUp(self):
		pygame.init()
		pygame.display.set_mode(self.__display, DOUBLEBUF|OPENGL)

		# set the perspective
		fieldOfView = 45 # degrees
		aspectRatio = self.__display[0] / self.__display[1]
		gluPerspective(fieldOfView, aspectRatio, 0.1, 50.0)

		self.setCameraPosition(0, 0, 0)
		self.turnCameraInDirection(PlayerObject.NORTH)


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

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		camPos = self.getCameraPosition()

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


	def setCameraPosition(self, x, y, z):
		print("Set Camera to " + str(x) + " : " + str(y) + " : " + str(z))

		# reset camera to 0, 0, 0
		oldPos = self.getCameraPosition()
		glTranslatef(-oldPos[0], -oldPos[1], -oldPos[2]) # minus 'cause it moves back

		# move camera to given coords
		glTranslatef(x, y, z)


	def getCameraPosition(self):
		return self.__cameraPosition


	def turnCameraInDirection(self, direction):
		direction = direction % 4 # make sure it's a valid direction
		print("Turning camera in direction: " + str(direction))


	def setMap(self, p_map):
		self.__map = p_map


	def getGround(self):
		return self.__ground


	def setGround(self, ground):
		self.__ground = ground
