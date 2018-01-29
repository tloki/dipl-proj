def get_all_dirs(path: str):

    if not path.endswith("/"):
        path += "/"

    import os
    files = os.listdir(path)

    files_full_path = [path + pathn + "/" for pathn in files]

    directories = []

    for f in files_full_path:
        if os.path.isdir(f):
            directories.append(f)

    return directories