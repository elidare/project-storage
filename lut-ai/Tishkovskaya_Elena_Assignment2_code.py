# Assignment II: Image processing and prediction
# The second assignment is about image processing and prediction.
# You will train a model based on the CNN architecture to classify the images in the dataset provided. In addition, you will need to fine-tune an existing model using ResNet as the backbone.
# You should experiment with different hyperparameters and compare the performance of the two models.
# Pay attention to preprocessing the images by resizing, scaling, and rotating them to a coherent form. 

import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import accuracy_score, classification_report


CLASSES = 10
cifar10 = datasets.cifar10
(x_train, y_train), (x_test, y_test) = cifar10.load_data()
# Making the labels 1-dimensional ([0 1 2 ...] instead of [[0] [1] [2] ...])
x_test, y_test = x_test.squeeze(), y_test.squeeze()

# Resizing the images to a consistent size
x_train, x_test = tf.image.resize(x_train, [32, 32]), tf.image.resize(x_test, [32, 32])
# Normalizing pixel size
x_train, x_test = x_train / 255.0, x_test / 255.0


def cnn(x_train, y_train, x_test, y_test):
    model = models.Sequential()
    model.add(layers.Input((32, 32, 3)))
    model.add(layers.Conv2D(32, (3, 3), padding='same', activation='relu'))
    model.add(layers.MaxPooling2D((2, 2), strides=2))
    model.add(layers.Conv2D(64, (3, 3), padding='same', activation='relu'))
    model.add(layers.MaxPooling2D((2, 2), strides=2))
    model.add(layers.Conv2D(64, (3, 3), padding='same', activation='relu'))
    model.add(layers.MaxPooling2D((2, 2), strides=2))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(CLASSES, activation='softmax'))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

    model.fit(x_train, y_train, epochs=20, batch_size=128, validation_data=(x_test, y_test))

    # Make predictions
    y_pred = model.predict(x_test)
    # Convert probabilities to class indices
    y_pred_classes = tf.argmax(y_pred, axis=1)

    print('Test Accuracy:', accuracy_score(y_test, y_pred_classes))
    print(classification_report(y_test, y_pred_classes))


def cnn_resnet(x_train, y_train, x_test, y_test):
    # One-hot encode the labels
    y_train_hot_enc = to_categorical(y_train, 10)
    y_test_hot_enc = to_categorical(y_test, 10)

    base_model = ResNet50(weights="imagenet", include_top=False, input_shape=(32, 32, 3))
    base_model.trainable = False  # Freezing the layers

    x = base_model.output
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dense(256, activation='relu')(x)
    output_layer = layers.Dense(CLASSES, activation='softmax')(x)

    model = models.Model(inputs=base_model.input, outputs=output_layer)

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(x_train, y_train_hot_enc, epochs=20, batch_size=128, validation_data=(x_test, y_test_hot_enc))

    # Make predictions
    y_pred = model.predict(x_test)
    # Convert probabilities to class indices
    y_pred_classes = tf.argmax(y_pred, axis=1)

    print('Test Accuracy:', accuracy_score(y_test, y_pred_classes))
    print(classification_report(y_test, y_pred_classes))


# cnn(x_train, y_train, x_test, y_test)
cnn_resnet(x_train, y_train, x_test, y_test)
