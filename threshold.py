import os
import shutil
from collections import OrderedDict
from random import shuffle as shuf
import re
from nltk.tokenize import word_tokenize

threshold = 4
limit = 100
USER_FOLDER = os.path.dirname(os.path.abspath(__file__))
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


def parse_text_file(input_file):
    with open(r'{}'.format(input_file)) as filedata:
        contents = filedata.read().lower()
    content_without_stopwords = remove_stopwords(contents)
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


# calling the parse function for text files
parse_text_file('/home/swapnil/github/Doctags/data/txt/test_3.txt')
