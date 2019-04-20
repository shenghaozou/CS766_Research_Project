#!/bin/bash

python inference.py --img_dir=data/generated --output_file=generated_result.txt 
python inference.py --img_dir=data/cropped --output_file=cropped_result.txt 
