import math

f = open('HAM-Train.txt', encoding='utf-8')
lines = f.readlines()
f.close()
titles = []
texts = []
unigram = []
bigram = []

epsilon = 0.0000001
classes_dict = dict()
classes = []
classes_words_num_dict = dict()
classes_phrases_num_dict = dict()
Lambda1 = 0.2
Lambda2 = 0.8

all_words_num = 0
all_phrases_num = 0

word_each_class_num = dict()
phrase_each_class_num = dict()
for line in lines:
    ll = line.split('@@@@@@@@@@')
    titles.append(ll[0])
    texts.append(ll[1])
    classes_dict[ll[0]] = classes_dict.get(ll[0], 0) + 1

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
        phrase = word2 + word
        counter2[phrase] = counter2.get(phrase, 0.0) + 1.0
        if word_each_class_num.get(word, 0) == 0:
            word_each_class_num[word] = dict()

        word_each_class_num[word][title] = word_each_class_num[word].get(title, 0) + 1
        word_each_class_num[word]['all_classes'] = word_each_class_num[word].get('all_classes', 0) + 1

        if phrase_each_class_num.get(phrase, 0) == 0:
            phrase_each_class_num[phrase] = dict()

        phrase_each_class_num[phrase][title] = phrase_each_class_num[phrase].get(title, 0) + 1
        phrase_each_class_num[phrase]['all_classes'] = phrase_each_class_num[phrase].get('all_classes', 0) + 1

        all_words_num += 1
        all_phrases_num += 1
        word2 = word

    counter['words_number'] = len(words)
    counter2['phrases_number'] = len(words)
    unigram.append(counter)
    bigram.append(counter2)


# for j in range(train_doc_size):
#     all_words_num += unigram[j]['words_number']
#     all_phrases_num += bigram[j]['phrases_number']

# print(phrase_each_class_num['انقلاباسلامی'])
print(word_each_class_num['فوتبال'])
# print(texts[1])
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

# test_unigram_answers = []
# test_bigram_answers = []
test_answers = []

for line in test_lines:
    ll = line.split('@@@@@@@@@@')
    test_titles.append(ll[0])
    test_texts.append(ll[1])


def word_prob(wordd):
    word_repetition = 0.0
    for i in range(train_doc_size):
        word_repetition += unigram[i].get(wordd, epsilon)
    return word_repetition / all_words_num


def phrase_prob(phrasee):
    phrase_repetition = 0.0
    for i in range(train_doc_size):
        phrase_repetition += bigram[i].get(phrasee, epsilon)
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


# def prob_word_class(word, classs):
#     word_in_class_num = 0.0
#     for ii in range(train_doc_size):
#         if titles[ii] == classs:
#             word_in_class_num += unigram[ii].get(word, epsilon)
#     return word_in_class_num/classes_words_num_dict[classs]

def prob_word_class(word, classs):
    if word_each_class_num.get(word, 0) == 0:
        return epsilon
    if word_each_class_num[word].get(classs, 0) == 0:
        return epsilon
    else:
        return word_each_class_num[word][classs]/classes_words_num_dict[classs]


def prob_class_word(word, classs):
    if word_each_class_num.get(word, 0) == 0:
        return epsilon
    if word_each_class_num[word].get(classs, 0) == 0:
        return epsilon
    else:
        return word_each_class_num[word][classs] / word_each_class_num[word]['all_classes']


# def num_word_class(word, classs):
#     word_in_class_num = 0.0
#     for ii in range(train_doc_size):
#         if titles[ii] == classs:
#             word_in_class_num += unigram[ii].get(word, epsilon)
#     return word_in_class_num

"""k"""
# def prob_phrase_class(phrase, classs):
#     phrase_in_class_num = 0.0
#     for ii in range(train_doc_size):
#         if titles[ii] == classs:
#             phrase_in_class_num += bigram[ii].get(phrase, epsilon)
#     return phrase_in_class_num/classes_phrases_num_dict[classs]


def prob_phrase_class(phrase, classs):
    if phrase_each_class_num.get(phrase, -1) == -1:
        return epsilon
    if phrase_each_class_num[phrase].get(classs, -1) == -1:
        return epsilon
    else:
        return phrase_each_class_num[phrase][classs]/phrase_each_class_num[phrase]['all_classes']


def prob_class_phrase(phrase, classs):
    if phrase_each_class_num.get(phrase, 0) == 0:
        return epsilon
    if phrase_each_class_num[phrase].get(classs, 0) == 0:
        return epsilon
    else:
        return phrase_each_class_num[phrase][classs]/classes_words_num_dict[classs]

# def num_phrase_class(phrase, classs):
#     phrase_in_class_num = 0.0
#     for ii in range(train_doc_size):
#         if titles[ii] == classs:
#             phrase_in_class_num += bigram[ii].get(phrase, epsilon)
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
            # unigram_sigma += math.log10(prob_word_class(wrd, _classs))
            unigram_sigma += math.log10(prob_class_word(wrd, _classs))
            phrase = wrd2+wrd
            # bigram_sigma += math.log10(prob_phrase_class(phrase, _classs))
            bigram_sigma += math.log10(prob_class_phrase(phrase, _classs))
            wrd2 = wrd
        # unigram_prob = math.log10(unigram_class_prob) + unigram_sigma
        # bigram_prob = math.log10(bigram_class_prob) + bigram_sigma
        # unigram_prob = math.log10(classes_dict[_classs]/train_doc_size) + unigram_sigma
        # bigram_prob = math.log10(classes_dict[_classs]/train_doc_size) + bigram_sigma
        unigram_prob = unigram_sigma
        bigram_prob = bigram_sigma
        prob = Lambda1 * unigram_prob + Lambda2 * bigram_prob

        if curr == 0:
            best_prob = prob
            class_answer = _classs
        elif prob > best_prob:
            best_prob = prob
            class_answer = _classs
        curr += 1

    test_answers.append(class_answer)

TP = dict()
FP = dict()
true_answers = 0
for i in range(len(test_titles)):
    if test_titles[i] == test_answers[i]:
        true_answers += 1
        TP[test_titles[i]] = TP.get(test_titles[i], 0) + 1
    else:
        if FP.get(test_titles[i], 0) == 0:
            FP[test_titles[i]] = dict()
        FP[test_titles[i]][test_answers[i]] = FP[test_titles[i]].get(test_answers[i], 0) + 1


print("Total Accuracy is : ", true_answers/len(test_titles)*100)

recall = dict()
for class_ in classes:
    TPP = TP[class_]
    keys = FP[class_].keys()
    FPP = 0
    for key in keys:
        FPP += FP[class_][key]
    recall[class_] = TPP/(TPP+FPP)

precision = dict()
for class_ in classes:
    TPP = TP[class_]
    FPP = 0
    for cls in classes:
        if cls != class_:
            FPP += FP[cls].get(class_, 0)
    precision[class_] = TPP/(TPP+FPP)

print('                 Recall         Precision     F-measure')
for class_ in classes:
    rcal = int(recall[class_]*10000)
    prcsion = int(precision[class_]*10000)
    rcal = rcal/10000
    prcsion = prcsion/10000
    fmeasure = int(2 * rcal * prcsion / (rcal + prcsion) * 10000)
    fmeasure = fmeasure/10000
    space = " " * (15-len(class_))
    print(rcal, "       ", prcsion, "        ", fmeasure, space, class_)




