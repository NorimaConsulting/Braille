import numpy as np
import copy
import struct
import sys
import datetime
import os
from stl import mesh

import BrailleToArray as b_to_a

current_directory = os.path.join(os.path.dirname(__file__))

class BraillePlaque:
	def __init__( 	self,
					text,
					plaque_length, plaque_width, plaque_height,
					col_space, row_space,
					x_space, y_space,
					dot_diameter,
					dot_stl_path=(current_directory + '/DefaultMeshes/dot.stl'), 
					plaque_stl_path=(current_directory + '/DefaultMeshes/plaque.stl'), 
					grid_stl_path=(current_directory + '/DefaultMeshes/grid.stl') ):

		self.text = text
		self.plaque_length = plaque_length
		self.plaque_width = plaque_width
		self.plaque_height = plaque_height
		self.col_space = col_space
		self.row_space = row_space
		self.x_space = x_space
		self.y_space = y_space
		self.dot_diameter = dot_diameter
		self.dot_stl_path = dot_stl_path
		self.plaque_stl_path = plaque_stl_path
		self.grid_stl_path = grid_stl_path

		self.dot_mesh = None
		self.plaque_mesh = None
		self.grid_mesh = None

		# create braille sequences
		words = self.text.split()
		max_length = max([len(x) for x in words])
		character_width = (2 * self.dot_diameter) + x_space

		if (((max_length - 1) * (col_space + character_width)) + character_width) > self.plaque_width:
			raise WordLengthException('Longest braille word extends beyond plaque width')

		self.braille_sequences = []
		curr_sequence = []
		curr_x_offset = 0
		for word in self.text.split():
			curr_x_offset += ((len(word) - 1) * (character_width + col_space)) + character_width
			if curr_x_offset > self.plaque_width:
				sequence_string = " ".join(curr_sequence)
				self.braille_sequences.append(b_to_a.BrailleSequence(sequence_string))

				curr_sequence = [word]
				curr_x_offset = ((len(word) - 1) * (character_width + col_space)) + character_width
			else:
				curr_sequence.append(word)

		sequence_string = " ".join(curr_sequence)
		self.braille_sequences.append(b_to_a.BrailleSequence(sequence_string))

	def create_mesh( self ):
		self._create_sequence_mesh()
		self._create_plaque_mesh()
		self._create_grid_mesh()

		self.combined_mesh = mesh.Mesh(np.concatenate([self.plaque_mesh.data.copy(), self.sequence_mesh.data.copy(), self.grid_mesh.data.copy()]))

	def _create_sequence_mesh( self ):
		if self.dot_mesh == None:
			self.dot_mesh = mesh.Mesh.from_file(self.dot_stl_path)

		self.dot_mesh.points *= self.dot_diameter

		self.sequence_mesh = BrailleSequenceMesh(
										self.braille_sequences,
										self.dot_mesh,
										self.col_space,
										self.row_space,
										self.x_space,
										self.y_space,
										self.dot_diameter ).braille_sequence_mesh

		self.sequence_mesh.z += self.plaque_height

	def _create_plaque_mesh( self ):
		if self.plaque_mesh == None:
			self.plaque_mesh = mesh.Mesh.from_file(self.plaque_stl_path)

		self.plaque_mesh.x *= self.plaque_width
		self.plaque_mesh.y *= self.plaque_length
		self.plaque_mesh.z *= self.plaque_height

	def _create_grid_mesh( self ):
		# create vertical grid lines every 3 millimeters
		
		grid_size = 0.0015
		grid_space = 0.003

		curr_vertical = 0
		vertical_end = self.plaque_length
		curr_horizontal = 0
		horizontal_end = self.plaque_width

		grid_lines = []

		while curr_vertical < (vertical_end - grid_size):
			grid_lines.append(GridLineMesh(self.grid_stl_path, grid_size, self.plaque_width, curr_vertical, True))
			curr_vertical += grid_size + grid_space

		grid_lines.append(GridLineMesh(self.grid_stl_path, grid_size, self.plaque_width, self.plaque_length - grid_size, True))
			
		while curr_horizontal < (horizontal_end - grid_space):
			grid_lines.append(GridLineMesh(self.grid_stl_path, grid_size, self.plaque_length, curr_horizontal, False))
			curr_horizontal += grid_size + grid_space

		grid_lines.append(GridLineMesh(self.grid_stl_path, grid_size, self.plaque_width, self.plaque_width - grid_size, False))
		
		self.grid_mesh = mesh.Mesh(np.concatenate([x.mesh.data for x in grid_lines]))

	def save( self, out_file ):
		self.combined_mesh.save(out_file)

	def to_std_out( self, name="default" ):
		header = '%s (%s) %s %s' % ('numpy-stl', '0.0.0', datetime.datetime.now(), name.encode('ascii'))

		# Make it exactly 80 characters
		header = header[:80].ljust(80, ' ')
		packed = struct.pack('@i', self.combined_mesh.data.size)

		header = self.to_bytes(header)
		packed = self.to_bytes(packed)

		write_bytes = header + packed + self.combined_mesh.data.tobytes()

		sys.stdout.buffer.write(write_bytes)

	def to_bytes( self, data ):
		if isinstance(data, str):
			return bytes(data, 'ascii', 'replace')
		else:
			return data

