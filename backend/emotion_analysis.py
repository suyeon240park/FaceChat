import os
import numpy as np
import tensorflow as tf
from models import prado
from projection_layers import ProjectionLayer  # Assuming this is part of your project
import base_layers  # Assuming this contains the mode definitions (TRAIN, EVAL, PREDICT)

# Configuration dictionaries (example, replace with actual values)
MODEL_CONFIG = {
    'max_seq_len': 100,
    'feature_size': 256,
    'multilabel': True
}
CONFIG = {
    'learning_rate': 0.001,
    'learning_rate_decay_rate': 0.96,
    'learning_rate_decay_steps': 1000,
    'train_steps': 10000,
    'save_checkpoints_steps': 1000
}
LABELS = ['label1', 'label2', 'label3']  # Example labels, replace with actual labels

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def build_model(mode):
    inputs = []
    if mode in (base_layers.TRAIN, base_layers.EVAL):
        projection = tf.keras.Input(
            shape=(MODEL_CONFIG['max_seq_len'], MODEL_CONFIG['feature_size']),
            name='projection',
            dtype='float32'
        )
        sequence_length = tf.keras.Input(
            shape=(), name='sequence_length', dtype='float32'
        )
        inputs = [projection, sequence_length]
    else:
        input = tf.keras.Input(shape=(), name='input', dtype='string')
        projection_layer = ProjectionLayer(MODEL_CONFIG, mode)
        projection, sequence_length = projection_layer(input)
        inputs = [input]

    model_layer = prado.Encoder(MODEL_CONFIG, mode)
    logits = model_layer(projection, sequence_length)

    if MODEL_CONFIG['multilabel']:
        activation = tf.keras.layers.Activation('sigmoid', name='predictions')
    else:
        activation = tf.keras.layers.Activation('softmax', name='predictions')
    predictions = activation(logits)

    model = tf.keras.Model(inputs=inputs, outputs=[predictions])
    return model

# Define your tokenizer function
def simple_tokenizer(text):
    # Placeholder tokenizer, replace with your actual tokenizer
    return np.array([ord(char) for char in text])

# Preprocess and reshape input data for prediction
def preprocess_input(text):
    input_data = simple_tokenizer(text)
    return np.reshape(input_data, (1, -1))  # Adjust shape as needed

# Instantiate the model in PREDICT mode
model = build_model(base_layers.PREDICT)

# Load the weights
checkpoint_path = 'model/model_checkpoint'
model.load_weights(checkpoint_path)

# Text inputs for prediction
PREDICT_TEXT = [
    'Good for you!',
    'I hate you!',
    'I love you.'
]

# Make predictions
for text in PREDICT_TEXT:
    input_data = preprocess_input(text)
    results = model.predict(x=[input_data])
    print(f'\n{text}:')
    labels = np.flip(np.argsort(results[0]))
    for x in range(3):
        label = LABELS[labels[x]]
        print(f'{label}: {results[0][labels[x]]}')
