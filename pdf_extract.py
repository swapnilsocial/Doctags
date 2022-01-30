import datetime
import json
import os


def doc_create(path, fname, fext, status, tokens):
    # today = datetime.date.today()
    data = {
        "filename": fname + fext,
        "format": fext,
        "location": path,
        "tokens": tokens,
        "status": status
    }
    json_string = json.dumps(data)
    path_to_store = '/home/swap/swapnilsocial/Doctags/static/jsons/'
    file = path_to_store + fname + '.json'
    print(file)
    with open(file, 'w') as outfile:
        outfile.write(json_string)
    print(json_string)
    os.system("""curl -XPOST "http://localhost:9200/doctags/_doc/""" + fname + """/" -H 'Content-Type: application/json' -d @""" + file)
    mytokenlist = []
    for k,v in tokens.items():
        for i in range(0,v):
            mytokenlist.append(k)
    print(mytokenlist)
    token_dict = {"tokens": mytokenlist}
    tdata = json.dumps(token_dict)
    tfile = path_to_store + fname + '_tokens.json'
    with open(tfile, 'w') as outfile:
        outfile.write(tdata)
    os.system("""curl -XPOST "http://localhost:9200/token/_doc/token_""" + fname + """/" -H 'Content-Type: application/json' -d @""" + tfile)

# print(datetime.date.today())


tokens = {'computer': 11, 'uccel': 2}
doc_create('/data/sampledata/crazy.txt', 'crazy', '.txt', 'passed', tokens)
