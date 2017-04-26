# sample_dataset.py
# author: dhung
# description: randomly sample a directory, separating contents into a
#              70-30 split of training data and validation data

import os
import shutil
import json
import argparse
import random

parser = argparse.ArgumentParser(description='Reads AZA CV JSON files and aligns targets to orient north')
parser.add_argument('-d', '--dir', required=True,
                    help='Directory to scan for JSON files.')
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-p', '--keep_prob', default=0.7, type=float,
                    help='Probability of keeping data in training '
                         'set. Should be in range [0, 1]. '
                         'Can also be thought of as train-validate split')
args = parser.parse_args()

def main():
	assert args.keep_prob >= 0 and args.keep_prob <= 1

	# TODO: initialize random seed
	json_files = [pos_json for pos_json in os.listdir(args.dir) if pos_json.endswith('.json')]
	
	num_files = len(json_files)
	num_train = int(num_files * args.keep_prob)
	num_validate = num_files - num_train

	if args.verbose:
		print('Found %d files in %s' % (num_files, args.dir))
		print('Will split into %d training and %d validation files' %
				(num_train, num_validate))

	count_train = 0
	count_validate = 0

	train_dir = os.path.join(args.dir, 'train_data/')
	validation_dir = os.path.join(args.dir, 'validation_data/')

	# TODO: Recursively delete existing directories? use shutil.rmtree()
	if not os.path.exists(train_dir):
		os.mkdir(train_dir)
	if not os.path.exists(validation_dir):
		os.mkdir(validation_dir)

	for f in json_files:
		image_path = ""
		with open(os.path.join(args.dir, f)) as json_file:
			# Parse JSON and extract image data
			json_text = json.load(json_file)
			assert not os.path.isabs(json_text['image']), \
				'Absolute paths for image field in JSON not supported!'
			image_path = json_text['image']
		if ((random.random() < args.keep_prob and count_train < num_train)
			or count_validate >= num_validate):
			# Move JSON and JPG to train_data/
			os.rename(os.path.join(args.dir, f),
						os.path.join(train_dir, f))
			# There may be multiple JSONs pointing to the same JPG
			# so a JPG may have already been moved
			if not os.path.isfile(os.path.join(train_dir, image_path)):
				shutil.copyfile(os.path.join(args.dir, image_path),
								os.path.join(train_dir, image_path))
			count_train += 1
			
		else:
			# TODO: Move JSON and JPG to validation_data/
			os.rename(os.path.join(args.dir, f),
						os.path.join(validation_dir, f))
			# There may be multiple JSONs pointing to the same JPG
			# so a JPG may have already been moved
			if not os.path.isfile(os.path.join(validation_dir, image_path)):
				shutil.copyfile(os.path.join(args.dir, image_path),
								os.path.join(validation_dir, image_path))
			count_validate += 1
	
	# Delete the leftover JPG files
	jpg_files = [pos_jpg for pos_jpg in os.listdir(args.dir) if pos_jpg.endswith('.jpg')]
	for f in jpg_files:
		os.remove(os.path.join(args.dir, f))

if __name__ == '__main__':
    main()
