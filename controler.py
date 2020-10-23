import os
import json
import multiprocessing

import validators

from text_handler import UrlHandler, FileHandler, StringHandler, REDIS


class ControlerPost:
    """
    The Controler defines the interface of the view logic.
    """
    def __init__(self, text, strategy=None):
        """
        @type text: str
        @param text: filepath, fileurl to download or a string to parse.
        @type strategy: TextHandler or None
        @param strategy: filepath, fileurl to download or a string to parse strategy
                         if not provided (None) we will choose the right strategy.
        """
        self.text = text
        self.strategy = strategy

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        if strategy is not None:
            # Note: this option will be good for testing or in case we change the API to send a
            #       JSON payload with different keys per strategy, e.g.:
            #       filepath => for local file or url
            #       stream => for string
            self._strategy = strategy
        elif os.path.exists(os.path.join(os.getcwd(), self.text)):
            self._strategy = FileHandler(self.text)
        elif validators.url(self.text):
            self._strategy = UrlHandler(self.text)
        else:
            self._strategy = StringHandler(self.text)

    def count_words(self):
        """
        Counts sanitied words in text, file or URL (of txt file).
        """
        lines = self.strategy.read_lines()
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        # print(next(self.strategy.count_words(line)))
        pool.map(self.strategy.count_words, lines)
        pool.close()
        pool.join()


class ControlerSearch:
    """
    The Controler defines the interface of the view logic.
    """
    def __init__(self, search, strategy=None):
        """
        @type search: list<str>
        @param search: list of words to search.
        """
        self.search = search

    def get_stats(self):
        """
        This method return word count stats.

        @rtype: int
        @return: word search appearance
        """
        return int(REDIS.get(self.search) or 0)
