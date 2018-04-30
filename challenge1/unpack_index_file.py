''' #############
#### CLI Parsing ####
''' #############
import sys

if len(sys.argv) < 2:
    print("Please provide the path to file")
    exit(1)

path = sys.argv[1]

if "txt.bz2" not in path:
    print("The file should have txt.bz2 format")
    exit(2)

''' ############
#### Processing ####
''' ############
import bz2

with open(path, 'rb') as file, open(path[0:-len(".bz2")], 'w', encoding="utf8", errors="ignore") as output:
    decompressor = bz2.BZ2Decompressor()
    chunk_size = 100 * 1024
    for chunk in iter(lambda: file.read(chunk_size), b''):
        data = decompressor.decompress(chunk)
        output.write(data.decode(encoding="utf8", errors='ignore'))
