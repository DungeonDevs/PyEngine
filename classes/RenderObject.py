from OpenGL.GL import *

class RenderObject(object):


	STANDARD_CUBE_VERTS = (
		(0.5, -0.5, -0.5),
		(0.5, 0.5, -0.5),
		(-0.5, 0.5, -0.5),
		(-0.5, -0.5, -0.5),
		(0.5, -0.5, 0.5),
		(0.5, 0.5, 0.5),
		(-0.5, -0.5, 0.5),
		(-0.5, 0.5, 0.5)
		)


	STANDARD_CUBE_EDGES = (
		(0, 1),
		(0, 3),
		(0, 4),
		(2, 1),
		(2, 3),
		(2, 7),
		(6, 3),
		(6, 4),
		(6, 7),
		(5, 1),
		(5, 4),
		(5, 7)
		)


	def __init__(self, vertices = STANDARD_CUBE_VERTS, edges = STANDARD_CUBE_EDGES):
		self.__vertices = vertices
		self.__edges = edges

		self.__groundNecessary = True


	def render(self, x, y, z):
		glBegin(GL_LINES)

		print("RenderObject at " + str(x) + " : " + str(z))

		for edge in self.__edges:
			for vertex in edge:
				glVertex3fv((self.__vertices[vertex][0] + x, self.__vertices[vertex][1] + y, self.__vertices[vertex][2] + z))

		glEnd()


	def getGroundNecessary(self):
		return self.__groundNecessary


	def setGroundNecessary(self, isNecessary):
		self.__groundNecessary = isNecessary


	def getVertices(self):
		return self.__vertices


	def setVertices(self, vertices):
		self.__vertices = vertices


	def getEdges(self):
		return self.__edges


	def setEdges(self, edges):
		self.__edges = edges
