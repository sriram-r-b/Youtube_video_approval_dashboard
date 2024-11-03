"""
A Python script for downloading all files under a folder in Google Drive.
Downloaded files will be saved at the current working directory.

This script uses the official Google Drive API (https://developers.google.com/drive).
As the examples in the official doc are not very clear to me,
so I thought sharing this script would be helpful for someone.

To use this script, you should first follow the instruction 
in Quickstart section in the official doc (https://developers.google.com/drive/api/v3/quickstart/python):
- Enable Google Drive API 
- Download `credential.json`
- Install dependencies


Notes:
- This script will only work on a local environment, 
  i.e. you can't run this on a remote machine
  because of the authentication process of Google.
- This script only downloads binary files not google docs or spreadsheets.


Author: Sangwoong Yoon (https://github.com/swyoon/)
"""
from __future__ import print_function
import io
import pickle
import os.path
from googleapiclient.http import MediaIoBaseDownload 
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload,MediaIoBaseDownload

def download():
    # Setup the Drive v3 API
    print("starting download")
    SCOPES = 'https://www.googleapis.com/auth/drive.file'
    store = file.Storage('credentials_drive.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('/etc/secrets/client_secrets.json', SCOPES)
        creds = tools.run_flow(flow, store)
    drive_service = build('drive', 'v3', http=creds.authorize(Http()))

    folder_id = '1Di_jtfDp0Q-AGtN9c2IMpjBu-nUrUUHo'
    # List all files in the folder
    page_token = None

    while True:
        print("page_token: ", page_token)
        results = drive_service.files().list(
            q = f"'{folder_id}' in parents", 
            fields='nextPageToken, files(id, name)',
            pageToken=page_token).execute()
        items = results.get('files', [])
        print("items: ", results)
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))


            file_id = item['id']
            request = drive_service.files().get_media(fileId=file_id)

            with open("drive_download_folder/"+item['name'], 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print("Download %d%%." % int(status.progress() * 100))




        page_token = results.get('nextPageToken')
        if not page_token:
            break

if __name__ == '__main__':
    download()