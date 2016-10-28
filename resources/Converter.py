STANDARD_PATH_FROM = "resources/originals/"
STANDARD_PATH_TO = "resources/"
STANDARD_NAME = "test"

def main():
	print("This program converts .ply " +
	 	  "files to python-friendly .py files.")
	path_from = input("Please enter the folder/path of the .ply file " +
				 "without ending:\n")
	name = input("Please enter the name of the .ply file (without ending):\n")
	path_to = input("Please enter the wished path to the to-be-created .py-file\n")

	if path_from == "":
		path_from = STANDARD_PATH_FROM
	if name == "":
		name = STANDARD_NAME
	if path_to == "":
		path_to = STANDARD_PATH_TO

	n_ply = path_from + name + ".ply"
	n_py  = path_to   + name + ".py"

	print("You selected to convert '" + name + "'.")
	print("The file '" + n_ply + "' will be used.")

	print("Converting file...")

	output = ""

	# -----------------------------------------------------

	# open .ply-file read-only
	f_ply = open(n_ply, 'r')

	# get number of vertices and faces and loop through header
	num_verts = 0
	num_faces = 0
	line = ""
	while line != "end_header\n":
		line = f_ply.readline()
		if line[0:15] == "element vertex ":
			num_verts = int(line[15:])
		if line[0:13] == "element face ":
			num_faces = int(line[13:])

	# append all vertices to plyVerts
	plyVerts = []
	for i in range(num_verts):
		line = f_ply.readline()[:-1].split()
		# split vertices and colors
		pair = [[int(line[0]), int(line[1]), int(line[2])],
				[int(line[3]), int(line[4]), int(line[5])]]
		plyVerts.append(pair)

	# append all faces to plyFaces and remove preceding "4 "
	plyFaces = []
	for i in range(num_faces):
		# convert to array
		face = f_ply.readline()[2:-1].split()
		# convert strings to integers
		for i, v in enumerate(face):
			face[i] = int(v)
		# append to face-list
		plyFaces.append(face)

	# find position of cubes
	cubes = []
	for num_cube in range(num_faces):
		cubes.append(plyVerts[plyFaces[num_cube][0]])

	allColors = []
	for cube in cubes:
		# convert 0-255 to 0-1
		cube[1][0] = float(cube[1][0]) / 255 # red
		cube[1][1] = float(cube[1][1]) / 255 # green
		cube[1][2] = float(cube[1][2]) / 255 # blue

		allColors.append(cube[1])
		cube[1] = len(allColors) - 1 # last index - the just added color

	# save each unique color only once and save all indizes that refer to that
	# color in a seperate array
	reducedColors = []
	cubeColorPairs = []
	for iCube, color in enumerate(allColors):
		try:
			iReduced = reducedColors.index(color)

			# color exists already
			cubeColorPairs[iReduced].append(iCube)
		except ValueError:
			# color does not exist yet
			reducedColors.append(color)
			cubeColorPairs.append([iCube])


	# put index of color in face, not color itself
	for iColor, pair in enumerate(cubeColorPairs):
		for iCube in pair:
			cubes[iCube][1] = iColor

	for iCube, cube in enumerate(cubes):
		cubes[iCube] = [
			cube[0][0],
			cube[0][1],
			cube[0][2],
			cube[1],
			]

	# -----------------------------------------------------

	output += "cubes = [\n\t"
	output += ",\n\t".join(map(str, cubes))
	output += "]\n\ncolors = [\n\t"
	output += ",\n\t".join(map(str, reducedColors))
	output += "]"

	# write output to .py file
	print("Writing '" + n_py + "'...")
	f_py = open(n_py, 'w')
	f_py.write(output)
	print("Done.")

main()
