from mrjob.job import MRJob

class MRWordCount(MRJob):

    def mapper(self, key, line):
        for word in line.split(): # for every word in line
            yield word, 1 # output that there is once occurrence

    def combiner(self, key, values):
        yield key, sum(values) # for the same key, sum all the ones collected previously

    # use default reduce

if __name__ == '__main__':
    MRWordCount.run()