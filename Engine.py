import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

class Engine(object):


	def __init__(self, display = (800, 600), p_map = ((None, None, None), (None, None, None), (None, None, None))):
		self.__map = p_map
		self.__display = display


	def startUp(self):
		pygame.init()
		pygame.display.set_mode(self.__display, DOUBLEBUF|OPENGL)

		# set the perspective
		fieldOfView = 45 # degrees
		aspectRatio = self.__display[0] / self.__display[1]
		gluPerspective(fieldOfView, aspectRatio, 0.1, 50.0)

		# x, y, z -> y is fixed - x, -2, y (in-game)
		glTranslatef(-1, -1, -10)
		glRotatef(0, 0, 0, 0)


	def render(self):

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		for x in range(len(self.__map)):
			for z in range(len(self.__map[0])):
				obj = self.__map[x][z]
				if not obj == None:
					obj.render(x, 0, z)

					if obj.getGroundNecessary(): # render ground under object
												 # if needed
						self.getGround().render(x, -1, z)
				else: # render ground underneath if no object
					self.getGround().render(x, -1, z)

		#
		# update is better, but does not work.
		# flip sadly produces an error on closing, but that is acceptable,
		# as the user does not notice this.
		#
		# pygame.display.update()
		pygame.display.flip()


	def setMap(self, p_map):
		self.__map = p_map


	def getGround(self):
		return self.__ground


	def setGround(self, ground):
		self.__ground = ground
