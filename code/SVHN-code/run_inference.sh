#!/bin/bash

for i in {0..13068}
do
    python inference.py --image data/cropped/$i.png --restore_checkpoints=Models/SVHN/tensorflow_model/model.ckpt-328000
done