class BrailleCharacterMesh:
	"""
		BrailleCharacterMesh
			Accepts an BrailleCharacter object and a mesh for a single 'dot'
			and returns a mesh for the passed BrailleCharacter
	"""

	def __init__( self, braille_char, dot_mesh, x_offset, y_offset, x_space, y_space, dot_diameter ):
		self._braille_character_mesh_data = self._create_mesh(braille_char, dot_mesh, x_offset, y_offset, x_space, y_space, dot_diameter)

	@property
	def braille_character_mesh_data( self ):
		return self._braille_character_mesh_data

	def _create_mesh( self, braille_char, dot_mesh, x_offset, y_offset, x_space, y_space, dot_diameter ):
		"""
			internal method _create_mesh

		"""

		meshes = []
		for index, dot in enumerate(braille_char.dot_code):
			if dot == 1:
				new_mesh = mesh.Mesh(dot_mesh.data.copy())

				new_mesh.x += x_offset + ((index >= 3) * x_space)
				new_mesh.y -= y_offset + ((index % 3) * y_space)

				meshes.append(new_mesh)

		return meshes

class BrailleSequenceMesh:
	def __init__( self, braille_sequences, dot_mesh, col_space, row_space, x_space, y_space, dot_diameter ):
		self._braille_sequence_mesh = self._create_sequence_mesh(braille_sequences, dot_mesh, col_space, row_space, x_space, y_space, dot_diameter)

	@property
	def braille_sequence_mesh( self ):
		return self._braille_sequence_mesh

	def _create_sequence_mesh( self, braille_sequences, dot_mesh, col_space, row_space, x_space, y_space, dot_diameter ):

		curr_y = 0
		mesh_data = []
		for braille_sequence in braille_sequences:
			curr_x = 0
			for braille_char in braille_sequence.braille_characters:
				mesh_data.extend(BrailleCharacterMesh(braille_char, dot_mesh, curr_x, curr_y, x_space, y_space, dot_diameter).braille_character_mesh_data)
				curr_x += (dot_diameter * 2) + x_space + col_space
			curr_y += (dot_diameter * 3) + (2 * y_space) + row_space

		return mesh.Mesh(np.concatenate([x.data for x in mesh_data]))

class GridLineMesh:

	def __init__( self, mesh_path, size=0.0015, length=1, offset=0, vertical=False ):
		self.mesh = mesh.Mesh.from_file(mesh_path)
		self.mesh.z *= size
		self.mesh.z -= size
		if vertical:
			self.mesh.x *= size
			self.mesh.y *= length
			self.mesh.x += offset
		else:
			self.mesh.x *= length
			self.mesh.y *= size
			self.mesh.y -= offset
