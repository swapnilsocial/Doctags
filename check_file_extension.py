import os

data_path = '/data/sampledata'


def split_name_ext(filename):
    split_tup = os.path.splitext(filename)
    print(split_tup)
    file_name = split_tup[0]
    file_extension = split_tup[1]
    return file_name, file_extension


def fetch_all_files(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + fetch_all_files(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def categorize(data_path):
    af = fetch_all_files(data_path)
    for f in af:
        fn, fext = split_name_ext(f)
        print(fn, fext[1:])
    # create folders and add files
    if

categorize(data_path)