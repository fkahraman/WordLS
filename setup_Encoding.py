"""
        Author : Fatih Kahraman
        Mail   : fatih.khrmn@hotmail.com
        Web    : www.fkahraman.com
"""

from generate_label_data import Upgrader
from class_admin import Admin
from sklearn import preprocessing

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

def main():

    ruleset = ['i', 'l', '1', 't', 'ı', 'o', 'c', '0', 'ö', 'd',
               'm', 'n', 'h', 'y', 'w', 'ç', 'c', 'v', 'u',
               'ş', 'g', '9', 's', 'ğ', 'z', '2', 'u', 'ü', 'a', 'e']

    product_list = []
    dict = {}

    admin = Admin()
    admin.mode.create_ruleset()

    ignore_list = []

    f = open('SOURCE/words.txt', 'r', encoding='utf-8')
    for word in f.readlines():

        if len(word) < 4:
            continue

        fix_word = word.replace('\n', '')
        fix_list = fix_word.split(" ")

        for wd in fix_list:

            fix_word = turkish_lower(wd)

            danger_char = 0
            for char in fix_word:
                if char in ruleset:
                    danger_char += 1

            if danger_char > 8:
                ignore_list.append(fix_word)
                continue

            if len(fix_word) < 4:
                continue

            elif len(fix_word) > 14:
                continue

            product_list.append(fix_word)

    #print('Göz ardı listesi: ',ignore_list)

    le_product = preprocessing.LabelEncoder()
    le_product.fit(product_list)

    product_list = list(le_product.classes_)

    upgrade = Upgrader()

    for word in product_list:

        upgrade.setDefaultWord(word)
        label = upgrade.generate()
        dict[word] = label

    admin.mode.create_dict(dict, admin.mode.getRuleSet())
    admin.mode.create_data()

if __name__ == '__main__':

    main()
