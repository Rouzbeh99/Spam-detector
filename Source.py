import csv

import numpy as np
import pandas as pd

df = pd.read_csv('train.csv')


def tokenize(string):
    stopwords = ['', 'همان', 'همین', 'آن', 'این', 'های', 'کردم', 'میکنم', 'رو', 'هستم', 'به', 'برای', 'ولی', 'یا', 'در',
                 'اما', 'با', 'که', 'تا',
                 'از', 'است', 'و', 'هست', 'بود', 'شده', 'بعد', 'می', 'هم', 'هر', 'حتی', 'داره', 'من', 'تو', 'او', 'ما',
                 'شما', 'ها', 'آنها']
    string.replace(".", " ").replace("!", " ").replace("?", " ").replace("؟", " ").replace(",", " ").replace("'", " ")
    words = [i for i in string.split() if i not in stopwords]
    return words


def spam_probability(words, spam_words, sum):
    probabality = 1
    for word in words:
        try:
            spam_word_count = 1 if (spam_words[word] == 0) else spam_words[word]
        except:
            spam_word_count = 1
        probabality *= spam_word_count / sum
    return probabality


def valid_probability(words, valid_words, sum):
    probabality = 1
    for word in words:
        try:
            valid_word_count = 1 if (valid_words[word] == 0) else valid_words[word]
        except:
            valid_word_count = 1
        probabality *= valid_word_count / sum
    return probabality


# word extracting
spam_words = {}
valid_words = {}
for i, item in df.iterrows():
    title_words = tokenize(str(item['title']))
    comment_words = tokenize(str(item['comment']))
    for word in title_words + comment_words:
        if item['verification_status'] == 1:
            try:
                spam_words[word] += 1
            except:
                spam_words[word] = 1
        else:
            try:
                valid_words[word] += 1
            except:
                valid_words[word] = 1

sum_of_spams = sum(list(spam_words.values()))
sum_of_valid = sum(list(valid_words.values()))

dic = {}
test_df = pd.read_csv('test.csv')

for i, item in test_df.iterrows():
    test_title_words = tokenize(str(item['title']))
    test_comment_words = tokenize(str(item['comment']))
    words = test_title_words + test_comment_words
    spam_prob = spam_probability(words, spam_words, sum_of_spams)
    valid_prob = valid_probability(words, valid_words, sum_of_valid)
    dic[item['id']] = 0 if valid_prob > spam_prob else 1

print(sum(list(dic.values())))

with open('ans.csv', 'w', newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["id", "verification_status"])
    for id, validity in dic.items():
        writer.writerow([id, validity])
