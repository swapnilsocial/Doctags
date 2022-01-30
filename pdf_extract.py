import datetime
import json
import os


def doc_create(path, fname, fext, status, tokens):
    today = datetime.date.today()
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
    # with open(file, 'w') as outfile:
    #     json.dump(json_string, outfile)
    with open(file, 'w') as outfile:
        outfile.write(json_string)
    print(json_string)
    os.system("""curl -XPOST "http://localhost:9200/doctags/_doc" -H 'Content-Type: application/json' -d @""" + file)


# print(datetime.date.today())


tokens = {'computer': 17, 'uccel': 14}
doc_create('/data/sampledata/crazy.txt', 'crazy', '.txt', 'passed', tokens)
