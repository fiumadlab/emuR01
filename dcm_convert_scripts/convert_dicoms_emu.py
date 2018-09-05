#!/usr/bin/env python

#SBATCH --job-name=emu_dcm_convert_submit
#SBATCH -p investor
#SBATCH --qos pq_madlab
#SBATCH --nodes 1
#SBATCH --ntasks 1

import os
import subprocess as sp
subjs = ['4000', '4001', '4005', '4012']
session = ['s1', 's2']

workdir = '/scratch/madlab/emu/dcm_convert'
outdir = '/home/data/madlab/data/mri/emuR01'
dicom_dir = '/home/data/madlab/dicoms/emu_r01/%s/%s/*/*/*/*'
heuristic_file = '/home/data/madlab/scripts/emuR01/dcm_convert_scripts/heuristic_emu.py'

for i, sid in enumerate(subjs):
    for _session in session:
        convertcmd = ' '.join(['python', 'dicomconvert2_Siemens.py',
                               '-d', dicom_dir,
                               '-z', _session,
                               '-s', sid,
                               '-o', outdir, 
                               '-c', 'dcm2nii',
                               '-f', heuristic_file])
        script_file = 'emu_dcm2nii-%s-%s.sh' % (sid, _session)
    	if os.path.exists(script_file):
            continue
        with open(script_file, 'wt') as fp:
            fp.writelines(['#!/bin/bash\n'])
            fp.writelines(['#SBATCH --job-name=emu_dcm2nii_%s-%s\n' % (sid, _session)])
            fp.writelines(['#SBATCH --nodes 1\n'])
            fp.writelines(['#SBATCH --ntasks 1\n'])
            fp.writelines(['#SBATCH -p investor\n'])
            fp.writelines(['#SBATCH --qos pq_madlab\n'])
            fp.writelines(['#SBATCH -t 24:00:00\n'])
            fp.writelines(['#SBATCH -e /scratch/madlab/crash/emu_dcm2nii_submit_err_%s-%s\n' % (sid, _session)])
            fp.writelines(['#SBATCH -o /scratch/madlab/crash/emu_dcm2nii_submit_out_%s-%s\n' % (sid, _session)])
            fp.writelines([convertcmd])
        outcmd = 'sbatch %s' % script_file
        sp.call(outcmd, shell='True')
        continue
