# File: preprocess_alphanums.py
# Author: dhung
# Description: Reads all JSONs in a directory and rotates referenced images
#				to be north oriented. Required for alphanum classifier training

import json
import os
import shutil
import argparse

import cv2

parser = argparse.ArgumentParser(
			description='Reads AZA CV JSON files and aligns targets to orient north')
parser.add_argument('-d', '--dir', required=True,
						help='Directory to scan for JSON files.')

args = parser.parse_args()

rot_lookup = {
	'n/a': 0,
	'N' : 0,
	'NE': 45,
	'E' : 90,
	'SE': 135,
	'S' : 180,
	'SW': -135,
	'W' : -90,
	'NW': -45
}
						
def main():
	json_files = [pos_json for pos_json in os.listdir(args.dir) if pos_json.endswith('.json')]
	
	for f in json_files:
		with open(os.path.join(args.dir, f)) as json_file:
			# Parse JSON and extract image data
			json_text = json.load(json_file)
			assert not os.path.isabs(json_text['image']), \
				'Absolute paths for image field in JSON not supported!'
			image_path = os.path.join(args.dir, json_text['image'])
                        assert os.path.isfile(image_path)
			image = cv2.imread(image_path)
			orient = json_text['orientation']
			rot = rot_lookup[orient]
			
			# Rotate image
			(h, w) = image.shape[:2]
			center = (w / 2, h / 2)
			M = cv2.getRotationMatrix2D(center, rot, 1.0)
			image_rot = cv2.warpAffine(image, M, (w, h))
			
			# Save processed JSON and image to subdirectory, leaving originals untouched
			directory = os.path.join(args.dir, 'preprocess_alphanums_out/')
			if not (os.path.isdir(directory)):
				os.mkdir(directory)
			shutil.copyfile(os.path.join(args.dir, f),
                                os.path.join(directory, os.path.basename(f)))
			shutil.copyfile(image_path, os.path.join(directory, os.path.basename(image_path)))

if __name__ == '__main__':
	main()
