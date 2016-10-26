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
middleCube.setRenderAsEdges()

rightCube = RenderObject()
rightCube.setGroundNecessary(False)
rightCube.setRenderAsEdges()

# create a player
player = PlayerObject()
player.setViewDirection(PlayerObject.NORTH)
player.setColor((100/255, 200/255, 100/255))

#--------------------------------------
# create map
my_map = (
	(leftCube, None, None),
	(None, middleCube, None),
	(None, None, rightCube),
	(None, None, None),
	(None, None, None),
	(None, None, None),
	(None, None, None),
	(None, None, None),
	(None, None, None),
	(None, None, None),
	(None, None, None),
	(None, None, None),
	(None, player, None),
	)
#--------------------------------------

# create engine object
engine = Engine((1800, 1000), my_map)
engine.debug = True # to show axis

# sets the ground under each field where ground needs to be shown
ground = RenderObject()
ground.setColor((150/255, 75/255, 0))
engine.setGround(ground)

# start engine and render first screen
engine.startUp()
engine.render()

# move this into engine "somehow"
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

	# glRotatef(1, 1, 0, 0) # x
	# glRotatef(1, 0, 1, 0) # y
	# glRotatef(1, 0, 0, 1) # z
	# engine.render()

	pygame.time.wait(10)
