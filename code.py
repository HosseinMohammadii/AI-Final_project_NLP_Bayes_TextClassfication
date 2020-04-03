import math

f = open('HAM-Train.txt', encoding='utf-8')
lines = f.readlines()
f.close()
titles = []
texts = []
unigram = []
bigram = []
epsilon = 0.001
epsilon2 = 0.001
bias = 20
classes_dict = dict()
classes = []
classes_words_num_dict = dict()
classes_phrases_num_dict = dict()
Lambda1 = 0.5
Lambda2 = 0.5

word_each_class_num = dict()
phrase_each_class_num = dict()
for line in lines:
    ll = line.split('@@@@@@@@@@')
    titles.append(ll[0])
    texts.append(ll[1])
    classes_dict[ll[0]] = classes_dict.get(ll[0], 0) + 1
# classes_dict['classes_number'] = len(titles)
train_doc_size = len(titles)
classes = classes_dict.keys()
print(classes_dict)
print(classes)

for j in range(len(titles)):
    text = texts[j]
    title = titles[j]
    words = text.split(" ")
    counter = dict()
    counter2 = dict()

    word2 = ""
    for word in words:
        counter[word] = counter.get(word, 0.0) + 1.0
        phrase = word + word2
        counter2[phrase] = counter2.get(phrase, 0.0) + 1.0
        word2 = word

    counter['words_number'] = len(words)
    counter2['phrases_number'] = len(words)
    unigram.append(counter)
    bigram.append(counter2)

all_words_num = 0
all_phrases_num = 0
for j in range(train_doc_size):
    all_words_num += unigram[j]['words_number']
    all_phrases_num += bigram[j]['phrases_number']

print(texts[1])
# print(unigram[1])
# # print(bigram[1])
# print(len(unigram[1]))
# # print(len(bigram[1]))
# print(len(texts[1].split(" ")))
# print(unigram[1]['عراق']*112)
# # print(bigram[1]['طرفایران'])


ff = open('HAM-Test.txt', encoding='utf-8')
test_lines = ff.readlines()
test_titles = []
test_texts = []

test_unigram_answers = []
test_bigram_answers = []
test_answers = []

for line in test_lines:
    ll = line.split('@@@@@@@@@@')
    test_titles.append(ll[0])
    test_texts.append(ll[1])


def word_prob(wordd):
    word_repetition = 0.0
    for i in range(train_doc_size):
        word_repetition += unigram[i].get(wordd, epsilon2)
    return word_repetition / all_words_num


def phrase_prob(phrasee):
    phrase_repetition = 0.0
    for i in range(train_doc_size):
        phrase_repetition += bigram[i].get(phrasee, epsilon2)
    return phrase_repetition / all_phrases_num


def unigram_class_words_num(_class):
    class_words_num = 0.0
    for ii in range(train_doc_size):
        if titles[ii] == _class:
            class_words_num += unigram[ii]['words_number']
    return class_words_num


def bigram_class_phrases_num(_class):
    class_phrases_num = 0.0
    for ii in range(train_doc_size):
        if titles[ii] == _class:
            class_phrases_num += bigram[ii]['phrases_number']
    return class_phrases_num


for _class_ in classes:
    classes_words_num_dict[_class_] = unigram_class_words_num(_class_)
    classes_phrases_num_dict[_class_] = bigram_class_phrases_num(_class_)


def prob_word_class(word, classs):
    word_in_class_num = 0.0
    for ii in range(train_doc_size):
        if titles[ii] == classs:
            word_in_class_num += unigram[ii].get(word, epsilon2)
    return word_in_class_num/classes_words_num_dict[classs]


# def num_word_class(word, classs):
#     word_in_class_num = 0.0
#     for ii in range(train_doc_size):
#         if titles[ii] == classs:
#             word_in_class_num += unigram[ii].get(word, epsilon2)
#     return word_in_class_num


def prob_phrase_class(phrase, classs):
    phrase_in_class_num = 0.0
    for ii in range(train_doc_size):
        if titles[ii] == classs:
            phrase_in_class_num += bigram[ii].get(phrase, epsilon2)
    return phrase_in_class_num/classes_phrases_num_dict[classs]


# def num_phrase_class(phrase, classs):
#     phrase_in_class_num = 0.0
#     for ii in range(train_doc_size):
#         if titles[ii] == classs:
#             phrase_in_class_num += bigram[ii].get(phrase, epsilon2)
#     return phrase_in_class_num








for test_text in test_texts:
    test_text_words = test_text.split(" ")
    best_prob = 0.0
    class_answer = ""
    curr = 0
    for _classs in classes:
        unigram_class_prob = classes_words_num_dict[_classs]/all_words_num
        bigram_class_prob = classes_phrases_num_dict[_classs] / all_phrases_num
        unigram_sigma = 0.0
        bigram_sigma = 0.0
        wrd2 = ""
        for wrd in test_text_words:
            unigram_sigma += math.log10(prob_word_class(wrd, _classs))
            phrase = wrd+wrd2
            x = prob_phrase_class(phrase, _classs)
            # print(x)
            bigram_sigma += math.log10(x)
            wrd2 = wrd
        unigram_prob = math.log10(unigram_class_prob) + unigram_sigma
        bigram_prob = math.log10(bigram_class_prob) + bigram_sigma
        prob = Lambda1 * unigram_prob + Lambda2 * bigram_prob

        if curr == 0:
            best_prob = prob
            class_answer = _classs
        elif prob > best_prob:
            best_prob = prob
            class_answer = _classs

    test_answers.append(class_answer)


true_answers = 0
for i in range(len(test_titles)):
    if test_titles[i] == test_answers[i]:
        true_answers += 1

print(true_answers/len(test_titles))





