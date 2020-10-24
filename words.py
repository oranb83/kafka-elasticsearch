import time
from collections import Counter
from string import digits, punctuation

REMOVE_CHARS = str.maketrans('', '', digits + punctuation.replace('-', '').replace(',', '').replace("'", ''))


class Words:
    """
    This class handles counting valid chars that consist words and sanities other words to make
    them valid.

    Examples:
        valid words:
        foo
        foo-
        foo,
        f-o,o
        it's

        invalid words => to valid words:
        me2           => me
        m2,m.j        => m,mj
        m2-3@2j2      => m-j
        MXC#40-2m,    => mxc-m
    """
    def __init__(self):
        self._frequency = Counter()

    @property
    def frequency(self):
        return self._frequency

    def count_words(self, line):
        """
        @type line: str
        @param line: line of text
        """
        line = self._sanities(line)
        self._count(line)

    def _sanities(self, line):
        """
        @type line: str
        @param line: line of text
        @rtype: str
        @return: sanitied string as seen in this class example.
        """
        # Efficent way to remove chars
        return line.lower().translate(REMOVE_CHARS)

    def _count(self, line):
        """
        @type line: str
        @param line: line of text
        """
        self.frequency.update(line.split())


