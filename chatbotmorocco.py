# -*- coding: utf-8 -*-
"""ChatbotMorocco.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CDaOfaL74q-YXzAsF_OuFeVJnJl7-CDB

## Importing Libraries
"""

import tensorflow as tf
import numpy as np
import pandas as pd
import json
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional, Dropout, Flatten

# Set a random seed for reproducibility
tf.random.set_seed(42)
np.random.seed(42)

# File path to your JSON data
file_path = "dataset/DarijaChatbotData.json"

# Load data from the existing file
with open(file_path, encoding='utf-8') as DarijaChatbotData:
    intents = json.load(DarijaChatbotData)

# Extract patterns, tags, and responses
tags = []
patterns = []
responses = {}
for intent in intents['intents']:
    responses[intent['tag']] = intent["responses"]
    for lines in intent['patterns']:
        patterns.append(lines)
        tags.append(intent['tag'])

# Data Preprocessing
data = pd.DataFrame({"inputs": patterns, "tags": tags})

tokenizer = Tokenizer(num_words=2000)
tokenizer.fit_on_texts(data["inputs"])
train = tokenizer.texts_to_sequences(data["inputs"])
x_train = pad_sequences(train)

le = LabelEncoder()
y_train = le.fit_transform(data["tags"])

input_shape = x_train.shape[1]
unique_words = len(tokenizer.word_index)
output_length = le.classes_.shape[0]

# Constructing a Neural Network
model = Sequential()
model.add(Embedding(unique_words + 1, 50, input_length=input_shape))
model.add(Bidirectional(LSTM(10, return_sequences=True)))
model.add(Bidirectional(LSTM(10)))
model.add(Dropout(0.5))
model.add(Dense(units=10, activation='relu'))
model.add(Dense(units=output_length, activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Training the Model
MoroccanBot = model.fit(x_train, y_train, epochs=400, verbose=1)
print("Accuracy: ", MoroccanBot.history['accuracy'][-1])

# Save the model
model.save('chatbotmorocco.h5')

#"""## Chatting with bot"""

#print("MoroccanBot: Salam ! Ana chatbot maghribi । kifach bghiti n3awnek ?")
#while True:
#    textList = []
#    USER  = input("badr: ")
#    prediction_input = []
#
#
#    prediction_input = ''.join(USER )
#    textList.append(prediction_input)
#
#    prediction_input = tokenizer.texts_to_sequences(textList)
#    prediction_input = np.array(prediction_input).reshape(-1)
#    prediction_input = pad_sequences([prediction_input], input_shape)
#
#    output = model.predict(prediction_input)
#    output = output.argmax()
#
#    response_tag = le.inverse_transform([output])[0]
#    print("MoroccanBot: ", random.choice(responses[response_tag]))
#    if response_tag == 'GoodBye':
#        break