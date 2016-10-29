from Engine import *
from classes.RenderObject import *
from classes.PlayerObject import *
from classes.LoadedObject import *

import pygame

# -------------------------------------------
# create a player
player = PlayerObject()
player.setRenderAsEdges()
player.setViewDirection(PlayerObject.EAST)
# player.setColors([(100/255, 200/255, 100/255), (1, 1, 1)])

# -------------------------------------------
# create a ground
ground = RenderObject()
# ground.setColors([(150/255, 75/255, 0), (0, 0, 0)])

# -------------------------------------------
# create three cubes

cube1 = RenderObject()
cube1.setGroundNecessary(False)
cube1.setRenderAsEdges()

cube2 = RenderObject()
cube2.setGroundNecessary(False)
cube2.setRenderAsEdges()

cube3 = RenderObject()
cube3.setGroundNecessary(False)
cube3.setRenderAsEdges()

# -------------------------------------------
# create object from file
loadedObj = LoadedObject("block", 16)
loadedObj.setPercentageOffsets((.5, 0, -.5))
# loadedObj.setScale(2)

# -------------------------------------------
# create engine object
engine = Engine((1500, 1000))
# engine.debug = True # to show axis

# -------------------------------------------
# set ground
engine.setGround(ground)

# -------------------------------------------
# start engine
engine.startUp()

# -------------------------------------------
# create map
my_map = (
	(None, None, None, cube1, cube2, cube3),
	(loadedObj, None, None, None, None, None)
	)

# -------------------------------------------
# render map
engine.setMap(my_map)
engine.setPlayerPosInfo(0, 1, PlayerObject.NORTH)
engine.render()

# pygame.time.wait(1000)
#
# # -------------------------------------------
# # create map
# my_map = (
# 	(None, loadedObj, None, cube1, cube2, cube3),
# 	(None, player, None, None, None, None, None)
# 	)
#
# # -------------------------------------------
# # render map
# engine.setMap(my_map)
# engine.render()
#
# pygame.time.wait(1000)
#
# # -------------------------------------------
# # create map
# my_map = (
# 	(None, loadedObj, None, cube1, cube2, cube3),
# 	(None, None, player, None, None, None, None)
# 	)
#
# # -------------------------------------------
# # render map
# engine.setMap(my_map)
# engine.render()



# -------------------------------------------
# keep program alive until close-event
while True:
	# TODO: give engine this functionality
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

	pygame.time.wait(100)
