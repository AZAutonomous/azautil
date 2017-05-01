# File: preprocess_alphanums.py
# Author: dhung
# Description: Reads all JSONs in a directory and rotates referenced images
#				to be north oriented. Required for alphanum classifier training

import json
import os
import argparse

import cv2
import numpy as np

parser = argparse.ArgumentParser(
			description='Reads AZA CV JSON files and aligns targets to orient north')
parser.add_argument('-d', '--dir', required=True,
						help='Directory to scan for JSON files.')

args = parser.parse_args()

def main():
	json_files = [pos_json for pos_json in os.listdir(args.dir) if pos_json.endswith('.json')]
	arr = []
	counter = 0
	for f in json_files:
		with open(os.path.join(args.dir, f)) as json_file:
			# Parse JSON and extract image data
			json_text = json.load(json_file)
			if os.path.isabs(json_text['image']):
				image_path = json_text['image']
			else:
				image_path = os.path.join(args.dir, json_text['image'])
			assert os.path.isfile(image_path)
			image = cv2.imread(image_path)
			if (len(arr) > 0):
				image = cv2.resize(image, dsize=arr[-1].shape[:2]) # Janky fix
			arr.append(image)
			counter += 1

	mean = np.mean(arr, axis=(0,1,2))
	stddev = np.std(arr, axis=(0,1,2))
	print('Processed %d files' % counter)
	print 'Calculated mean = ', mean
	print 'Calculated std dev = ', stddev


if __name__ == '__main__':
	main()
