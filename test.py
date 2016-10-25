from Engine import *
from classes.RenderObject import *

import pygame

# start code

leftCube = RenderObject()
middleCube = RenderObject()
rightCube = RenderObject()

my_map = (
	(None, None, None),
	(leftCube, middleCube, rightCube),
	(None, None, None)
	)

engine = Engine((1000, 400), my_map)
engine.startUp()

engine.render()

my_map = (
	(leftCube, None, None),
	(None, middleCube, None),
	(None, None, rightCube)
	)
engine.setMap(my_map)

engine.render()

# move this into engine "somehow"
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

	pygame.time.wait(100)
