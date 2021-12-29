import os
from typing import Any, Union, Tuple

parent_dir = '/home/swapnil/github/Doctags/data'
data_path = '/home/swapnil/github/Doctags/data/sampledata'


def split_name_ext(filename):
    split_tup = os.path.splitext(filename)
    file_name = split_tup[0]
    file_extension = split_tup[1]
    return file_name, file_extension


def fetch_all_files(dir_name):
    listOfFile = os.listdir(dir_name)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dir_name, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + fetch_all_files(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def categorize(path):
    if len(os.listdir(path)) == 0:
        print('Files not found in the provided folder')
    else:
        af = fetch_all_files(path)
        for f in af:
            only_fn = os.path.split(f)
            the_path, the_filename = only_fn
            fn, fext = split_name_ext(f)
            # create folders and add files
            dirc = os.path.join(parent_dir, fext[1:].lower())
            if os.path.isdir(dirc):
                os.rename(f, dirc + '/' + the_filename)
                print('Moved file '+ f + ' to ' + dirc + '/' + the_filename)
            else:
                os.mkdir(dirc)
                os.rename(f, dirc + '/' + the_filename)
                print('Moved file ' + f + ' to ' + dirc + '/' + the_filename)



categorize(data_path)
