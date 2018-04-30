''' #############
#### CLI Parsing ####
''' #############
import sys

if len(sys.argv) < 2:
    print("Please provide the path to file")
    exit(1)

database_path = sys.argv[1]

if "xml.bz2" not in database_path:
    print("The file should have xml.bz2 format")
    exit(2)

index_path = database_path[0:-len(".xml.bz2")] + "-index.txt"

''' ############
#### Processing ####
''' ############
import bz2, re

def find_offsets(index_file, article_name):
    """Summary
    Returns starting and ending byte offset of the chunk containing
    the article in xml.bz2 archive.
    
    Args:
        index_file (file): index file in txt format
        article_name (string): name of article
    
    Returns:
        (int, int): starting, ending offset
    """
    pattern = re.compile("[0-9]:" + article_name + "$", re.UNICODE)
    offset = -1
    for entry in index_file:
        if offset == -1 and pattern.search(entry):
            print(entry[:-1]) # DEBUG
            offset = entry[:entry.find(':')]
            print(offset) # DEBUG
        elif offset != -1:
            ending_offset = entry[:entry.find(':')]
            if ending_offset != offset:
                print(ending_offset) # DEBUG
                return int(offset), int(ending_offset)

def extract_article(database, index_file, article_name):
    """Summary
    Returns an xml version of article.
    Args:
        database (file): wiki bz2 file
        index_file (file): index txt file
        article_name (string): name of article
    """
    starting_offset, ending_offset = find_offsets(index_file, article_name)
    chunk_size = ending_offset - starting_offset
    print(chunk_size) # DEBUG

    database.seek(starting_offset)
    articles_compressed = database.read(chunk_size)
    decompressor = bz2.BZ2Decompressor()
    articles_decompressed = decompressor.decompress(articles_compressed)
    print(articles_compressed[:40].decode("utf8"))






with open(index_path, 'r', encoding="utf8") as index_file, open(database_path, 'rb') as database:
    extract_article(database, index_file, "Cat")

# with open(database_path, 'rb') as file:
#     decompressor = bz2.BZ2Decompressor()
#     file.seek(33016912)
#     

# TODO!!!!!: Search for DEBUG and remove all those lines.