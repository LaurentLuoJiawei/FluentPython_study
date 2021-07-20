"""
    Des：用于Section14 Sentence类的迭代方式的实现
    Date: 2021.06.21
    Author：Laurent Lo
"""
"""
Sentence + sentenceiterator
分开构建可迭代对象和迭代器
"""
import re
import reprlib
PATTERN= re.compile("\w+")
class Sentence_v1:
    def __init__(self, words, pattern):
        self.pattern = pattern
        self.words = re.findall(self.pattern, words)

    def __len__(self):
        return len(self.words)

    def __getitem__(self, item):
        return self.words[item]

    def __repr__(self):
        fmt = "Sentence {}"
        return fmt.format(reprlib.repr(self.words))


"""构建迭代器类

"""
from collections import abc
class SentenceIterator(abc.Iterator):
    def __init__(self, sentence):
        self.index = 0
        self.sen = sentence
    def __next__(self):
        try:
            return next(self.sen)
        except IndexError:
            raise StopIteration

    def __iter__(self):
        return self

class Sentence_v2:
    def __init__(self, words, pattern):
        self.pattern = pattern
        self.words = re.findall(self.pattern, words)

    def __iter__(self):
        return SentenceIterator(self)

    def __len__(self):
        return len(self.words)


    def __repr__(self):
        fmt = "Sentence {}"
        return fmt.format(reprlib.repr(self.words))

"""利用生成器函数构建sentence类
不需要单独定义一个迭代器类
"""
class Sentence_v3:
    def __init__(self, words, pattern):
        self.pattern = pattern
        self.words = re.findall(self.pattern, words)

    def __iter__(self):
        for word in self.words:
            yield word

    def __len__(self):
        return len(self.words)


    def __repr__(self):
        fmt = "Sentence {}"
        return fmt.format(reprlib.repr(self.words))

"""V4
惰性实现
"""
class Sentence_v4:
    def __init__(self, words, pattern):
        self.pattern = pattern
        self.text = words

    # def __iter__(self):
    #     for match in self.pattern.finditer(self.text):
    #         # print(match)
    #         yield match.group()
    #
    def __iter__(self):
        return (match.group() for match in self.pattern.finditer(self.text))

    def __len__(self):
        return len(self.text)


    def __repr__(self):
        fmt = "Sentence {}"
        return fmt.format(reprlib.repr(self.text))

"""等差数列生成器
"""
from itertools import count, takewhile
def ag_gen(start, stop, step):
    first = type(start+step)(start)
    gen = count(first, step)
    forever = False if stop else True
    if stop is not None:
        res = takewhile(lambda x: x<stop , gen)
    return res




if __name__ == '__main__':
    text = "w&%2&fds)a&fjkdl()s35n"
    s1 = Sentence_v4(text,PATTERN)
    for s in s1:
        print(s)

