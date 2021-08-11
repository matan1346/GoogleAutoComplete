# Google Project: Auto Complete
import os
try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle

import string

from TrieComplete import TrieAutoComplete, SourceData


comp = TrieAutoComplete()
minimized_db = {}
db = {}

missing_score = {0: 10, 1: 8, 2: 6, 3: 4}


def splitter(n, words):
    new_list = []
    for i in range(0, len(words)-n+1):
        new_list += [" ".join(words[i:i+n])]
    return new_list


def all_files(path):
    my_lst = []
    for filename in os.listdir(path):
        if filename.endswith(".pkl") or filename.endswith(".txt"):
            my_lst.append(path+'\\'+filename)
        else:
            my_lst += all_files(path + '\\' + filename)
    return my_lst


def init(path_root='./'):
    # return
    global comp

    for file_path in all_files(path_root):
        print('file init: ', file_path)

        with open(file_path, 'r', encoding="utf8") as f:
            line_number = -1
            for line in f.readlines():
                line_number += 1
                sentence = line.rstrip()
                words = sentence.translate(str.maketrans('', '', string.punctuation)).lower().split()
                for i in range(1, len(words)):
                    for piece in splitter(i, words):
                        comp.insert_word(piece, SourceData(file_path, line_number, 0, 0))


def main():

    path = input('please enter path of directory to scan text files: ')

    init(path)

    print('Done!')

    while True:
        q = input("type word or part of word: ")
        q = q.lower()

        res = comp.search_prefix(q, '')
        print('suggestion auto complete:')

        sorted_res = sorted(res, key=lambda x: x[2], reverse=True)

        for i, item in enumerate(sorted_res[:10]):
            print(f'{i+1}. {item[0]}, score: {item[2]}')
            #for source_data in item[1]:
            #    print('\t', source_data.file_name)
        #print('regular res:', res)
        # sorted_res = sorted(res, key=lambda x: x.score, reverse=True)
        # print('sorted res: ', sorted_res)
        # sleep(1)


if __name__ == '__main__':
    main()