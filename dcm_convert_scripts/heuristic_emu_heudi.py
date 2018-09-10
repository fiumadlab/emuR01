def create_key(template, outtype=('dicom', 'nii.gz',), annotation_classes=None):
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

    rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_run-{item:02d}_bold')
    study_r1 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-study_run-{item:02d}_bold')
    study_r2 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-study_run-{item:02d}_bold')
    test_r1 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-test_run-{item:02d}_bold')
    test_r2 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-test_run-{item:02d}_bold')
    test_r3 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-test_run-{item:02d}_bold')
    fmstudy = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-func_dir-{dir}_fm_study-{item:02d}_epi')
    fmtest = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-func_dir-{dir}_fm_test-{item:02d}_epi')
    fmrest = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-func_dir-{dir}_fm_rest-{item:02d}_epi')
    fmdwi = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-dwi_dir-{dir}_fm_dwi-{item:02d}_epi')
    dwi = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_dwi-{item:02d}_dwi')
    t1 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T1-{item:02d}_T1w')
    pd = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_PD')
    info = {rest: [], study_r1: [], study_r2: [], test_r1: [], test_r2: [],
            test_r3: [], fmstudy: [], fmtest: [], fmrest: [],
            fmdwi: [], dwi: [], t1: [], pd: []}
    for s in seqinfo:
        x, y, sl, nt = (s[6], s[7], s[8], s[9])
        print(s[12])
        if (sl == 176) and (nt == 1) and ('T1w_MPR_vNav' in s[12]):
            info[t1].append(s[2])
        elif (nt == 238) and ('fMRI_Emotion_PA_Rest' in s[12]):
            info[rest].append(int(s[2]))
        elif (nt == 305) and ('fMRI_Emotion_PS_Study_1' in s[12]):
            info[study_r1].append(s[2])
        elif (nt == 303) and ('fMRI_Emotion_PS_Study_2' in s[12]):
            info[study_r2].append(s[2])
        elif (nt == 293) and ('fMRI_Emotion_PS_Test_1' in s[12]):
            info[test_r1].append(s[2])
        elif (nt == 293) and ('fMRI_Emotion_PS_Test_2' in s[12]):
            info[test_r2].append(s[2])
        elif (nt == 288) and ('fMRI_Emotion_PS_Test_3' in s[12]):
            info[test_r3].append(s[2])
        elif (sl > 1) and (nt == 103) and ('dMRI' in s[12]):
            info[dwi].append(s[2])
        elif s[12] in ('fMRI_DistortionMap_AP_Rest', 'fMRI_DistortionMap_PA_Rest'):
            info[fmrest].append({'item':s[2], 'dir':s[12][-7:-5]})
        elif s[12] in ('fMRI_DistortionMap_AP_PS_STUDY', 'fMRI_DistortionMap_PA_PS_STUDY'):
            info[fmstudy].append({'item':s[2], 'dir':s[12][-11:-9]})
        elif s[12] in ('fMRI_DistortionMap_AP_Test', 'fMRI_DistortionMap_PA_PS_Test'):
            info[fmtest].append({'item':s[2], 'dir':s[12][-10:-8]})
        elif s[12] in ('dMRI_DistortionMap_AP_dMRI', 'dMRI_DistortionMap_PA_dMRI'):
            info[fmdwi].append({'item':s[2], 'dir':s[12][-7:-5]})
        elif (sl == 30) and ('pd_tse_Cor_T2' in s[12]):
            info[pd].append(s[2])
        else:
            pass
    return info
