#!/bin/bash

rm -f data/generated.tfrecords
cp data/test/digitStruct.mat data/generated
python convert_to_tfrecords.py
python eval.py
