# https://www.tensorflow.org/tutorials/images/cnn?hl=en
# restnet 50 32x32
# base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(32, 32, 3)) (from tensorflow - from tensorflow.keras.applications import ResNet50)

import tensorflow as tf
from tensorflow.keras import datasets, layers, models, metrics
from sklearn.metrics import accuracy_score, classification_report


cifar10 = datasets.cifar10
(x_train, y_train), (x_test, y_test) = cifar10.load_data()
# Making the labels 1-dimensional ([0 1 2 ...] instead of [[0] [1] [2] ...])
x_test, y_test = x_test.squeeze(), y_test.squeeze()

# Resizing the images to a consistent size
x_train, x_test = tf.image.resize(x_train, [32, 32]), tf.image.resize(x_test, [32, 32])
# Normalizing pixel size
x_train, x_test = x_train / 255.0, x_test / 255.0

# Training the model
# https://keras.io/api/layers/convolution_layers/convolution2d/
model = models.Sequential()
model.add(layers.Input((32, 32, 3)))
model.add(layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))
model.summary()

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)

# Make predictions
y_pred = model.predict(x_test)

# Convert probabilities to class indices
y_pred_classes = tf.argmax(y_pred, axis=1)

print('Test Accuracy:', accuracy_score(y_test, y_pred_classes))
print(classification_report(y_test, y_pred_classes))
