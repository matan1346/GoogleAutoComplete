from dataclasses import dataclass

@dataclass
class SourceData:
    file_name: str
    line_number: int
    offset: int
    score: int



@dataclass
class TrieAutoComplete:
    def __init__(self):
        self.chars = {}
        self.end_of_word = False
        self.source_data = []

    def set_end_of_word(self, flag):
        self.end_of_word = flag

    def insert_word(self, word, source_data):
        if word == '':
            self.end_of_word = True
            self.source_data.append(source_data)
        else:
            c = word[0]
            if c not in self.chars:
                self.chars[c] = TrieAutoComplete()
            self.chars[c].insert_word(word[1:], source_data)

    def search_prefix(self, s, prefix, flag = False):
        # print(s, self.end_of_word)
        if s == '':
            # print('success')
            # print(prefix, 'try')
            # print(self.chars)
            return self.collect_words(prefix)
        elif s[0] in self.chars:
            return self.chars[s[0]].search_prefix(s[1:], prefix + s[0], flag)
        elif not flag:
            res = []
            for c, item in self.chars.items():
                res.extend(self.chars[c].search_prefix(s[1:], prefix + c, True))
            return res

    def collect_words(self, prefix):
        res = []

        if self.end_of_word:
            #print(prefix)
            res.append((prefix, self.source_data))
        for c, item in self.chars.items():
            # print(item.chars)
            res.extend(item.collect_words(prefix + c))
        # print(res)
        return res


def print_trie(tr, sentence = '', level = 0):
    if tr is None:
        return
    print('*'*level, 'level: ', level)
    if tr.end_of_word:
        print('*'*level, 'word:', sentence)
    for c, item in tr.chars.items():
        print_trie(item, sentence + c, level + 1)


# s = "i like to play"
# o = SourceData('a.tx', 3, 12, 1)
# comp = TrieAutoComplete()
# comp.insert_word(s, o)
#
# s = "iglu"
# comp.insert_word(s, o)
#
# comp.insert_word('i', o)
#
#
#
#
# comp.insert_word('avocado', o)
# comp.insert_word('aviron', o)
# comp.insert_word('aviatar', o)
# #print(comp.collect_words('av'))
# print(comp.search_prefix('asi', ''))
# # print_trie(comp)

