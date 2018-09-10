#!/usr/bin/env python
import os
import subprocess as sp
SUBJECTS = [4001, 4002, 4005, 4012, 4013]
SESSIONS = ['S1', 'S2']
for subject in SUBJECTS:
    for sess in SESSIONS:
        if not \
        os.path.exists('/home/data/madlab/dicoms/emu_r01/{1}/{0}/{0}.tar.gz'.format(sess, subject)):
            continue
        heudi_cmd = \
        "heudiconv -b -d '/home/data/madlab/dicoms/emu_r01/{subject}/{session}/*.tar.gz' \
        -ss {0} -s {1} \
        -f /home/data/madlab/scripts/emuR01/dcm_convert_scripts/heuristic_emu_heudi.py \
        -o /scratch/madlab/dicoms/emuR01/".format(sess, subject)
        sp.Popen('sbatch -J heudiconv_{0}_{1} \
                 -p investor -N 1 --mail-type=END,FAIL \
                 -e ~/{0}_{1}_err \
                 --mail-user=akimbler@fiu.edu \
                 --qos pq_madlab --wrap="{2}"'.format(subject, sess, heudi_cmd),
                 shell=True)
