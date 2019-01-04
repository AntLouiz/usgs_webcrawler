import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)


def upload_file(filename, file_path):
    file = drive.CreateFile({'title': filename})

    file.SetContentFile(file_path)
    file.Upload()
    os.remove(file_path)
