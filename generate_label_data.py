"""
        Author : Fatih Kahraman
        Mail   : fatih.khrmn@hotmail.com
        Web    : www.fkahraman.com
"""

from sklearn import preprocessing
import random
import difflib

class Upgrader:

    def __init__(self):

        self.default_word = ""
        self.default_word_size = 0
        self.default_word_list = []

        self.all_chars = ["a", "b", "c", "ç", "d", "e", "f", "g", "ğ", "h", "ı", "i", "j", "k",
                          "l", "m", "n", "o", "ö", "p", "r", "s", "ş", "t", "u", "ü", "v", "y", "z", "w", "x",
                          "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        self.ruleset = [('i', 'l', '1', 't', 'ı'), ('o', 'c', '0', 'ö', 'd'),
                        ('m', 'n', 'h'), ('y', 'w', 'h'), ('ç', 'c'), ('v', 'u', 'y'),
                        ('ş', 'g', '9', 's', 'ğ'), ('z', '2'), ('u', 'ü'), ('a', 'e')]

        #self.ruleset = [('i', 'l', '1', 'ı'), ('o','ö'), ('ç', 'c'), ('v', 'u'), ('g', 'ğ'),
        #                ('ş', 's'), ('z', '2'), ('u', 'ü'), ('a', 'e', 'o')]

    def getDefaultWord(self):
        return self.default_word

    def setDefaultWord(self, word):
        self.default_word_size = len(word)
        self.default_word = word

    def combine(self, words, tupple, index):

        fit_word_list = []

        for word in words:
            for i in tupple:

                if len(word) == len(self.default_word):
                    kernel_word = word[:index] + i + word[index + 1:]

                else:
                    kernel_word = word[:index + 1] + i + word[index + 1 + 1:]
                fit_word_list.append(kernel_word)

        return fit_word_list

    def decrease(self, list):

        if len(list[0]) < 5:
            return list


        upgrade_list = []

        for word in list:

            #if len(word) < 5:
             #   continue

            under = word[1:]
            over = word[:-1]
            upgrade_list.append(under)
            upgrade_list.append(over)

        return list+upgrade_list

    def increased(self, list):

        adding_list = []

        extra_char = ['x',  '4', ]

        #word = self.getDefaultWord()
        for word in list:
            for char in extra_char:
                adding_word = char + word
                adding_list.append(adding_word)

        return adding_list

    def croping(self, list, CROP_COMBINIG=3):

        if self.default_word_size >= 8:
            CROP_COMBINIG = 2

        croping_list = []

        le_fit = preprocessing.LabelEncoder()
        le_fit.fit(list)

        for word in le_fit.classes_:

            if (difflib.SequenceMatcher(None, self.default_word, word).ratio() >= ((self.default_word_size-CROP_COMBINIG)/self.default_word_size)):
                croping_list.append(word)

        return croping_list

    def generate(self):

        fit_list = []
        fit_list.append(self.default_word)

        ct = 0
        word_index = 0


        for i in self.default_word:

            for tp in self.ruleset:

                for index in tp:

                    if index == i:

                        upgrade_list = self.combine(fit_list, self.ruleset[ct], word_index)

                        for wd in upgrade_list:
                            fit_list.append(wd)

                    #else:
                    #    break

                ct += 1

                if ct == len(self.ruleset):
                    ct = 0

            word_index += 1


        fit_list = self.croping(fit_list)

        increased_list = self.increased(fit_list)

        fit_list = self.decrease(fit_list)

        fit_list += increased_list

        le = preprocessing.LabelEncoder()
        le.fit(fit_list)

        k = 2000 / len(le.classes_)

        self.default_word_list = le.classes_

        if k > 1:
            print("----- ", self.default_word, ' - ', len(list(le.classes_)*int(k+1)))
            return list(le.classes_)*int(k+1)

        #else:
        #    return le.classes_

        #if self.default_word == "gold":
        #    print(le.classes_)
        print("----- ", self.default_word, ' - ', len(le.classes_))
        return le.classes_

if __name__ == '__main__':


    message = """
                32 Bit Bilgisayar Hiz.
    """

    print(message)