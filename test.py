from Engine import *
from classes.RenderObject import *
from classes.PlayerObject import *

import pygame

#------------------------------------------------
# start code

# create three cubes as objects in the game
leftCube = RenderObject()
leftCube.setGroundNecessary(False)
leftCube.setRenderAsEdges()

middleCube = RenderObject()
middleCube.setGroundNecessary(False)
# middleCube.setRenderAsEdges()
middleCube.setScale(64)
middleCube.loadObjectFromPlyToPy("test")
middleCube.setPercentageOffsets((.5, 0, .5))

rightCube = RenderObject()
rightCube.setGroundNecessary(False)
rightCube.setRenderAsEdges()

# create a player
player = PlayerObject()
player.setRenderAsEdges()
player.setViewDirection(PlayerObject.NORTH)
# player.setColors([(100/255, 200/255, 100/255), (1, 1, 1)])

#--------------------------------------
# create map
my_map = (
	(leftCube, None, None),
	(None, middleCube, None),
	(None, None, rightCube),
	(None, None, None),
	(None, None, None),
	(None, None, None),
	(None, player, None),
	)
#--------------------------------------

# create engine object
engine = Engine((1000, 800), my_map)
engine.debug = True # to show axis

# sets the ground under each field where ground needs to be shown
ground = RenderObject()
# ground.setColors([(150/255, 75/255, 0), (0, 0, 0)])
engine.setGround(ground)

# start engine and render first screen
engine.stopper = False # for debugging
engine.startUp()
engine.render()

my_map = (
	(leftCube, None, None),
	(None, middleCube, None),
	(None, None, rightCube),
	(None, None, None),
	(None, None, None),
	(None, player, None),
	(None, None, None),
	)
engine.setMap(my_map)
pygame.time.wait(1000)
engine.render()
pygame.time.wait(1000)

while True:
	# TODO: give engine this functionality
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

	pygame.time.wait(1000)
