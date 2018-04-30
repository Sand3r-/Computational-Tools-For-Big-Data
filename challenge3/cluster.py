import imageio
import sys, os
import numpy as np

from skimage import feature

def convert_mp4(input_path, output_path):
    if os.path.isfile(output_path) or input_path == "videos_red\Thumbs.db": # If the file exists, skip it
        return
    print("Opening ", input_path)
    reader = imageio.get_reader(input_path)
    meta = reader.get_meta_data()
    size = meta['size']

    writer = imageio.get_writer(output_path)

    video_length = reader.get_length()
    resulting_image = np.zeros((size[1], size[0]))

    frames = 24
    step = int(video_length / frames)
    for i in range(0, frames, step):
        img = reader.get_data(i)
        resulting_image += feature.canny(img[:, :, 1]) / frames
    # for im in reader:
    #     # resulting_image += feature.canny(im[:, :, 1]) / video_length
    #     resulting_image += im[:, :, 1] / video_length

    resulting_image *= 255.0/resulting_image.max()

    writer.append_data(resulting_image)
    writer.close()

def parse_files(input_dir, output_dir):
    i = 0
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.png')
        last_img_path = output_path
        convert_mp4(input_path, output_path)
        i += 1
        print("Processed " + str(i) + "th image.")

parse_files("videos_red", "images_red")
