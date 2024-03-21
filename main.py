import os
from pathlib import Path
import time
import numpy
import pandas as pd
import numpy as np
import ntpath as ntp
from pydicom import dcmread
import pydicom
import glob
import pathlib

path = (r'C:\Users\danyu\OneDrive\Рабочий стол\dicom tester')
output_path = (r'C:\Users\danyu\OneDrive\Рабочий стол\dicom destination tester')
#Patient Name, Date of Birth, Modality, Study Description, StudyDate

def dicom_scan(InputPath, OutputPath=None, Compression=None):
    start = time.time()
    filesize = 0
    counter = 0
    patients_df = pd.DataFrame(
        {'PatientName': [], 'DateOfBirth': [], 'StudyDate': [], 'StudyDescription': [], 'Modality': []})
    for dcm_file in pathlib.Path(InputPath).rglob('*'):
        counter = counter + 1
        try:
            dcm = dcmread(str(dcm_file))
            filesize = filesize + os.stat(dcm_file).st_size
            patientsname = str(dcm.PatientName)
            patientsname.replace(', ', '')
            new_row = pd.DataFrame({'PatientName': [patientsname], 'DateOfBirth': [dcm.PatientBirthDate], 'StudyDate': [dcm.StudyDate], 'StudyDescription': [dcm.StudyDescription], 'Modality': [dcm.Modality]})
            frames = [patients_df, new_row]
            patients_df = pd.concat(frames, ignore_index=True)
        except:
            continue
    patients_df = patients_df.drop_duplicates()
    patients_df.reset_index(drop=True,inplace=True)
    print(patients_df)
    print("Number of records: " +str(counter))
    end = time.time()
    elapsed_time = end - start
    print("Elapsed time: " +str(elapsed_time))
    filesize_mb = filesize/(1024*1024)
    if filesize_mb>1024:
        filesize = filesize_mb/1024
        print('Files size in GB: ' + str(filesize))
    else:
        filesize = filesize_mb
        print('File size in MB: ' + str(filesize))

dicom_scan(path)
