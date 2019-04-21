import os


def get_extensions(path):
    """Gets all the files and their extensions from the given path."""
    directory = os.listdir(path)

    for file in directory:
        if file.startswith('.'):
            directory.remove(file)
        elif file.startswith('~'):
            directory.remove(file)

    extensions = [list(os.path.splitext(file)) for file in directory]

    return extensions


def match_mimetypes(path, mimetypes):
    """Matches mimetypes to the files in the directory, based on their
    extensions.
    """
    filenames = get_extensions(path)

    for k,v in mimetypes.items():
        for filename in filenames:
            if filename[1] == k:
                filename.append(v)
                full_name = filename[0] + filename[1]
                filename.append(full_name)

    return filenames
