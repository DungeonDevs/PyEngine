from .RenderObject import RenderObject

import importlib

class LoadedObject(object):


	def __init__(self, filename, scale = 64, percentageOffsets = (0,0,0)):
		self.setScale(scale)
		self.setPercentageOffsets(percentageOffsets)
		self.setFilename(filename) # self.__updateRenderObjects()

		self.setGroundNecessary(True)
		self.setRenderAsEdges(False)


	def render(self, x, y, z):
		print("Render LoadedObject")
		for obj in self.__renderObjects:
			print(" - Render RenderObject")
			offsets = self.getPercentageOffsets()
			pos = [x + offsets[0],
				   y + offsets[1],
				   z + offsets[2]]
			print(" -  - at pos: " + str(pos))
			obj.render(pos[0],
					   pos[1],
					   pos[2])


	def setFilename(self, filename):
		self.__filename = filename
		self.__updateRenderObjects()


	def getFilename(self):
		return self.__filename


	def setScale(self, scale):
		self.__scale = scale


	def getScale(self):
		return self.__scale


	def setPercentageOffsets(self, offsets):
		self.__percentageOffsets = offsets


	def getPercentageOffsets(self):
		return self.__percentageOffsets


	def setGroundNecessary(self, necessary):
		self.__groundNecessary = necessary


	def getGroundNecessary(self):
		return self.__groundNecessary


	def setRenderAsEdges(self, renderAsEdges):
		self.__renderAsEdges = renderAsEdges

		for obj in self.__renderObjects:
			obj.setRenderAsEdges(renderAsEdges)


	def getRenderAsEdges(self):
		return self.__renderAsEdges


	def __updateRenderObjects(self):
		cubes  = []
		colors = []

		print("loading data from file : " + self.getFilename())
		varfile = importlib.import_module("resources." + self.getFilename())

		cubes  = varfile.cubes
		colors = varfile.colors

		print("cubes: " + str(cubes))
		print("colors: " + str(colors))

		self.__renderObjects = []
		for cube in cubes:
			print("adding cube to list")
			c_obj = RenderObject.createOneColorCube(colors[cube[3]])
			c_obj.setScale(self.getScale())
			print("with color " + str(colors[cube[3]]))
			offsets = [float(cube[0]) / self.getScale(),
					   float(cube[1]) / self.getScale(),
					   float(cube[2]) / self.getScale()]
			c_obj.setPercentageOffsets(offsets)
			print("With offsets" + str(offsets))

			self.__renderObjects.append(c_obj)
			print("\n")
		print("Done with all cubes")
