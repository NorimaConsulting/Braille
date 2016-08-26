import BraillePlaque as bp
import argparse as ap
import sys

# Command line setup, particularily for optional arguments

parser = ap.ArgumentParser(
	description="Generates an stl file with braille representation of passed text. Note that all measurements are in meters.",
	epilog="Have a wonderful day!"
	)

parser.add_argument("--text",
	"-t",
	default="norima",
	dest="text",
	help="The text that will be converted to braille.")
parser.add_argument("--plaque-length",
	"-l",
	type=float,
	default=0.1,
	dest="plaque_length",
	help="Length of the plaque where the braille will rest.")
parser.add_argument("--plaque-width",
	"-w",
	type=float,
	default=0.1,
	dest="plaque_width",
	help="Width of the plaque where the braille will rest.")
parser.add_argument("--plaque-height",
	"-e",
	type=float,
	default=0.005,
	dest="plaque_height",
	help="Height of the plaque where the braille will rest.")
parser.add_argument("--col-space",
	"-c",
	type=float,
	default=0.005,
	dest="col_space",
	help="Horizontal (along width) space between each braille character column.")
parser.add_argument("--row-space",
	"-r",
	type=float,
	default=0.005,
	dest="row_space",
	help="Vertical (along length) space between each braille character row.")
parser.add_argument("--x-space",
	"-x",
	type=float,
	default=0.002,
	dest="x_space",
	help="Horizontal (along width) space between a braille character's first and second column.")
parser.add_argument("--y-space",
	"-y",
	type=float,
	default=0.002,
	dest="y_space",
	help="Vertical (along length) space between a braille character's first, second, and third row.")
parser.add_argument("--dot-diam",
	"-d",
	type=float,
	default=0.001,
	dest="dot_diameter",
	help="Diameter of a braille dot.")
parser.add_argument("--out-file",
	"-o",
	default="./results/out.stl",
	dest="out_file",
	help="Name of the output file.")

args = parser.parse_args()

braille_plaque = bp.BraillePlaque(args.text,
					args.plaque_length,
					args.plaque_width,
					args.plaque_height,
					args.col_space,
					args.row_space,
					args.x_space,
					args.y_space,
					args.dot_diameter)

braille_plaque.create_mesh()

# braille_plaque.save(args.out_file)
braille_plaque.to_std_out()
