import os
import threshold as th
import json
import nltk
import datetime

nltk.download('punkt')

USER_FOLDER = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.dirname(USER_FOLDER + '/uploads/')
parent_dir = os.path.dirname(USER_FOLDER + "/data/")
# data_path = os.path.dirname(USER_FOLDER + "/data/sampledata/")
data_path = UPLOAD_FOLDER
path_to_store = os.path.dirname(USER_FOLDER + "/static/jsons/")


# this function will split the filename and extension

def split_name_ext(filename):
    split_tup = os.path.splitext(filename)
    file_name = split_tup[0]
    file_extension = split_tup[1]
    return file_name, file_extension


# this function loops through all directories and fetches all files in provided path
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


# this function creates a json document of the file with tokens and properties and loads to elasticsearch
def doc_create(path, fname, fext, status, tokens):
    ct = str(datetime.datetime.now())
    mytokenlist = []
    for k, v in tokens.items():
        for i in range(0, v):
            mytokenlist.append(k)

    data = {
        "filename": fname + fext,
        "format": fext,
        "location": path,
        "tokens": mytokenlist,
        "time": ct,
        "status": status
    }
    json_string = json.dumps(data)
    print(json_string)
    file = path_to_store + '/' + fname + '.json'
    with open(file, 'w') as outfile:
        outfile.write(json_string)
    print(json_string)
    os.system(
        """curl -XPOST "http://elasticsearch:9200/doctags/_doc/""" + fname + """/" -H 'Content-Type: application/json' -d @""" + file)
    print(mytokenlist)
    token_dict = {"tokens": mytokenlist}
    tdata = json.dumps(token_dict)
    tfile = path_to_store + '/' + fname + '_tokens.json'
    with open(tfile, 'w') as outfile:
        outfile.write(tdata)
    os.system(
        """curl -XPOST "http://elasticsearch:9200/token/_doc/token_""" + fname + """/" -H 'Content-Type: application/json' -d @""" + tfile)


# this function calls threshold module and helps to create the categories and tokens for each file based on file
# extension

def categorize(path):
    if len(os.listdir(path)) == 0:
        print('Files not found in the provided folder')
    else:
        af = fetch_all_files(path)
        for f in af:
            only_fn = os.path.split(f)
            the_path, the_filename = only_fn
            fn, fext = split_name_ext(the_filename)
            print(fn, fext, the_path, the_filename)
            if fext == '.txt':
                p, t = th.txt_tokenize(f)
                print(p, t)
                status = "parsed"
            elif fext == '.pdf':
                p, t = th.pdf_tokenize(f)
                print(p, t)
                status = "parsed"
            elif fext == '.docx':
                p, t = th.docx_tokenize(f)
                print(p, t)
                status = "parsed"
            elif fext == '.json':
                print("pass")
            else:
                print('bad file : {}'.format(f))
                t = 'NA'
                status = "not parsed"
            # create folders and add files
            dirc = os.path.join(parent_dir, fext[1:].lower())
            if os.path.isdir(dirc):
                os.rename(f, dirc + '/' + the_filename)
                print('Moved file ' + f + ' to ' + dirc + '/' + the_filename)
            else:
                os.mkdir(dirc)
                os.rename(f, dirc + '/' + the_filename)
                print('Moved file ' + f + ' to ' + dirc + '/' + the_filename)
            doc_create(dirc + '/' + the_filename, fn, fext, status, t)

    return "the program has run successfully"


# to be called from the main file
# if __name__ == '__main__':
#     categorize(data_path)
