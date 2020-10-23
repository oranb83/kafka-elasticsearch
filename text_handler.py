from abc import ABC, abstractmethod
from urllib.request import urlopen

import redis

from words import Words

REDIS = redis.Redis(host='redis', port=6379)


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

    @classmethod
    def count_words(cls, line):
        """
        @type line: str
        @param line: line of text
        //@rtype: Counter
        //@return: a Counter dict with a mapping of all the words in this line and there count
        """
        words = Words()
        words.count_words(line)
        # Note: to avoid many IO calls to redis I chose to count the words of each line in memory.
        #       That way I only push the aggregated words count into redis.
        #       It's more efficent with bigger lines.
        #       Working on an algorithem to decide when to push the data will take more
        #       development time and testing.
        #       Another option to consider will be to use redis pipelines and
        #       incr each key by 1 once seen while pushing in bulk - need to invest time in
        #       generating testing data and stress testing to see which approch is faster for
        #       long/short lines.
        with REDIS.pipeline() as pipe:
            for key, value in words.frequency.items():
                pipe.incrby(key, value)
            pipe.execute()

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
