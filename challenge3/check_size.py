import imageio
import os
import numpy as np

def remove_thumbs_db(input_dir, file_list):
    thumbs_db = "Thumbs.db"
    thumbs_path = input_dir + "/" + thumbs_db
    if thumbs_db in file_list:
        os.remove(thumbs_path)
        print("Thumbs.db removed successfully")

def parse_files(input_dir):
    file_list = os.listdir(input_dir)
    remove_thumbs_db(input_dir, file_list)
    input_path = os.path.join(input_dir, file_list[0])
    reader = imageio.get_reader(input_path)
    meta = reader.get_meta_data()
    min_size = [99999999, 9999999999]
    for filename in file_list:
        input_path = os.path.join(input_dir, filename)
        reader = imageio.get_reader(input_path)
        meta = reader.get_meta_data()
        size = meta['size']
        if size[0] < size[1]:
            size = (size[1], size[0])
        # print(size)

        if size[0] < min_size[0]:
            min_size[0] = size[0]
        if size[1] < min_size[1]:
            min_size[1] = size[1]
    print(min_size)

# min_size = ()
parse_files("videos")