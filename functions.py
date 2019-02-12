import os

path = '/Users/MateuszGrzybek/Desktop/Magisterka/Main/'
mimetypes = {'.docx': 'application/msword',
             '.xlsx': 'application/msexcel',
             '.pdf': 'application/pdf',
             '.dwg': 'image/vnd.dwg',
             '.txt': 'text/plain',
             'other': 'application/octet-stream',
            }

def get_files(path):
    """Gets all the files and their extensions from the given path."""
    directory = os.listdir(path)

    for file in directory:
        if file.startswith('.'):
            directory.remove(file)
        elif file.startswith('~'):
            directory.remove(file)

    extensions = [list(os.path.splitext(file)) for file in directory]
    return extensions

filenames = get_files(path)

def match_mimetypes(filenames, mimetypes):
    """Matches mimetypes to the files in the directory, based on their
    extensions.
    """
    for k,v in mimetypes.items():
        for filename in filenames:
            if filename[1] == k:
                filename.append(v)

    print(filenames)



get_files(path)
match_mimetypes(filenames, mimetypes)
