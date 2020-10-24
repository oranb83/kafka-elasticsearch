import os

import validators

from text_handler import UrlHandler, FileHandler, StringHandler
from words import Words
from my_redis import Redis

LINES_TO_READ = 10000
MAX_UNIQUE_KEYS = 10000
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
        # Note:
        # I tried to use mulit-thread and multi-process to speed things up, but a single thread in
        # Python gave the best benchmark. Python is not a good choice for this task along with my
        # redis container choice. The operation here is mostly IO bound, but still in python it
        # doesn't necesserily mean that you will get optimal results compared to single thread (see
        # GIL for better understanding the issue). Multi-process might have helped to improved
        # performance even though we are mostly IO and not CPU bound, but only in case we have
        # several redis clusters and I only use one.
        for i, line in enumerate(lines):
            # Assumption: to avoid many IO calls to redis I chose to count the words of each
            #   line in memory. That way I only push the aggregated words count into redis once
            #   every X lines. It's more efficent if the words per lines are unique.
            #   Working on an algorithem to decide when to push the data will take more
            #   development time and testing so for now I chose every 10k lines assuming
            #   that normal text lines (like in a book) are short.
            # TODO: need to really count the size of the counter object with sys.getsizeof
            # to make sure the memory consumption is not too high.
            if i > 0 and i % LINES_TO_READ and len(counter) > MAX_UNIQUE_KEYS:
                # TODO: need to add try except and retries in case of connection issues, since locally
                # the issue forces a restart I skipped this for now.
                REDIS.save(counter)
                counter.clear()

            self.strategy.count_words(line)

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
