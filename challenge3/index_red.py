# truth = [set(['DMDR1U2RA7VN', 'K29U1709EA5R', 'D3NAY0YYFO4P', '58D4CGTDM5VX', 'ZLRB9DMOYSM9', 'J27VW94YYJRP', '77FOA4UNWD8Y', 'W0JQH817T6IE', 'OTXGMC3STDZ7', 'F4R4MW6W1BO8']), set(['NY0XRPCQX2J6', '5B15T46T75XM', 'QKPLUGBHWX1S', '90BP7NQLOZI8', 'H3ETKWH70OZ0', 'BWWQDUXMWDTU', '0J5OWQRLV2ZF', 'D0K9L1DTG1EQ', 'SRXWGC3XXJJO', '148X2AS0P7MP']), set(['YS0M2FXHFUKK', 'KASAZL3RPKK6', 'ZILSSCBC40IR', 'NEFEWA5CEPMW', '8DGQWN7D24RW', 'G1FQA6E96794', 'XNP69S9V9849', 'X5YBR7LX367U', '7INXG6910I57', 'W6G19WDE9FBN']), set(['0TIBYZMOJD10', '3QBNSX4XCPSA', 'X3NC9RI7ZPUK', 'FRVXUX3X2S3R', 'V9GUVOSSR83H', '9ED47BUW3J9B', '1RY6YNAXRI7X', 'VWQTW530L7HU', 'MBA1GBU5A3MJ', 'FQR5NJPRAQ1T']), set(['27BMODQ3KSDY', '2WRJA9D9SEPC', 'Q6RVWKG553K7', '8S46FET9O2Y1', 'AG7PEPJHIALE', 'WJ9Y2OG0EKR7', 'PLXC6ZHQIVVA', 'YRTYMIDTOV1R', '2DM3J4TN9557', 'LBVFSL8OUUHG']), set(['L1EYAG4PN55N', 'WXA3PLRSG53G', '74SBBUUA94N3', 'AQ6XWF6SZZ3K', 'B45DHKLKJDYD', '5OM79AIPHX6W', 'ELVYERD2OSIT', '21USARENDKEH', 'VBEY9RLYA5IF', 'MZMYC75VUQCA'])]

import os, imagehash
from sklearn.metrics import adjusted_rand_score
from PIL import Image
from sklearn.cluster import KMeans
import numpy as np
from itertools import chain

def rand_index(clusters):
    elems = list(set.union(*truth))

    # Index of Containing Set
    memory_truth = {}
    memory_clusters = {}
    def ics(element, set_list, set_list_name):
        if set_list_name == "truth":
            if element in memory_truth:
                return memory_truth[element]
        if set_list_name == "clusters":
            if element in memory_clusters:
                return memory_clusters[element]

        for c, s in enumerate(set_list):
            if element in s:
                if set_list_name == "truth":
                    memory_truth[element] = c
                if set_list_name == "clusters":
                    memory_clusters[element] = c
                return c

    x = list(map(lambda e: ics(e, clusters, 'clusters'), elems))
    y = list(map(lambda e: ics(e, truth, 'truth'), elems))

    # print(x)
    # print(y)
    # print(len(y))

    return adjusted_rand_score(x,y)

image_hash_pairs = []
hashes = []
# image_name = {}

input_dir = "images_red"
for filename in os.listdir(input_dir):
    input_path = os.path.join(input_dir, filename)
    if input_path.endswith(".png"):
        hash = imagehash.phash(Image.open(input_path))
        image_hash_pairs.append((int(str(hash), 16), os.path.splitext(filename)[0]))
        # image_name[int(str(hash), 16)] = os.path.splitext(filename)[0] # unused currently
        hashes.append(int(str(hash), 16))

# for i, p in image_hash_pairs:
#     print(i, p)

hashes = np.array(hashes)
hashes = hashes.reshape(-1, 1)

# print(image_name)

clusters = [set() for x in range(6)]
kmeans = KMeans(n_clusters=6).fit(hashes)
for i in range(len(hashes)):
    clusters[kmeans.labels_[i]].add(image_hash_pairs[i][1])
    # print(hashes[i], kmeans.labels_[i])

# print(clusters)
# print(truth)

print(rand_index(clusters))