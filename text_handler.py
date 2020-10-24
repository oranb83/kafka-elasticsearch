import time
from abc import ABC, abstractmethod
from urllib.request import urlopen

from words import Words


class TextHandler(ABC):
    """
    Strategy text handler. It get text from URL, File or String.
    """
    def __init__(self, text):
        """
        @type text: str
        @param text: filepath, fileurl to download or a string to parse
        """
        self.text = text
        self.words = Words()

    def count_words(self, line):
        """
        @type line: str
        @param line: line of text
        """
        self.words.count_words(line)

    @abstractmethod
    def read_lines(self):
        """
        This method will return an iterator of new lines without digits.
        Any other chars are valid and will be considered as part of the word.
        """
        raise NotImplementedError('This method must be implemeted')


class StringHandler(TextHandler):
    def read_lines(self):
        # Assumption: the amount of chars that can be passes here is limited and can be fully read
        #             into the memory, otherwise please send a FILE or a URL.
        return iter(self.text.splitlines())


class FileHandler(TextHandler):
    # Assumption: the data per line will fit into memory, otherwise I need to read the data in
    #             chunks until the last space of that chunk (so I will not split a word) and it
    #             will add to the development time. Lines can be quite big so I will read them into
    #             a generator line by line - it's quite fast since python optimizes this process.
    def read_lines(self):
        with open(self.text) as fd:
            for line in fd:
                yield line


class UrlHandler(FileHandler):
    # Assumption: the data per line will fit into memory, otherwise I need to read the data in
    #             chunks until the last space of that chunk (so I will not split a word) and it
    #             will add to the development time. Lines can be quite big so I will read them into
    #             a generator line by line - it's quite fast since python optimizes this process.
    def read_lines(self):
        with urlopen(self.text) as fd:
           for line in fd:
                yield line
