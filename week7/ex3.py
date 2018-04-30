from mrjob.job import MRJob, MRStep
from hashlib import sha1
from itertools import chain

class MRWordCount(MRJob):

    def map_to_line_hash_and_list(self, key, line):
        numbers = [float(x) for x in line.split()]  # convert line to list of 
                                                    # floats
        line_hash = sha1(line.encode()).hexdigest() # compute hash of line
        yield line_hash, numbers                    # and use it as a key

    # generic, used in both first and second step
    def combine_generator_to_list(self, key, values):
        yield key, list(values) # convert generator to list

    def reduce_to_product(self, key, values):
        values = next(values)[0] # there is only a single list in the generator
        product = 1 
        for value in values: # compute product
            product *= value
        yield key, product

    def map_all_products_to_list(self, key, product):
            yield "final_answer", product # map each product to single key

    def reduce_final_answer(self, key, results_list):
        # It's easiest to read it from right to left (excluding slicing oper.)
        # Convert the generator to list of lists, merge inner lists into single
        # list using chain.from_iterable(1) and list constructor, sort the list
        # using sorted, select last 5 results through slicing.
        top_five = sorted(list(chain.from_iterable(list(results_list))))[-5:]
        yield key, top_five

    def steps(self): # TODO: Change names of those functions
        return [MRStep(mapper=self.map_to_line_hash_and_list,
                       combiner=self.combine_generator_to_list,
                       reducer=self.reduce_to_product
                ),
                MRStep(mapper=self.map_all_products_to_list,
                       combiner=self.combine_generator_to_list,
                       reducer=self.reduce_final_answer
                )]

if __name__ == '__main__':
    MRWordCount.run()