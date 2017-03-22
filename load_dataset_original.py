# Functionality imports
import numpy as np
import glob
import os, os.path
import pickle
from PIL import Image
from scipy import misc

# Data imports
from random import shuffle
import xml.etree.ElementTree

# Environment
mode = ["training","testing","validation"]

# Assumption: data are separated in 3 folders already, training/testing/validation. Each file is a jpg image with an associated xml file.

max_image = [-1, -1, -1]
datum_index = [-1, -1, -1]
image_list = [[],[],[]]
shuffler = [[],[],[]]
means = [[],[],[]]
data_folder = None

# We assume that we have w,h,c images to process, if that is a bad assumption we need to change shape[2] to the correct indice for the channels we are normalizing
# We also need to change the cmeans =?.mean(axis=?) line
def normalize(mymode,shape=(-1,-1,3),update=True, no_channel=False): # no channel means we have a grayscale image with no 3rd dimension
    global data_folder
    if os.path.isfile(data_folder+"./means.p") and not update:
        return pickle.load( open( data_folder+"means.p", "rb" ) )[mode.index(mymode)]
    else:

        shape_channels = 1

        if no_channel:
            means[mode.index(mymode)] = np.zeros(shape[2])
        else:
            means[mode.index(mymode)] = np.zeros(1)
        counter = 0
        for i in range(len(image_list[mode.index(mymode)])/128+1):
            counter += 1
            current_batch = return_batch(128,mymode,normalized=False)[0]
            myshape = current_batch.shape
            if no_channel:
                current_batch = current_batch.reshape([myshape[0],myshape[1],myshape[2],1])
            cmeans = current_batch.mean(axis=(0,1,2))

            for c in range(shape_channels):
                means[mode.index(mymode)][c] += cmeans[c]

        np.multiply(means[mode.index(mymode)],1/(counter*128.0))
        pickle.dump( means, open( data_folder+"/means.p", "wb" ) )
        return means

def initialize_batches(current_folder,mymode=mode[0]):
    global image_list, max_image, datum_index, shuffler
    datum_index[mode.index(mymode)] = -1
    image_list[mode.index(mymode)] = []
    for f in glob.glob(current_folder+"/*.jpg"):
        image_list[mode.index(mymode)].append(f)
    shuffler[mode.index(mymode)] = [i for i in range(max_image[mode.index(mymode)])]
    shuffle(shuffler[mode.index(mymode)])

<<READ_XML_LABELS>>

# If the output is not a one-dimensional vector, then we have to change the max_categories and the one-hot encoding
def return_batch(batch_size=32,mymode=mode[0],normalized=True,update=True, input_shape=(32,32,3), output_shape=(10)):

    global image_list, means, data_folder

    current_folder = data_folder+"/"+mymode
    if max_image[mode.index(mymode)] == -1:
        max_image[mode.index(mymode)] = len(glob.glob(current_folder+"/*.jpg"))
        initialize_batches(current_folder,mymode)

    datums = 0
    X = np.ones([batch_size]+input_shape)
    y = np.zeros([batch_size]+output_shape)

    while datums < batch_size:
        datum_index[mode.index(mymode)] += 1
        if datum_index[mode.index(mymode)] == max_image[mode.index(mymode)]:
            datum_index[mode.index(mymode)] = 0
        shuffled_index = shuffler[mode.index(mymode)][datum_index[mode.index(mymode)]]

        # to open xml and jpeg, if success put it in datum and update to +1
        if (os.path.exists(image_list[mode.index(mymode)][shuffled_index])):

            "proper image"
            image_path = image_list[mode.index(mymode)][shuffled_index]
            xml_path = os.path.splitext(image_list[mode.index(mymode)][shuffled_index])[0]+str('.xml')

            category, skip = read_annotations(xml_path)
            if skip:
                continue

            X[datums,] = np.asarray(misc.imresize(Image.open(image_list[mode.index(mymode)][shuffled_index]),input_shape))
            <<SET_LABELS>>

            datums += 1

    if means[mode.index(mymode)] == [] and normalized:
        normalize(mymode,shape=input_shape,update=update)

    if normalized:
        X = np.multiply(X - means[mode.index(mymode)],1/255.0)
    return X,y

def one_hot(category,max_labels): # category 0 - 4 for 5 labels
        y = np.zeros(max_labels)
        y[category] = 1
        return y

data_folder = <<DATA_FOLDER>>

<<OTHER>>