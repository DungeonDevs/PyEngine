from OpenGL.GL import *

#
# A class for all objects that can be rendered into the "world". It saves
# vertices, edges and faces of the object and contains a render-method to make
# it visible.
#
# Inherit this class for things that should be shown as objects. (Unless it's
# the player - the player should inherit PlayerObject which inherits this class
# already).
#
class RenderObject(object):


	#
	# The vertices needed to create a simple cube ( 1 x 1 x 1 )
	#
	STANDARD_VERTS = (
		(1, 0, 0),
		(1, 1, 0),
		(0, 1, 0),
		(0, 0, 0),
		(1, 0, 1),
		(1, 1, 1),
		(0, 0, 1),
		(0, 1, 1)
		)


	#
	# The vertex-combinations needed to create the edges of a cube, if the order
	# from above is used. The last is the color to be used for the edge.
	#
	STANDARD_EDGES = (
		(0, 1, 0),
		(0, 3, 0),
		(0, 4, 0),
		(2, 1, 0),
		(2, 3, 0),
		(2, 7, 0),
		(6, 3, 0),
		(6, 4, 0),
		(6, 7, 0),
		(5, 1, 0),
		(5, 4, 0),
		(5, 7, 0)
		)


	#
	# The vertex-combinations needed to create the faces of a cube, if the order
	# from above is used. The last is the color to be used for the face.
	#
	STANDARD_FACES = (
		(0, 1, 2, 3, 1),
		(3, 2, 7, 6, 2),
		(6, 7, 5, 4, 3),
		(4, 5, 1, 0, 4),
		(1, 5, 7, 2, 5),
		(4, 0, 3, 6, 6)
		)

	STANDARD_NORMALS = (
		(0, 0, -1),
		(-1, 0, 0),
		(0, 0, 1),
		(1, 0, 0),
		(0, 1, 0),
		(0, -1, 0)
		)


	#
	# Some default color to use for the object if not differently defined.
	#
	STANDARD_COLORS = (
		(1, 1, 1),
		(1, 0, 0),
		(0, 1, 0),
		(0, 0, 1),
		(1, 1, 0),
		(0, 1, 1),
		(1, 0, 1)
		)


	#
	# The constructor for an object that should be rendered on-screen.
	#
	# @param vertices : the vertices needed to describe this object (default for
	# 					a 1x1x1 cube)
	# @param edges : the vertex-combinations needed to describe the edges of
	# 				 this object (default for a cube)
	# @param faces : the vertex-combinations needed to describe the faces of
	# 				 this object (default for a cube)
	# @param colors : the colors to render this object in.
	#
	def __init__(self, vertices = STANDARD_VERTS,
					   edges    = STANDARD_EDGES,
					   faces    = STANDARD_FACES,
					   colors   = STANDARD_COLORS,
					   normals  = STANDARD_NORMALS):
		self.setVertices(vertices)
		self.setEdges(edges)
		self.setFaces(faces)
		self.setColors(colors)
		self.setNormals(normals)

		self.setScale(1)
		self.setPercentageOffsets([0, 0, 0])

		self.setGroundNecessary(True)
		self.setRenderAsEdges(False)


	#
	# The necessary PyOpenGL code needed to render this object at the given
	# coords.
	#
	# @param x : The x-coord at which the object shall be rendered
	# @param y : The y-coord at which the object shall be rendered
	# @param z : The z-coord at which the object shall be rendered
	#
	def render(self, x, y, z):
		if self.__renderAsEdges: # the object is set to render only it's edges
			glBegin(GL_LINES) # set the GL-mode to line-drawing

			for edge in self.getEdges():
				glColor3fv(self.getColors()[edge[2]])
				edge = edge[:-1]
				for iVertex in edge:
					self.__drawVertexAtPosition(self.getVertices()[iVertex],
												x, y, z)

			glEnd()
		else: # the object is set to render only it's faces
			glBegin(GL_QUADS) # set the GL-mode to rectangle-drawing

			for iFace, face in enumerate(self.getFaces()):
				glColor3fv(self.getColors()[face[4]])
				face = face[:-1]
				for iVertex in face:
					self.__drawVertexNormalAtPosition(
						self.getVertices()[iVertex],
						self.getNormals()[iFace],
						x, y, z)

			glEnd()


	def __drawVertexAtPosition(self, vertex, x, y, z):
		drawVert = [0,0,0]
		drawVert[0] = (vertex[0] / self.__scale +
						self.getPercentageOffsets()[0] + x)
		drawVert[1] = (vertex[1] / self.__scale +
						self.getPercentageOffsets()[1] + y)
		drawVert[2] = (vertex[2] / self.__scale +
						self.getPercentageOffsets()[2] + z)

		glVertex3fv(drawVert)


	def __drawVertexNormalAtPosition(self, vertex, normal, x, y, z):
		drawVert = [0,0,0]
		drawVert[0] = (vertex[0] / self.__scale +
						self.getPercentageOffsets()[0] + x)
		drawVert[1] = (vertex[1] / self.__scale +
						self.getPercentageOffsets()[1] + y)
		drawVert[2] = (vertex[2] / self.__scale +
						self.getPercentageOffsets()[2] + z)

		glNormal3fv(normal)
		glVertex3fv(drawVert)


	def setScale(self, scale):
		self.__scale = scale


	def getScale(self):
		return self.__scale


	def setPercentageOffsets(self, offsets):
		self.__percentageOffsets = offsets


	def getPercentageOffsets(self):
		return self.__percentageOffsets


	#
	# A boolean whether there has to be ground rendered underneath this object.
	#
	def getGroundNecessary(self):
		return self.__groundNecessary


	#
	# Set whether default ground should be rendered underneath this object.
	#
	# @param isNecessary : If set to true, ground will be rendered (default).
	# 					   If set to false, ground will not be rendered.
	#
	def setGroundNecessary(self, isNecessary = True):
		self.__groundNecessary = isNecessary


	#
	# A boolean whether this object should only be rendered as it's edges
	# (true), or whether the faces should be rendered (false).
	#
	def getRenderAsEdges(self):
		return self.__renderAsEdges


	#
	# Set whether this object should be rendered as only it's edges or as it's
	# faces.
	#
	# @param renderAsEdges : If True, the object will only render as edges
	# 						 (default).
	# 						 If False, it will render as it's faces.
	#
	def setRenderAsEdges(self, renderAsEdges = True):
		self.__renderAsEdges = renderAsEdges


	#
	# A list of all 3D vertices needed to describe this object.
	#
	def getVertices(self):
		return self.__vertices


	#
	# Set a list of 3D vertices that is needed to describe this object.
	#
	# @param vertices : The vertices needed to describe this object.
	#
	def setVertices(self, vertices):
		self.__vertices = vertices


	#
	# A list of vertex-combinations needed to describe the edges of this object,
	# using its defined vertices.
	#
	def getEdges(self):
		return self.__edges


	#
	# Set a list of vertex-combinations that is needed to describe the edges of
	# this object.
	#
	# @param edges : A list of vertex-indizes referring to this object's
	# 				 vertices-list, describing which vertex-combinations form an
	# 				 edge of this object.
	#
	def setEdges(self, edges):
		self.__edges = edges


	#
	# A list of vertex-combinations needed to describe the faces of this object.
	#
	def getFaces(self):
		return self.__faces


	#
	# Set a list of vertex-combinations that is needed to describe the faces of
	# this object.
	#
	# @param faces : A list of vertex-indizes referring to this object's
	# 				 vertices-list, describing which vertex-combinations form a
	# 				 face of this object.
	def setFaces(self, faces):
		self.__faces = faces


	#
	# A list of numbers in the range of 0 to 1 in form of RGB describing the
	# color this object is rendered in.
	#
	def getColors(self):
		return self.__colors


	#
	# Set the colors this object is rendered in.
	#
	# @param colors : A list of 3 numbers in the range 0 to 1, in order RGB,
	# 				  describing the color this object shall be rendered in.
	#
	def setColors(self, colors):
		self.__colors = colors


	def getNormals(self):
		return self.__normals


	def setNormals(self, normals):
		self.__normals = normals


	@staticmethod
	def createOneColorCube(color):
		vertices = (
			(1, 0, 0),
			(1, 1, 0),
			(0, 1, 0),
			(0, 0, 0),
			(1, 0, 1),
			(1, 1, 1),
			(0, 0, 1),
			(0, 1, 1))
		edges = (
			(0, 1, 0),
			(0, 3, 0),
			(0, 4, 0),
			(2, 1, 0),
			(2, 3, 0),
			(2, 7, 0),
			(6, 3, 0),
			(6, 4, 0),
			(6, 7, 0),
			(5, 1, 0),
			(5, 4, 0),
			(5, 7, 0))
		faces = (
			(0, 1, 2, 3, 0),
			(3, 2, 7, 6, 0),
			(6, 7, 5, 4, 0),
			(4, 5, 1, 0, 0),
			(1, 5, 7, 2, 0),
			(4, 0, 3, 6, 0))

		return RenderObject(vertices, edges, faces, [color])
