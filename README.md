### Google Drive uploader for master's thesis

This is a simple script for automating the uploading process of all core files
related to my master's thesis to Google Drive.  

## Workflow

The script works after running `python3 main.py`. It looks for files in the  
specified directory, checks their extensions and matches them with corresponding  
mimetypes. After that, the Drive API is being contacted (the app is authorized  
for my google account) and a directory with current date is being created.  
All the files found in the local directory are then uploaded.  
If there already is a folder with current date, files won't be uploaded.  
If such a folder exists in trashed files, it will be ignored.
