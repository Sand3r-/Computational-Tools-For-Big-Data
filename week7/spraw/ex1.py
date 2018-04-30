#!/usr/bin/python3

import sys
from mrjob.job import MRJob
from mrjob.step import MRStep
import re

class MRWordOccurences(MRJob):

    def mapper(self, _, line):
        line = re.sub(r'[?|$|.|!|,|;]',r'',line)
        for word in line.split():
            yield word.lower(), 1

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    MRWordOccurences.run()