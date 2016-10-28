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

	# append color to faces
	for face in plyFaces:
		face.append(plyVerts[face[0]][1])

	# remove color from vertices
	for i, vert in enumerate(plyVerts):
		plyVerts[i] = [vert[0][0],
						vert[0][1],
						vert[0][2]]

	# put colors in seperate array and reference them in faces
	allColors = []
	for face in plyFaces:
		# convert 0-255 to 0-1
		face[4][0] = float(face[4][0]) / 255 # red
		face[4][1] = float(face[4][1]) / 255 # green
		face[4][2] = float(face[4][2]) / 255 # blue

		allColors.append(face[4])
		face[4] = len(allColors) - 1 # last index - the just added color

	# save each unique color only once and save all indizes that refer to that
	# color in a seperate array
	reducedColors = []
	faceColorPairs = []
	for iFace, color in enumerate(allColors):
		try:
			iReduced = reducedColors.index(color)

			# color exists already
			faceColorPairs[iReduced].append(iFace)
		except ValueError:
			# color does not exist yet
			reducedColors.append(color)
			faceColorPairs.append([iFace])


	# put index of color in face, not color itself
	for iColor, pair in enumerate(faceColorPairs):
		for iFace in pair:
			plyFaces[iFace][4] = iColor

	# make list of unique vertices
	reducedVerts = []
	for iVert, vert in enumerate(plyVerts):
		try:
			iList = reducedVerts.index(vert)
			# vert already in list
		except ValueError:
			# vert not in list yet
			reducedVerts.append(vert)

	# put reduced vertex index in face
	for iFace, face in enumerate(plyFaces):
		# do this for each vertex in face - remember, the last is color
		for vertNum in range(4):
			# get vertex by old index
			vert = plyVerts[face[vertNum]]
			# get new index by vert
			iNew = reducedVerts.index(vert)
			# set new index in plyFaces
			plyFaces[iFace][vertNum] = iNew


	# the vertex parts have to be changed, because they are differently
	# interpreted in OpenGL and MagicaVoxel
	# for i, vert in enumerate(reducedVerts):
	# 	reducedVerts[i][0] = vert[0]
	# 	reducedVerts[i][1] = vert[1]
	# 	reducedVerts[i][2] = vert[2]


	# -----------------------------------------------------

	# test-outputs
	# output += "\n".join(map(str, plyVerts))
	# output += "\n".join(map(str, allColors))
	# output += "\n".join(map(str, reducedColors))
	# output += str(faceColorIndexPairs)
	# output += "\n".join(map(str, plyFaces))

	#
	# The vertices are now saved in reducedVerts
	# The faces are now saved in plyFaces
	# The colors are now saved in reducedColors
	#

	output += ("vertices = [" +
				str(reducedVerts)[1:-1].replace("[", "(").replace("]", ")") +
				"]\n")
	output += ("faces = [" +
				str(plyFaces)[1:-1].replace("[", "(").replace("]", ")") +
				"]\n")
	output += ("colors = [" +
				str(reducedColors)[1:-1].replace("[", "(").replace("]", ")") +
				"]\n")

	# write output to .py file
	print("Writing '" + n_py + "'...")
	f_py = open(n_py, 'w')
	f_py.write(output)
	print("Done.")


main()
