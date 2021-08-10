# Google Project: Auto Complete
import os
import pickle

from AutoCompleteData import AutoCompleteData
import string
import threading
from time import sleep

import time
import sys

toolbar_width = 40

# setup toolbar





main_db = {}
minimized_db = {}
db = {}

missing_score = {0: 10, 1: 8, 2: 6, 3: 4}


def splitter(n, words):
    new_list = []
    for i in range(0, len(words)-n+1):
        new_list += [" ".join(words[i:i+n])]
    return new_list


def insert_to_db(key, sentence, source, score = None):
    if key not in db:
        db[key] = []

    if score is None:
        score = len(key) * 2
    db[key] += [AutoCompleteData(sentence, source, sentence.find(key), score)]


def insert_to_db_minimize(key, line_number, sentence, source, score = None):
    if key not in minimized_db:
        minimized_db[key] = []

    if score is None:
        score = len(key) * 2
    minimized_db[key] += (source, line_number, sentence.find(key), score) # [AutoCompleteData(sentence, source, sentence.find(key), score)]

# lke to


def all_files(path):
    my_lst = []
    # print('try:', path)
    # return [r'C:\Users\omesi\PycharmProjects\GoogleAutoComplete/file.txt']
    for filename in os.listdir(path):
        if filename.endswith(".pkl") or filename.endswith(".txt"):
            my_lst.append(path+'\\'+filename)
        else:
            my_lst += all_files(path + '\\' + filename)
    return my_lst


def init(path_root='./', recreate=True):
    directory_name = path_root.split('\\')[-1]
    # return
    global db
    if not recreate and os.path.isfile('sql/' + directory_name + '.pkl'):
        db = load_db()
        return
    inserts = ''
    for file_path in all_files(path_root):
        # file_path = 'file.txt'
        print('file init: ', file_path)

        with open(file_path, 'r', encoding="utf8") as f:
            line_number = -1
            for line in f.readlines():
                line_number += 1
                sentence = line.rstrip()
                words = sentence.translate(str.maketrans('', '', string.punctuation)).lower().split()
                formatted_sentence = ' '.join(words)
                #if formatted_sentence != '':
                #    inserts += f"INSERT INTO InitData (KeySentence, RealSentence, SourceFile) VALUES ('{formatted_sentence}', '{formatted_sentence}', '{file_path}');\r\n"
                # continue
                # chunks words as keys
                #print('#########sentrence slicing: ', sentence)
                for i in range(1, len(words)):
                    #print('# slice ', i, 'chuncks:')
                    for piece in splitter(i, words):
                        # insert_to_db(piece, sentence, file_path)

                        insert_to_db_minimize(piece, line_number, sentence, file_path)

                        #for every piece, we gonna add each missing position: ex. i like to play: like to play, i ike to play...
                        # print('#-# missing position: for ', piece)
                        # continue
                        start_score = (len(piece) - 1) * 2
                        for pos in range(len(piece)):
                            current_score = start_score - 2
                            if pos <= 3:
                                current_score = start_score - missing_score[pos]

                            piece_misssing_char = piece[:pos] + piece[pos+1:]
                            # insert_to_db(piece_misssing_char, sentence,  file_path, current_score)
                            insert_to_db_minimize(piece_misssing_char, line_number, sentence,  file_path, current_score)

                            # insert dot for addition char
                            piece_addition_char = piece[:pos] + '.' + piece[pos+1:]
                            # insert_to_db(piece_addition_char, sentence, file_path, current_score)
                            # insert_to_db_minimize(piece_addition_char, line_number, sentence, file_path, current_score)
        # break
    save_db(minimized_db, directory_name)


def query(q, main_db):
    queries = [q]
    for i in range(len(q)):
        queries.append(q[:i] + '.' + q[i+1:])

    res = []
    for sentence in queries:
        if sentence in main_db:
            res.extend(main_db[sentence])
            break
    return res


def query_add_character(q):
    for i in range(len(q)):
        piece_addition_char = q[:i] + '.' + q[i+1:]
        res = query(piece_addition_char)
        if res is not None:
            return res
    return res


def save_db(data, name_file):
    a_file = open('data-missing/' + name_file + '.pkl', "wb")
    pickle.dump(data, a_file)
    a_file.close()


def load_db(file_name):
    # a_file = open("data.pkl", "rb")
    a_file = open(file_name, "rb")
    return pickle.load(a_file)

def get_results_from_files(q):

    queries = [q]
    res = []
    for i in range(len(q)):
        queries.append(q[:i] + '.' + q[i+1:])
    files = all_files('data')
    for file in files[1:]:
        current_db = load_db(file)

        for sentence in queries:
            if sentence in current_db:
                res.append(current_db[sentence])
    return res


def init_files():
    files = all_files('data')
    # print(files)
    global main_db, toolbar_width

    for file in files[1:]:
        print(file)
        #sys.stdout.write("[%s]" % (" " * toolbar_width))
        #sys.stdout.flush()
        #sys.stdout.write("\b" * (toolbar_width + 1))  # return to start of line, after '['

        current_db = load_db(file)
        # print(current_db)

        for k in current_db:
            if k not in main_db:
                main_db[k] = []
            main_db[k].extend(current_db[k])
        # time.sleep(0.1)  # do real work here
        # update the bar
        #sys.stdout.write("-")
        #sys.stdout.flush()
        break
    # sys.stdout.write("]\n")  # this ends the progress bar
    # return main_db


def main():
    global main_db
    #res =splitter2(5, ['i','like','to','play','games'])
    #print(res)
    init(r'.\2021-archive\python-3.8.4-docs-text', recreate=True)
    #init(r'D:\Users\Matan\ExcellentTeam\Python Course\GoogleAutoComplete\2021-archive\RFC', recreate=True)
    #t1 = threading.Thread(target=init_files)
    #t1.start()
    #init_files()
    #print(main_db)
    print('Done!')
    return
    while True:
        q = input("enter word: ")
        q = q.lower()

        res = query(q, main_db)
        print('regular res:', res)
        # sorted_res = sorted(res, key=lambda x: x.score, reverse=True)
        # print('sorted res: ', sorted_res)
        # sleep(1)

    #t1.join()

if __name__ == '__main__':
    main()