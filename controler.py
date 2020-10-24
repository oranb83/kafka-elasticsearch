import os
import json
import logging
from multiprocessing import Pool

import validators

from text_handler import UrlHandler, FileHandler, StringHandler
from words import Words
from my_redis import Redis

LINES_TO_READ = 10000
REDIS = Redis()


class Controler:
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
        counter = self.strategy.words.frequency
        for i, line in enumerate(lines):
            self.strategy.count_words(line)
            # Assumption: to avoid many IO calls to redis I chose to count the words of each
            #   line in memory. That way I only push the aggregated words count into redis once
            #   every X lines. It's more efficent if the words per lines are unique.
            #   Working on an algorithem to decide when to push the data will take more
            #   development time and testing so for now I chose every 10k lines assuming
            #   that normal text lines (like in a book) are short.
            # TODO: need to really count the size of the counter object with sys.getsizeof
            # every X lines to make sure the memory consumption is not too big.
            if i > 0 and i % LINES_TO_READ and len(counter) > 10000:
                # TODO: need to add try except and retries in case of connection issues
                REDIS.save(counter)

        # Leftovers that were not inserted in the above if condition
        REDIS.save(counter)

    @staticmethod
    def get_stats(search):
        """
        This method return word count stats.

        @type search: str
        @param search: key=word to search.
        @rtype: int
        @return: word search appearance
        """
        return int(REDIS.get(search) or 0)
