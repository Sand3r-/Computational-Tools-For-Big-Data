#!/usr/bin/python3

from mrjob.job import MRJob
import io
from contextlib import redirect_stdout,redirect_stderr

# define my map reduce class
class MREulerTour(MRJob):

    # yield each node in the line
    def mapper(self,_,line):
        for node in line.split():
            yield(node,1) 

    # sum the number of edges for each node
    def reducer(self, node, ones):
        yield (node,sum(ones))


main = io.BytesIO()
info = io.BytesIO()

# Run the Map Reduce job and capture the output by redirecting
# the stdout and the stderr to the variables "main" and "info" respectively

if __name__ == "__main__":
    
    with redirect_stdout(main):
        with redirect_stderr(info):
            MREulerTour.run()

output = main.getvalue().decode().rstrip()
# Display output
print(output)

# Parse the output to check if there are nodes with an odd number of edges
hasEuler = True
for line in output.split("\n"):
    line = line.split("\t")
    if int(line[1])%2 != 0:
        hasEuler = False
        break

# Display result
if hasEuler: 
    print("The input graph has an Euler tour")
else: 
    print("The input graph doesn't have an Euler tour")