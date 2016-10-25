from Engine import *
from classes.RenderObject import *
from classes.PlayerObject import *

import pygame

# start code

leftCube = RenderObject()
leftCube.setGroundNecessary(False)

middleCube = RenderObject()
middleCube.setGroundNecessary(False)

rightCube = RenderObject()
rightCube.setGroundNecessary(False)

player = PlayerObject()

my_map = (
	(None, None, None),
	(leftCube, middleCube, rightCube),
	(None, player, None)
	)

<<<<<<< HEAD
engine = Engine((1200, 800), my_map)

# sets the ground under each field where ground needs to be shown
ground = RenderObject()
engine.setGround(ground)

=======
engine = Engine((1000, 400), my_map)
>>>>>>> 1ba60d9f579c6e69865015cb155aae1d33ece370
engine.startUp()

engine.render()

my_map = (
	(leftCube, None, None),
	(None, middleCube, None),
	(None, player, rightCube)
	)
engine.setMap(my_map)

engine.render()

# move this into engine "somehow"
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

	pygame.time.wait(100)
