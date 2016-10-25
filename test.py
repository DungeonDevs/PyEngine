from Engine import *
from classes.RenderObject import *
from classes.PlayerObject import *

import pygame

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
player.setColor((100/255, 200/255, 100/255))

my_map = (
	(leftCube, None, None),
	(None, middleCube, None),
	(None, player, rightCube)
	)

engine = Engine((1000, 400), my_map)

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

	pygame.time.wait(100)
