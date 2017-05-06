#!/usr/bin/env bash

DIR=${1%/}

echo 'Calculating meanstd of dataset, saving result to' $DIR/metadata.txt
python calc_meanstd.py -d $DIR | tee $DIR/metadata.txt
ALPHANUM_DIR=$DIR/preprocess_alphanums_out
echo 'Creating preprocessed alphanumerics copy of dataset in' $ALPHANUM_DIR 
python preprocess_alphanums.py -d $DIR

# Main dataset
echo 'Sampling dataset in' $DIR
python sample_dataset.py -d $DIR -p .99 | tee -a $DIR/metadata.txt
echo 'Converting data in' $DIR 'to TFRecords in' $DIR/TFRecords
python json_to_tfrecord.py --train_directory $DIR/train_data --validation_directory $DIR/validation_data --output_directory $DIR/TFRecords --train_shards 128 --validation_shards 32

# Alphanums dataset
echo 'Sampling dataset in' $ALPHANUM_DIR
python sample_dataset.py -d $ALPHANUM_DIR -p .99
echo 'Converting data in' $ALPHANUM_DIR 'to TFRecords in' $ALPHANUM_DIR/TFRecords
python json_to_tfrecord.py --train_directory $ALPHANUM_DIR/train_data --validation_directory $ALPHANUM_DIR/validation_data --output_directory $ALPHANUM_DIR/TFRecords --train_shards 128 --validation_shards 32
