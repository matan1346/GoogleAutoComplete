from dataclasses import dataclass

replace_char = {0: 5, 1: 4, 2: 3, 3: 2}
remove_char = {0: 10, 1: 8, 2: 6, 3: 4}

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

    @classmethod
    def minimize_results(cls, results):
        data = set()
        s = ''

        sorted_results = sorted(results, key=lambda s: len(s), reverse=True)
        for result in sorted_results:
            found = False
            # for item in data:
            #    if result.startswith(item):


    def search_prefix(self, s, prefix, flag=False, level = 0, score = 0): # pithon
        # print(s, self.end_of_word)
        res = []
        score += 2
        if s == '':
            return self.collect_words(prefix, score - 2)
        elif s[0] in self.chars:

            res = self.chars[s[0]].search_prefix(s[1:], prefix + s[0], flag, level + 1, score)
            if res:

                return res
        if not flag:
            for c, item in self.chars.items():
                # replace other char
                if level > 3:
                    current_score = score - 1
                else:
                    current_score = score - replace_char[level]

                current_res = self.chars[c].search_prefix(s[1:], prefix + c, True, level + 1, current_score)
                if current_res:
                    res.extend(current_res)

                # add other char
                if level > 3:
                    current_score = score - 2
                else:
                    current_score = score - remove_char[level]

                current_res = self.chars[c].search_prefix(s, prefix + c, True, level, current_score - 2)
                if current_res:
                    res.extend(current_res)

                if level > 3:
                    current_score = score - 2
                else:
                    current_score = score - remove_char[level]

                # ignore char
                if len(s) > 2:
                    current_res = self.chars[c].search_prefix(s[2:], prefix + s[1], True, level + 1, current_score)
                    if current_res:
                        res.extend(current_res)
            return res

    def collect_words(self, prefix, score = 0):
        res = []

        if self.end_of_word:
            res.append((prefix, self.source_data, score))

        #current_res = []
        for c, item in self.chars.items():
            # print(item.chars)
            res.extend(item.collect_words(prefix + c, score))
        #if current_res:
        #    return current_res
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
