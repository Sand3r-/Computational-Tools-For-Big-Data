from mrjob.job import MRJob, MRStep

class MRWordCount(MRJob):

    def map_edges_num_to_nodes(self, key, line):
        node_one, node_two = line.split() # split the line into two vertices
        # assign "1" indicating a single connection to each vertex
        yield node_one, 1 
        yield node_two, 1

    # generic, used in both first and second step
    def combine_generator_to_list(self, node, values):
        yield node, list(values) # convert generator to list

    def reduce_to_evenness(self, node, edges_generator):
        edge_num = 0
        for edge_list in edges_generator:
            edge_num += len(edge_list) # determine number of edges per vertex
        # return True if that number is even, False otherwise
        yield (node, True) if edge_num % 2 == 0 else (node, False) 

    def map_to_and_gate(self, node, test_result):
            yield "final_answer", test_result # map to final_answer so it can
                                              # be smoothly mergeed into one 
                                              # by combiner

    def reduce_final_answer(self, key, results_list):
        has_euler_tour = True # later change to false if applicable
        for results in results_list:
            for result in results:
                if result == False: # if there is at least one non-even degree
                    has_euler_tour = False # set output value to false
                    break                  # and break out of the loop
        yield key, has_euler_tour

    def steps(self):
        return [MRStep(mapper=self.map_edges_num_to_nodes,
                       combiner=self.combine_generator_to_list,
                       reducer=self.reduce_to_evenness),
                MRStep(mapper=self.map_to_and_gate,
                       combiner=self.combine_generator_to_list,
                       reducer=self.reduce_final_answer)]

if __name__ == '__main__':
    MRWordCount.run()