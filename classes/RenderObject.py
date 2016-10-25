from OpenGL.GL import *

class RenderObject(object):


	STANDARD_VERTS = (
		(0.5, -0.5, -0.5),
		(0.5, 0.5, -0.5),
		(-0.5, 0.5, -0.5),
		(-0.5, -0.5, -0.5),
		(0.5, -0.5, 0.5),
		(0.5, 0.5, 0.5),
		(-0.5, -0.5, 0.5),
		(-0.5, 0.5, 0.5)
		)


	STANDARD_EDGES = (
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

	STANDARD_FACES = (
		(0, 1, 2, 3),
		(3, 2, 7, 6),
		(6, 7, 5, 4),
		(4, 5, 1, 0),
		(1, 5, 7, 2),
		(4, 0, 3, 6)
		)

	STANDARD_COLOR = ( 156 / 255, 18 / 255, 160 / 255 )


	def __init__(self, vertices = STANDARD_VERTS, edges = STANDARD_EDGES, faces = STANDARD_FACES, color = STANDARD_COLOR):
		self.__vertices = vertices
		self.__edges = edges
		self.__faces = faces
		self.__color = color

		self.__groundNecessary = True
		self.__renderAsEdges = False


	def render(self, x, y, z):
		print("RenderObject at " + str(x) + " : " + str(z))

		if self.__renderAsEdges:
			glBegin(GL_LINES)

			glColor3fv(self.__color)

			for edge in self.__edges:
				for vertex in edge:
					glVertex3fv((self.__vertices[vertex][0] + x, self.__vertices[vertex][1] + y, self.__vertices[vertex][2] + z))

			glEnd()
		else:
			glBegin(GL_QUADS)

			glColor3fv(self.__color)

			for face in self.__faces:
				for vertex in face:
					glVertex3fv((self.__vertices[vertex][0] + x, self.__vertices[vertex][1] + y, self.__vertices[vertex][2] + z))

			glEnd()


	def getGroundNecessary(self):
		return self.__groundNecessary


	def setGroundNecessary(self, isNecessary = True):
		self.__groundNecessary = isNecessary


	def getRenderAsEdges(self):
		return self.__renderAsEdges


	def setRenderAsEdges(self, renderAsEdges = True):
		self.__renderAsEdges = renderAsEdges


	def getVertices(self):
		return self.__vertices


	def setVertices(self, vertices):
		self.__vertices = vertices


	def getEdges(self):
		return self.__edges


	def setEdges(self, edges):
		self.__edges = edges


	def getFaces(self):
		return self.__faces


	def setEdges(self, faces):
		self.__faces = faces


	def getColor(self):
		return self.__color


	def setColor(self, color):
		self.__color = color
