import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

data = keras.datasets.mnist
(train_data, train_labels), (test_data, test_labels) = data.load_data()

'''
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(196, activation="relu"),
    keras.layers.Dense(49, activation="relu"),
    keras.layers.Dense(10, activation="softmax")
])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

model.fit(train_data, train_labels, epochs=15)

model.save("digits_classification.h5")'''

model = keras.models.load_model("digits_classification.h5")


print(model.evaluate(test_data, test_labels))

prediction = model.predict(test_data)
for i in range(100):
    print("Prediction: ", np.argmax(prediction[i]))
    print("Actual: ", test_labels[i])