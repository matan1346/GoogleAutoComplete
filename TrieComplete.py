from dataclasses import dataclass


@dataclass
class TrieAutoComplete:
    def __init__(self):
        self.chars = {}
        self.end_of_word = False

    def set_end_of_word(self, flag):
        self.end_of_word = flag

    def insert_word(self, word):
        if word == '':
            self.end_of_word = True
        else:
            c = word[0]
            if c not in self.chars:
                self.chars[c] = TrieAutoComplete()
            self.chars[c].insert_word(word[1:])

    def search_prefix(self, s):
        print(s)
        if s == '' and self.end_of_word:
            print('success')
            print_trie(self)
        elif s == '':
            return
        elif s[0] in self.chars:
            self.chars[s[0]].search_prefix(s[1:])


def print_trie(tr, sentence = '', level = 0):
    if tr is None:
        return
    print('*'*level, 'level: ', level)
    if tr.end_of_word:
        print('*'*level, 'word:', sentence)
    for c, item in tr.chars.items():
        print_trie(item, sentence + c, level + 1)


s = "i like to play"

comp = TrieAutoComplete()
comp.insert_word(s)

s = "iglu"
comp.insert_word(s)

comp.insert_word('i')

comp.insert_word('avocado')
comp.insert_word('aviron')
comp.insert_word('aviatar')

comp.search_prefix('av')
#print_trie(comp)

