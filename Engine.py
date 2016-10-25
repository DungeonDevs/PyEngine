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

		glTranslatef(-1, -2, -10)
		glRotatef(0, 0, 0, 0)


	def render(self):

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		for y in range(len(self.__map)):
			for x in range(len(self.__map[0])):
				obj = self.__map[x][y]
				if not obj == None:
					obj.render(x, y)
					#if obj

		#
		# update is better, but does not work.
		# flip sadly produces an error on closing, but that is acceptable,
		# as the user does not notice this.
		#
		# pygame.display.update()
		pygame.display.flip()


	def setMap(self, p_map):
		self.__map = p_map
