import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


gauth = GoogleAuth()

gauth.LoadCredentialsFile('credentials.txt')

if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

gauth.SaveCredentialsFile('credentials.txt')

drive = GoogleDrive(gauth)


def upload_file(filename, file_path):
    file = drive.CreateFile({'title': filename})

    file.SetContentFile(file_path)
    file.Upload()
    os.remove(file_path)
