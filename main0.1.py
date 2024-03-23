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
import shutil
from datetime import datetime

path = (r'C:\Users\danyu\OneDrive\Рабочий стол\dicom tester')
output_path = (r'C:\Users\danyu\OneDrive\Рабочий стол\dicom destination tester')


# Patient Name, Date of Birth, Modality, Study Description, StudyDate

def dicom_scan(InputPath, OutputPath=None, Compression=None):
    start = time.time()
    filesize = 0
    counter = 0
    directories_df = pd.DataFrame({'PatientName': [], 'StudyDate': [], 'Path': []})
    patients_df = pd.DataFrame(
        {'PatientName': [], 'DateOfBirth': [], 'StudyDate': [], 'StudyDescription': [], 'Modality': []})
    for dcm_file in pathlib.Path(InputPath).rglob('*'):
        counter = counter + 1
        try:
            dcm = dcmread(str(dcm_file))
            filesize = filesize + os.stat(dcm_file).st_size
            patientsname = str(dcm.PatientName)
            patientsname.replace(', ', '')
            directorypath = str(Path(dcm_file).parent.absolute())
            new_row_directories = pd.DataFrame(
                {'PatientName': [patientsname], 'StudyDate': [dcm.StudyDate], 'Path': [directorypath]})
            new_row = pd.DataFrame(
                {'PatientName': [patientsname], 'DateOfBirth': [dcm.PatientBirthDate], 'StudyDate': [dcm.StudyDate],
                 'StudyDescription': [dcm.StudyDescription], 'Modality': [dcm.Modality]})
            frames = [patients_df, new_row]
            directory_frames = [directories_df, new_row_directories]
            directories_df = pd.concat(directory_frames, ignore_index=True)
            patients_df = pd.concat(frames, ignore_index=True)
        except:
            continue
    patients_df = patients_df.drop_duplicates()
    patients_df.reset_index(drop=True, inplace=True)
    directories_df = directories_df.drop_duplicates()
    directories_df.reset_index(inplace=True)
    print(directories_df)
    dirlist = []
    if OutputPath == None:
        pass
    else:
        counter_output = 0
        for dcm_file in pathlib.Path(InputPath).rglob('*'):
            try:
                dcm = dcmread(str(dcm_file))
                counter_output = counter_output + 1
                dcmpath = str(os.path.dirname(os.path.abspath(dcm_file)))
                dirlist.append(dcmpath)
            except:
                continue

    directories = []
    for i in dirlist:
        if i not in directories:
            directories.append(i)

    for i in range(len(directories_df)):
        old_name = str(directories_df.loc[i, 'Path'])
        dirPatientName = directories_df.loc[i, 'PatientName']
        dirStudyDate = directories_df.loc[i, 'StudyDate']
        dir_Study_Date = datetime.strptime(dirStudyDate, '%Y%m%d').strftime('%Y/%m/%d')
        new_name = str(output_path + "\\" + dirPatientName + " " + dir_Study_Date)
        shutil.move(old_name, new_name)


    return patients_df
    print("Number of records: " + str(counter))
    end = time.time()
    elapsed_time = end - start
    print("Elapsed time: " + str(elapsed_time))

    filesize_mb = filesize / (1024 * 1024)
    if filesize_mb > 1024:
        filesize = filesize_mb / 1024
        print('Files size in GB: ' + str(filesize))
    else:
        filesize = filesize_mb
        print('File size in MB: ' + str(filesize))


dicom_scan(path, output_path)
