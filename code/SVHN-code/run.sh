#!/usr/bin/env bash

#SBATCH --job-name=inference-svhn
#SBATCH --ntasks=1 --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --output='inference_generated.log'
#SBATCH -p slurm_default

cd $SLURM_SUBMIT_DIR 

module load cuda

./run_inference.sh
