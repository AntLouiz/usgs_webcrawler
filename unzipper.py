import zipfile
import glob
import os


def clean_file(file_path, extract_dir='./'):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    tir_file = glob.glob("{}/*TIR.tif".format(extract_dir))
    all_files = glob.glob("{}/*.tif".format(extract_dir))

    files_to_exclude = [file for file in all_files if file not in tir_file]

    for file in files_to_exclude:
        os.remove(file)

    os.remove(file_path)
