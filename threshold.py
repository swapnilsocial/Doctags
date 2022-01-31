import os
import re
import shutil
from collections import OrderedDict
from random import shuffle as shuf
import PyPDF2
import docx
from nltk.tokenize import word_tokenize

threshold = 4
limit = 100
USER_FOLDER = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.dirname(USER_FOLDER + "data/sampledata/")
pdf_path = os.path.dirname(USER_FOLDER + "/data/pdf/")
docx_path = os.path.dirname(USER_FOLDER + "/data/docx/")
doc_path = os.path.dirname(USER_FOLDER + "/data/doc/")
txt_path = os.path.dirname(USER_FOLDER + "/data/txt/")
base_template = os.path.join(USER_FOLDER + "/templates", "tagcloud_template.html")
final_template = os.path.join(USER_FOLDER + "/templates/saved_doctags", "tagcloud.html")


# defining the replace method
def replace(file_path, text, subs, flags=0):
    with open(file_path, "r+") as file:
        file_contents = file.read()
        text_pattern = re.compile(re.escape(text), flags)
        file_contents = text_pattern.sub(subs, file_contents)
        file.seek(0)
        file.truncate()
        file.write(file_contents)


def wordcount(str):
    count = dict()
    words = str.split()
    # print(words)

    for word in words:
        if word in count:
            count[word] += 1
            # print(count[word])
        else:
            count[word] = 1

    return count


def remove_stopwords(text):
    text_tokens = word_tokenize(text)
    with open(r"stopwords.txt", "r") as word_list:
        stopwords = word_list.read().split('\n')
    tokens_without_sw = [word for word in text_tokens if word not in stopwords]
    sentence = []
    for element in tokens_without_sw:
        if len(element) > 2:
            sentence.append(element)

    filtered_sentence = (" ").join(sentence)
    print(filtered_sentence)
    return filtered_sentence


def parse_file(content):
    content_without_stopwords = remove_stopwords(content)
    occurrence = wordcount(content_without_stopwords)
    if len(occurrence) < 100:
        final_dict = OrderedDict(sorted(occurrence.items(), key=lambda x: x[1], reverse=True))
    else:
        dt = OrderedDict(sorted(occurrence.items(), key=lambda x: x[1], reverse=True))
        final_dict = {A: N for (A, N) in [x for x in dt.items()][:60]}
    # print(occurrence)
    sum_values = sum(final_dict.values())

    # shuffle the keys in the dictionary (now python dict are ordered by default)

    keys = list(final_dict.keys())  # List of keys
    shuf(keys)

    # templating the tags in html format

    tags_and_links = ''' <li><a href=\"\" data-weight=\"{}\">{}</a></li>'''
    tags_list = ''''''
    for key in keys:
        v = occurrence[key]
        weight = round(((v * 3 / sum_values) * 100)) + 2
        if v > threshold:
            tags_list = tags_list + '\n' + tags_and_links.format(weight, key)

    # replace tag_list with DOCTAG_TOKEN_TO_BE_REPLACED in tagcloud_template.html and store in static/saved_doctags
    shutil.copy(base_template, final_template)
    replace(final_template, 'DOCTAG_TOKEN_TO_BE_REPLACED', tags_list)
    return final_dict



# calling the parse function for text files
def txt_tokenize(path_to_file):
    with open(r'{}'.format(path_to_file)) as filedata:
        text = filedata.read().lower()
        # text = my_text.decode("utf-8")
    token_dict = parse_file(text)

    return path_to_file, token_dict


# calling the parse function for pdf files

def pdf_tokenize(path_to_file):
    with open(path_to_file, 'rb') as pdf_file:
        pdfReader = PyPDF2.PdfFileReader(pdf_file)
        numOfPages = pdfReader.getNumPages()
        file_data = ''''''
        for i in range(0, numOfPages):
            pageObj = pdfReader.getPage(i)
            file_data = file_data + pageObj.extractText()
        text = file_data
        token_dict = parse_file(text)
        return path_to_file, token_dict

# calling the parse function for docx files
def docx_tokenize(path_to_file):
    doc = docx.Document(path_to_file)  # Creating word reader object.
    text = ''''''
    for para in doc.paragraphs:
        text = text + " " + para.text
    # text = text.decode("utf-8")
    token_dict = parse_file(text)
    return path_to_file, token_dict
