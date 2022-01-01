from random import shuffle as shuf

from nltk.tokenize import word_tokenize
from collections import OrderedDict
threshold = 2


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


with open(r"/home/swapnil/github/Doctags/data/txt/sample.txt") as filedata:
    contents = filedata.read().lower()
content_without_stopwords = remove_stopwords(contents)
occurrence = wordcount(content_without_stopwords)
# final_dict = OrderedDict(sorted(occurrence.items(), key=lambda x: x[1], reverse=True))
print(occurrence)
sum_values = sum(occurrence.values())

#suffle the keys
keys = list(occurrence.keys())  # List of keys
shuf(keys)
print(keys)
for key in keys:
    # key = int(key)
    v = occurrence[key]
    weight = round(((v * 3 / sum_values) * 100)) + 2
    if v > threshold:
        print("<li><a href=\"\" data-weight=\"{}\">{}</a></li>".format(weight, key))

# for k, v in occurrence.items():
#     weight = round(((v * 3/sum_values) * 100)) + 1
#     if v > threshold:
#         print("<li><a href=\"\" data-weight=\"{}\">{}</a></li>".format(weight, k))
