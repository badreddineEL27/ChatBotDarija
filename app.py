from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import json
import random

app = Flask(__name__)

# Load the model
model = tf.keras.models.load_model('chatbotmorocco.h5')  # Correct path

# Load the data
with open("dataset/DarijaChatbotData.json", encoding='utf-8') as DarijaChatbotData:
    intents = json.load(DarijaChatbotData)

tags = []
patterns = []
responses = {}
for intent in intents['intents']:
    responses[intent['tag']] = intent["responses"]
    for lines in intent['patterns']:
        patterns.append(lines)
        tags.append(intent['tag'])

tokenizer = Tokenizer(num_words=2000)
tokenizer.fit_on_texts(patterns)

le = LabelEncoder()
y_train = le.fit_transform(tags)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        message = request.form['user_input']
        sequence = tokenizer.texts_to_sequences([message])
        padded_sequence = pad_sequences(sequence, maxlen=8, padding='post')

        output = model.predict(np.array(padded_sequence))
        predicted_class = np.argmax(output)
        response_tag = le.inverse_transform([predicted_class])[0]

        response_options = responses.get(response_tag, [])
        response = random.choice(response_options) if response_options else "I don't understand."

        return jsonify({'message': response})

    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=False)  # Set debug to False for production
