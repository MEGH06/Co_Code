import numpy as np
import pandas as pd
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Flatten, Dense, LSTM, Dropout, Embedding, Activation
from tensorflow.keras.layers import add, concatenate, BatchNormalization, Input
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
import matplotlib.pyplot as plt
import cv2
import glob

# Step 1: Load descriptions
def load_description(text):
    mapping = dict()
    for line in text.split("\n"):
        token = line.split("\t")
        if len(line) < 2:
            continue
        img_id = token[0].split(".")[0]
        img_des = token[1]
        if img_id not in mapping:
            mapping[img_id] = []
        mapping[img_id].append(img_des)
    return mapping

# File paths
token_path = "/Users/kashishmandhane/Documents/Kashish Data/LAPTOP STUFF/DJ Sanghvi College/Extra-curriculars/Hackathons/Ed-tech/Flickr8K/Flickr8k_text/Flickr8k.token.txt"
train_path = "/Users/kashishmandhane/Documents/Kashish Data/LAPTOP STUFF/DJ Sanghvi College/Extra-curriculars/Hackathons/Ed-tech/Flickr8K/Flickr8k_text/Flickr_8k.trainImages.txt"
glove_path = "/Users/kashishmandhane/Documents/Kashish Data/LAPTOP STUFF/DJ Sanghvi College/Extra-curriculars/Hackathons/Ed-tech/glove-vectors-embeddings/glove.6B.200d.txt"
images_path = "/Users/kashishmandhane/Documents/Kashish Data/LAPTOP STUFF/DJ Sanghvi College/Extra-curriculars/Hackathons/Ed-tech/Flickr8K/Flicker8k_Images"

# Load and clean descriptions
text = open(token_path, "r", encoding="utf-8").read()
descriptions = load_description(text)
print(len(descriptions))

# Clean text function
def clean_text(des_list):
    for i in range(len(des_list)):
        desc = des_list[i]
        desc = desc.lower().replace(".", "").replace(",", "")
        des_list[i] = desc
for key, des_list in descriptions.items():
    clean_text(des_list)

# Step 2: Vocabulary creation
def to_vocab(desc):
    words = set()
    for key in desc.keys():
        for line in desc[key]:
            words.update(line.split())
    return words
vocab = to_vocab(descriptions)

# Step 3: Load train images
train_images = open(train_path, "r", encoding="utf-8").readlines()
train_img = [im for im in os.listdir(images_path) if im.lower().endswith(".jpg") if os.path.basename(im) in train_images]
# Step 4: Load clean descriptions for train set
def load_clean_descriptions(des, dataset):
    dataset_des = {}
    for key, des_list in des.items():
        if key + ".jpg" in dataset:
            if key not in dataset_des:
                dataset_des[key] = []
            for line in des_list:
                desc = "startseq " + line + " endseq"
                dataset_des[key].append(desc)
    return dataset_des
train_descriptions = load_clean_descriptions(descriptions, train_img)

# Step 5: Image preprocessing
def preprocess_img(img_path):
    img = load_img(img_path, target_size=(299, 299))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

# Step 6: Encode images
base_model = InceptionV3(weights="imagenet")
model = Model(base_model.input, base_model.layers[-2].output)
def encode(image):
    image = preprocess_img(image)
    vec = model.predict(image)
    vec = np.reshape(vec, (vec.shape[1]))
    return vec
train_features = {os.path.basename(img): encode(img) for img in train_img}

# Step 7: Prepare data for the model
all_train_captions = [cap for key, val in train_descriptions.items() for cap in val]
threshold = 10
word_counts = {}
for cap in all_train_captions:
    for word in cap.split(" "):
        word_counts[word] = word_counts.get(word, 0) + 1
vocab = [word for word in word_counts if word_counts[word] >= threshold]
wordtoix = {word: ix for ix, word in enumerate(vocab, start=1)}
ixtoword = {ix: word for word, ix in wordtoix.items()}
vocab_size = len(wordtoix) + 1
max_length = max(len(des.split()) for des in all_train_captions)

# Prepare sequences
X1, X2, y = [], [], []
for key, des_list in train_descriptions.items():
    pic = train_features[key + ".jpg"]
    for cap in des_list:
        seq = [wordtoix[word] for word in cap.split(" ") if word in wordtoix]
        for i in range(1, len(seq)):
            in_seq, out_seq = seq[:i], seq[i]
            in_seq = pad_sequences([in_seq], maxlen=max_length)[0]
            out_seq = to_categorical([out_seq], num_classes=vocab_size)[0]
            X1.append(pic)
            X2.append(in_seq)
            y.append(out_seq)
X1, X2, y = np.array(X1), np.array(X2), np.array(y)

# Step 8: GloVe embedding
embeddings_index = {}
glove = open(glove_path, "r", encoding="utf-8").read()
for line in glove.split("\n"):
    values = line.split()
    word = values[0]
    indices = np.asarray(values[1:], dtype="float32")
    embeddings_index[word] = indices
emb_dim = 200
emb_matrix = np.zeros((vocab_size, emb_dim))
for word, i in wordtoix.items():
    emb_vec = embeddings_index.get(word)
    if emb_vec is not None:
        emb_matrix[i] = emb_vec

# Step 9: Define the model
ip1 = Input(shape=(2048,))
fe1 = Dropout(0.2)(ip1)
fe2 = Dense(256, activation="relu")(fe1)
ip2 = Input(shape=(max_length,))
se1 = Embedding(vocab_size, emb_dim, mask_zero=True)(ip2)
se2 = Dropout(0.2)(se1)
se3 = LSTM(256)(se2)
decoder1 = add([fe2, se3])
decoder2 = Dense(256, activation="relu")(decoder1)
outputs = Dense(vocab_size, activation="softmax")(decoder2)
model = Model(inputs=[ip1, ip2], outputs=outputs)
model.layers[2].set_weights([emb_matrix])
model.layers[2].trainable = False
model.compile(loss="categorical_crossentropy", optimizer="adam")
model.fit([X1, X2], y, epochs=50, batch_size=256)

# Greedy search
def greedy_search(pic):
    start = "startseq"
    for i in range(max_length):
        seq = [wordtoix[word] for word in start.split() if word in wordtoix]
        seq = pad_sequences([seq], maxlen=max_length)
        yhat = model.predict([pic, seq], verbose=0)
        yhat = np.argmax(yhat)
        word = ixtoword[yhat]
        start += " " + word
        if word == "endseq":
            break
    final = start.split()[1:-1]
    return " ".join(final)
