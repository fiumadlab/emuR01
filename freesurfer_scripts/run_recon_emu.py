#!/usr/bin/env python

#SBATCH --job-name=emu_fs
#SBATCH --nodes 1
#SBATCH --ntasks 1
#SBATCH -p investor
#SBATCH --qos pq_madlab
#SBATCH -e /scratch/madlab/crash/emu_fs_err
#SBATCH -o /scratch/madlab/crash/emu_fs_out

import os
from glob import glob

from nipype import Node, Function, Workflow, IdentityInterface
from nipype.interfaces.freesurfer import ReconAll
from nipype.interfaces.io import DataGrabber

# CURRENT PROJECT DATA DIRECTORY
data_dir = '/home/data/madlab/data/mri/emuR01'

# CURRENT PROJECT SUBJECT IDS
sids = ['4000', '4001']

info = dict(T1=[['subject_id']])

infosource = Node(IdentityInterface(fields=['subject_id']), name='infosource')
infosource.iterables = ('subject_id', sids)

# Create a datasource node to get the T1 file
datasource = Node(DataGrabber(infields=['subject_id'],outfields=info.keys()),name = 'datasource')
datasource.inputs.template = '%s/%s'
datasource.inputs.base_directory = os.path.abspath(data_dir)
datasource.inputs.field_template = dict(T1='%s/s1/anatomy/T1_002.nii.gz')
datasource.inputs.template_args = info
datasource.inputs.sort_filelist = True

reconall_node = Node(ReconAll(), name='reconall_node')
reconall_node.inputs.openmp = 2
reconall_node.inputs.args = '-hippocampal-subfields-T1'
reconall_node.inputs.subjects_dir = '/home/data/madlab/surfaces/emuR01'
reconall_node.plugin_args={'sbatch_args': ('-p investor --qos pq_madlab -n 2'), 'overwrite': True}

wf = Workflow(name='fsrecon')

wf.connect(infosource, 'subject_id', datasource, 'subject_id')
wf.connect(infosource, 'subject_id', reconall_node, 'subject_id')
wf.connect(datasource, 'T1', reconall_node, 'T1_files')

wf.base_dir = os.path.abspath('/scratch/madlab/emu/')
#wf.config['execution']['job_finished_timeout'] = 65

wf.run(plugin='SLURM', plugin_args={'sbatch_args': ('-p investor --qos pq_madlab -N 1 -n 1'), 'overwrite': True})
