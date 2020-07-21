"""
        Author : Fatih Kahraman
        Mail   : fatih.khrmn@hotmail.com
"""


import json, time
import numpy as np
import joblib, pickle

from keras.engine.saving import model_from_json
import difflib, statistics

from sklearn import preprocessing

class encoded_chars:

    def __init__(self):
        self.all_chars = ["a", "b", "c", "ç", "d", "e", "f", "g", "ğ", "h", "ı", "i", "j", "k",
                 "l", "m", "n", "o", "ö", "p", "r", "s", "ş", "t", "u", "ü", "v", "y", "z", "w", "x",
                 "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        self.char_data = {}
        self.data_flow = {}
        self.label_dict = {}

        self.min_word_ct = 3
        self.max_word_ct = 15

        self.negative_class = []

        self.model = None
        self.model_negative = None

    def getRuleSet(self):
        return self.char_data

    def getDataDict(self):
        return self.data_flow

    def getLabelDict(self):
        return self.label_dict

    def getNegativeClass(self):
        return self.negative_class

    def getAllChars(self):
        return self.all_chars

    def encode_char(self, chars):

        le = preprocessing.LabelEncoder()
        le.fit(chars)
        encoded_char = le.transform(chars)
        scaled = preprocessing.scale(encoded_char)
        return le.classes_, scaled

    def create_ruleset(self):

        char_label, scaled = self.encode_char(self.getAllChars())
        for i in range(len(char_label)):
            self.char_data[char_label[i]] = str(scaled[i])

        with open('SOURCE/ruleset.json', 'w') as outfile:
            json.dump(self.char_data, outfile, ensure_ascii=False)

    def encode_label(self, dict):

        label_dict = {}
        label_list = []
        for item in dict:
            label_list.append(item)

        le = preprocessing.LabelEncoder()
        le.fit(label_list)
        encoded_label = le.transform(label_list)

        for index in range(len(le.classes_)):
            label_dict[le.classes_[index]] = str(encoded_label[index])

        #return le.classes_, encoded_label

        self.label_dict = label_dict

        return label_dict

    def create_dict(self, dict, ruleset):

        data_list = []
        data_all = []
        label_dict = self.encode_label(dict)

        for label in label_dict.keys():

            for word in dict[label]:

                for char in word:

                    data_list.append(str(ruleset[char]))

                data_all.append(data_list)
                data_list = []

            self.data_flow[str(label_dict[label])] = data_all
            data_all = []



        with open('SOURCE/data.json', 'w') as outfile:
            json.dump(self.data_flow, outfile, ensure_ascii=False)

        with open('SOURCE/label.json', 'w') as outfile2:
            json.dump(self.getLabelDict(), outfile2, ensure_ascii=False)

    def append_dict(self,label,new_data, path_label='SOURCE/label.json', path_data='SOURCE/data.json'):

        data_list = []
        data_all = []

        with open(path_label) as f:
            data = json.load(f)

        encode = []
        for value in data.values():
            encode.append(int(value))

        new_encode_value = max(encode)
        new_encode_value += 1

        data[label] = str(new_encode_value)

        with open(path_label, 'w') as outfile:
           json.dump(data, outfile, ensure_ascii=False)

        with open('SOURCE/ruleset.json') as r:
            ruleset = json.load(r)


        for word in new_data:

            for char in word:

                data_list.append(str(ruleset[char]))

            data_all.append(data_list)
            data_list = []

        with open(path_data) as d:
            all_data = json.load(d)

        all_data[str(new_encode_value)] = data_all

        with open(path_data, 'w') as outfile:
            json.dump(all_data, outfile, ensure_ascii=False)

    def create_data(self, path_json='SOURCE/data.json'):

        with open (path_json) as json_file:
            data = json.load(json_file)

        f = open("DATA/data.csv", "w+")

        for label in data:

            for index in data[label]:

                ct = 0

                for value in index:

                    f.write("%f " % float(value))
                    ct += 1

                while ct < self.max_word_ct:

                    f.write("%f " % float("-2.000001"))
                    ct += 1

                f.write("%d" % int(label))
                f.write("\n")

    def fit_word(self, word):

        fit_word = []
        #ruleset = self.getRuleSet()

        with open ('SOURCE/ruleset.json') as json_file:
            ruleset = json.load(json_file)

        ct = 0

        for index in word:

            fit_word.append(float(ruleset[index]))
            ct += 1

        while ct < self.max_word_ct:

            fit_word.append(float("-2.000001"))
            ct += 1

        fit = np.array(fit_word).reshape(1, -1)

        return fit

    def predict(self, word, output_model_file='MODEL/model_RF.sav', model_type=None):

        if model_type == 'keras':

            if self.model == None:
                start = time.time()
                model_file = open('MODEL/model_ann.json', 'r')
                self.model = model_file.read()
                model_file.close()
                self.model = model_from_json(self.model)
                self.model.load_weights('MODEL/ann_weights.h5')
                stop = time.time()
                print("Model load time: ", round(stop-start, 3))


        else:
            with open(output_model_file, 'rb') as f:

                if self.model == None:
                    start = time.time()
                    self.model = joblib.load(f)
                    stop = time.time()
                    print("Model load time: ", round(stop - start, 3))


        word = turkish_lower(word)

        X = np.array(self.fit_word(word)).reshape(1, -1)

        if model_type == 'keras':
            X = np.expand_dims(X, axis=2)
            output = self.model.predict(X)

        else:
            output = self.model.predict(X)

        if model_type=='keras':

            output_list = list(output[0])

            max_value = max(output_list)

            counter = 0
            for index in output_list:

                if index == max_value:
                    output = counter
                    break

                counter += 1

        #output2 = model.predict_proba(X)
        #print(output2)

        with open('SOURCE/label.json') as json_file:
            labels = json.load(json_file)

        for key in labels:
            if int(labels[key]) == int(output):
                return key

    def predict_available(self, input_word, predicted_word, model_file='MODEL/model_negative.pkl'):

        ruleset = ['i', 'l', '1', 't', 'ı', 'o', 'c', '0', 'ö', 'd',
                   'm', 'n', 'h', 'y', 'w', 'ç', 'c', 'v', 'u',
                   'ş', 'g', '9', 's', 'ğ', 'z', '2', 'u', 'ü', 'a', 'e']

        ruleset_tuple = [('i', 'l', '1', 't', 'ı'), ('o', 'c', '0', 'ö', 'd'),
                         ('m', 'n', 'h'), ('y', 'w', 'h'), ('ç', 'c'), ('v', 'u', 'y'),
                         ('ş', 'g', '9', 's', 'ğ'), ('z', '2'), ('u', 'ü'), ('a', 'e')]

        charset = set(ruleset)

        lower_input = turkish_lower(input_word)
        lower_predicted = turkish_lower(predicted_word)

        fit_list = []

        fit_in_word = []
        fit_pr_word = []

        diff_unq_in = []
        diff_unq_pr = []

        in_unique = 0
        in_no_unique = 0

        pr_unique = 0
        pr_no_unique = 0

        with open('SOURCE/ruleset.json') as json_file:
            ruleset = json.load(json_file)



        for index in lower_input:
            fit_in_word.append(round(float(ruleset[index]), 6))


        for index in lower_predicted:
            fit_pr_word.append(float(ruleset[index]))



        for index in lower_input:

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

        for index in lower_predicted:

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

        like_rate = difflib.SequenceMatcher(None, lower_input, lower_predicted).ratio()
        like_rate_unique = difflib.SequenceMatcher(None, diff_in, diff_pr).ratio()

        fit_list.append(round(statistics.stdev(fit_in_word), 6))
        fit_list.append(round(statistics.mean(fit_in_word),6))
        fit_list.append(in_unique)
        fit_list.append(in_no_unique)
        fit_list.append(len_diff_in/10)
        fit_list.append(round(statistics.stdev(fit_pr_word), 6))
        fit_list.append(round(statistics.mean(fit_pr_word), 6))
        fit_list.append(pr_unique)
        fit_list.append(pr_no_unique)
        fit_list.append(len_diff_pr/10)
        fit_list.append(round(like_rate, 6))
        fit_list.append(round(like_rate_unique, 6))

        fit = np.array(fit_list).reshape(1, -1)

        with open(model_file, 'rb') as m:
            # model = pickle.load(f)

            if self.model_negative == None:
                start = time.time()
                self.model_negative = pickle.load(m)
                stop = time.time()
                print("Negative model load time: ", round(stop - start, 3))

        output = self.model_negative.predict(fit)
        return output

class Admin:

    mode = encoded_chars()

def turkish_lower(text):

    keys = [('Ğ','ğ'),('G', 'g'),
            ('I', 'ı'),('İ', 'i'),
            ('U', "u"), ("Ü", 'ü'),
            ('O', 'o'), ('Ö', 'ö'),
            ('Ç', 'ç'),('C', 'c'),
            ('Ş','ş'),('S', 's'),]

    text_copy = list(text)

    ct = 0
    for i in text:

        for key in keys:

            if i in key[0]:

                text_copy[ct] = key[1]

            else:
                text_copy[ct] = text_copy[ct].lower()

        ct += 1

    return_str = ""
    for index in text_copy:
        return_str += index

    return return_str