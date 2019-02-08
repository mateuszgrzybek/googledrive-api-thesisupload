from __future__ import print_function
import pickle
import os.path
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=1000, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

def upload_file(filename, filepath, mimetype):
    """Upload the specified file"""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    page_token = None
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(pageSize=1000,
                                   fields="nextPageToken, files(id, name)",
                                   q='trashed=false',
                                   pageToken=page_token).execute()
    items = results.get('files', [])
    item_names = [item['name'] for item in items]

    # create a folder for the current date
    folder_name = datetime.datetime.today().strftime('%d.%m.%Y')
    # targeted parent folder's id
    main_parent_id = '1aA5ByhHf-8IIWrm82us4wqgoW78TxVlr'
    folder_mimetype = 'application/vnd.google-apps.folder'


    if folder_name not in item_names:
        # execute if the desired folder name was not found in non-trashed files
        file_metadata = {'name': folder_name,
                         'parents': [main_parent_id],
                         'mimeType': folder_mimetype}
        folder = service.files().create(body=file_metadata,
                                            fields='id').execute()
        print('File ID: %s' % folder.get('id'))

        # upload the desired files to the newly created directory (folder_name)
        parent_id = '%s' % folder.get('id')
        file_metadata = {'name': filename,
                         'parents': [parent_id]}
        media = MediaFileUpload(filepath,
                                mimetype=mimetype)
        file = service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        print('File ID: %s' % file.get('id'))
    else:
        print('Folder', folder_name, 'already exists.')

# if __name__ == '__main__':
#     main()
upload_file('fizzbuzz.py', os.path.expanduser('~/Desktop/fizzbuzz.py'),
            'application/x-python-code')
