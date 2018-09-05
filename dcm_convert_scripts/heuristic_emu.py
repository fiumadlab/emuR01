import os

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return (template, outtype, annotation_classes)

def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where
    
    allowed template fields - follow python string module: 
    
    item: index within category 
    subject: participant id 
    seqitem: run number during scanning
    subindex: sub index within group
    """
    
    rs = create_key('rsfmri/rest_run{item:03d}/rest', outtype=('dicom', 'nii.gz'))
    study_r1 = create_key('BOLD/study_run{item:03d}/bold', outtype=('dicom', 'nii.gz'))
    study_r2 = create_key('BOLD/study_run{item:03d}/bold', outtype=('dicom', 'nii.gz'))
    test_r1 = create_key('BOLD/test_run{item:03d}/bold', outtype=('dicom', 'nii.gz'))
    test_r2 = create_key('BOLD/test_run{item:03d}/bold', outtype=('dicom', 'nii.gz'))
    test_r3 = create_key('BOLD/test_run{item:03d}/bold', outtype=('dicom', 'nii.gz'))
    fmstudy = create_key('fieldmap/fm_study_{item:03d}', outtype=('dicom', 'nii.gz'))
    fmtest = create_key('fieldmap/fm_test_{item:03d}', outtype=('dicom', 'nii.gz'))
    fmrest = create_key('fieldmap/fm_rest_{item:03d}', outtype=('dicom', 'nii.gz'))
    fmdwi = create_key('fieldmap/fm_dwi_{item:03d}', outtype=('dicom', 'nii.gz'))
    dwi = create_key('dmri/dwi_{item:03d}', outtype=('dicom', 'nii.gz'))
    t1 = create_key('anatomy/T1_{item:03d}', outtype=('dicom', 'nii.gz'))
    pd = create_key('anatomy/PD_{item:03d}', outtype=('dicom', 'nii.gz'))
    info = {rs: [], study_r1: [], study_r2: [], test_r1: [], test_r3: [], 
            test_r3: [], fmstudy: [], fmtest: [], fmrest: [],
            fmdwi: [], dwi: [], t1: [], pd: []}
    last_run = len(seqinfo)
    for s in seqinfo:
        x,y,sl,nt = (s[6], s[7], s[8], s[9])
        print(s[12])
        if (sl == 176) and (nt == 1) and ('T1w_MPR_vNav' in s[12]):
            info[t1].append(s[2])
        elif (nt == 238) and ('fMRI_Emotion_PA_Rest' in s[12]):
                info[rs].append(int(s[2]))
        elif ('fMRI_Emotion_PS_Study_1' in s[12]):
                info[study_r1].append(s[2])
        elif ('fMRI_Emotion_PS_Study_2' in s[12]):
                info[study_r2].append(s[2])
        elif (nt == 293) or (nt == 100) and ('fMRI_Emotion_PS_Test_1' in s[12]):
                info[test_r1].append(s[2])
        elif (nt == 293) and ('fMRI_Emotion_PS_Test_2' in s[12]):
                info[test_r2].append(s[2])
        elif (nt == 288) and ('fMRI_Emotion_PS_Test_3' in s[12]):
                info[test_r3].append(s[2])
        elif (sl > 1) and (nt == 103) and ('dMRI' in s[12]):
            info[dwi].append(s[2])
        elif ('fMRI_DistortionMap_AP_Rest' in s[12]) or ('fMRI_DistortionMap_PA_Rest' in s[12]):
            info[fmrest].append(s[2])
        elif ('fMRI_DistortionMap_AP_PS_STUDY' in s[12]) or ('fMRI_DistortionMap_PA_PS_STUDY' in s[12]):
            info[fmstudy].append(s[2])
        elif ('fMRI_DistortionMap_AP_PS_STUDY' in s[12]) or ('fMRI_DistortionMap_PA_PS_STUDY' in s[12]):
            info[fmtest].append(s[2])
        elif ('dMRI_DistortionMap_AP' in s[12]) or ('dMRI_DistortionMap_PA' in s[12]):
            info[fmdwi].append(s[2])
        elif (sl == 30) and ('pd_tse_Cor_T2' in s[12]):
            info[pd].append(s[2])
        else:
            pass
    return info
