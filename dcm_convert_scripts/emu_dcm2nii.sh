#!/bin/bash
#SBATCH --job-name=emu_dcm2nii_4000
#SBATCH --nodes 1
#SBATCH --ntasks 1
#SBATCH -p investor
#SBATCH --qos pq_madlab
#SBATCH -t 24:00:00
#SBATCH -e /scratch/madlab/crash/emu_dcm2nii_submit_err_4000
#SBATCH -o /scratch/madlab/crash/emu_dcm2nii_submit_out_4000
python dicomconvert2_Siemens.py -d /home/data/madlab/dicoms/emu_r01/%s/%s/*/*/*/* -z s2 -s 4000 -o /home/data/madlab/data/mri/emuR01 -c dcm2nii -f /home/data/madlab/scripts/emuR01/dcm_convert_scripts/heuristic_emu.py
