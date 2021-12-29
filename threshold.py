from nltk.tokenize import word_tokenize
from collections import OrderedDict
threshold = 3


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
final_dict = OrderedDict(sorted(occurrence.items(), key=lambda x: x[1], reverse=True))
print(final_dict)

for k, v in final_dict.items():
    if v > threshold:
        print(k, v)
