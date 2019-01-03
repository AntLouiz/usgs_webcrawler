import zipfile
import glob
import os
from datetime import datetime


def clean_file(file_path, extract_dir='./'):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    tir_file = glob.glob("{}/*TIR.tif".format(extract_dir))
    all_files = glob.glob("{}/*.tif".format(extract_dir))

    files_to_exclude = [file for file in all_files if file not in tir_file]

    for file in files_to_exclude:
        os.remove(file)


if __name__ == '__main__':
    clean_file(
        './download/LC08_L1TP_219062_20181220_20181227_01_T1.zip',
        './download/{}'.format(datetime.now())
    )
