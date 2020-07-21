"""
        Author : Fatih Kahraman
        Mail   : fatih.khrmn@hotmail.com
"""

import difflib
import statistics

from setup_Encoding import Admin

ruleset = ['i', 'l', '1', 't', 'ı', 'o', 'c', '0', 'ö', 'd',
                        'm', 'n', 'h', 'y', 'w', 'ç', 'c', 'v', 'u',
                        'ş', 'g', '9', 's', 'ğ', 'z', '2', 'u', 'ü', 'a', 'e']

ruleset_tuple = [('i', 'l', '1', 't', 'ı'), ('o', 'c', '0', 'ö', 'd'),
                        ('m', 'n', 'h'), ('y', 'w', 'h'), ('ç', 'c'), ('v', 'u', 'y'),
                        ('ş', 'g', '9', 's', 'ğ'), ('z', '2'), ('u', 'ü'), ('a', 'e')]


charset = set(ruleset)

# creating a simple data - set
input_list = []
predicted_list = []
label_list = []

admin = Admin()

input = open('SOURCE/negative.txt', 'r')
predicted = open('SOURCE/negative_predicted.txt', 'r')
label = open('SOURCE/negative_label.txt')


for line in input.readlines():
    input_word = line.replace('\n', '')
    input_list.append(input_word)

for line in predicted.readlines():
    predicted_word = line.replace('\n', '')
    predicted_list.append(predicted_word)

for line in label.readlines():
    label_value = line.replace('\n', '')
    label_list.append(label_value)

nds = open('DATA/negative_data_structure.txt', 'w+')

for i in range(len(label_list)):

    input_word_index_list = []
    predicted_word_index_list = []


    in_unique = 0
    in_no_unique = 0

    pr_unique = 0
    pr_no_unique = 0

    diff_unq_in = []
    diff_unq_pr = []

    in_word = input_list[i]
    in_word_fit = admin.mode.fit_word(in_word)
    in_word_re = in_word_fit.reshape(-1,1)
    in_word_orj = in_word_re[:len(in_word)]

    for orj in in_word_orj:
        input_word_index_list.append(float(orj))


    pr_word = predicted_list[i]
    pr_word_fit = admin.mode.fit_word(pr_word)
    pr_word_re = pr_word_fit.reshape(-1, 1)
    pr_word_orj = pr_word_re[:len(pr_word)]

    for orj in pr_word_orj:
        predicted_word_index_list.append(float(orj))


    for index in in_word:

        if not index in charset:
            in_unique += 1

        else:
            in_no_unique += 1

            tuple_ct = 0
            for tuple in ruleset_tuple:

                if index in tuple:
                    diff_unq_in.append(tuple_ct)

                tuple_ct += 1

    diff_in = set(diff_unq_in)
    len_diff_in = len(diff_in)

    tuple_ct = 0
    for index in pr_word:

        if not index in charset:
            pr_unique += 1

        else:
            pr_no_unique += 1

            tuple_ct = 0
            for tuple in ruleset_tuple:

                if index in tuple:
                    diff_unq_pr.append(tuple_ct)

                tuple_ct += 1

    diff_pr = set(diff_unq_pr)
    len_diff_pr = len(diff_pr)

    diff_pr = list(diff_pr)
    diff_in = list(diff_in)

    like_rate = difflib.SequenceMatcher(None, in_word, pr_word).ratio()
    like_rate_unique = difflib.SequenceMatcher(None, diff_in, diff_pr).ratio()



    nds.write(str(round(statistics.stdev(input_word_index_list),6)))
    nds.write(" ")
    nds.write(str(round(statistics.mean(input_word_index_list),6)))
    nds.write(" ")
    nds.write(str(in_unique))
    nds.write(" ")
    nds.write(str(in_no_unique))
    nds.write(" ")
    nds.write(str(len_diff_in/10))
    nds.write(" ")

    nds.write(str(round(statistics.stdev(predicted_word_index_list), 6)))
    nds.write(" ")
    nds.write(str(round(statistics.mean(predicted_word_index_list), 6)))
    nds.write(" ")
    nds.write(str(pr_unique))
    nds.write(" ")
    nds.write(str(pr_no_unique))
    nds.write(" ")
    nds.write(str(len_diff_pr / 10))
    nds.write(" ")

    nds.write(str(round(like_rate,6)))
    nds.write(" ")
    nds.write(str(round(like_rate_unique, 6)))

    nds.write(" ")

    nds.write(str(label_list[i]))

    nds.write("\n")

nds.close()