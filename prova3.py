import glob
import os
import random
import shutil
import tempfile

from tensorflow import keras
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPool2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator

initializer = keras.initializers.RandomUniform(minval=0., maxval=.1, seed=23)

model = Sequential([
            Conv2D(filters=32, kernel_size=(3, 3), activation='relu', padding='same', input_shape=(224, 224, 3), kernel_initializer=initializer, bias_initializer=initializer),
            MaxPool2D(pool_size=(2, 2), strides=2),
            Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding='same', kernel_initializer=initializer, bias_initializer=initializer),
            MaxPool2D(pool_size=(2, 2), strides=2),
            #Dense(units=8,activation='relu',input_shape=(224, 224, 3)),
            Flatten(),
            Dense(units=2, activation='softmax', kernel_initializer=initializer, bias_initializer=initializer)
])


model.compile(optimizer=Adam(learning_rate=0.0000001), loss='categorical_crossentropy', metrics=['accuracy'])

image_data_generator = ImageDataGenerator(preprocessing_function=keras.applications.vgg16.preprocess_input)

b_size = 32

train_batches = image_data_generator.flow_from_directory(
    directory="/home/francesc/Escritorio/folder_client/chest_xray/train",
    target_size=(224, 224),
    classes=['PNEUMONIA', 'NORMAL'],
    batch_size=b_size,
    shuffle=True)

valid_batches = image_data_generator.flow_from_directory(
    directory="/home/francesc/Escritorio/folder_client/chest_xray/test",
    target_size=(224, 224),
    classes=['PNEUMONIA', 'NORMAL'],
    batch_size=b_size,
    shuffle=True)

for x in range(50):

    #train_batches = image_data_generator.flow_from_directory(
    #        directory="/home/francesc/Escritorio/fed_learning/chest_xray/train",
    #        target_size=(224, 224),
    #        classes=['PNEUMONIA', 'NORMAL'],
    #        batch_size=b_size,
    #        shuffle=True)

    #valid_batches = image_data_generator.flow_from_directory(
    #    directory="/home/francesc/Escritorio/fed_learning/chest_xray/test",
    #    target_size=(224, 224),
    #    classes=['PNEUMONIA', 'NORMAL'],
    #    batch_size=b_size,
    #    shuffle=True)




    model.fit(
            x=train_batches,
            # steps_per_epoch=50, ### aaaaah okay.
            epochs=1,
            validation_data=valid_batches,
            #validation_steps=5, ### aaaaah okay.
            #verbose=2
          )

    #model.evaluate(x= valid_batches)

    #### provaaaaaa: lo seguent sera que no recarreguis el dataset a cada epoch i treure steps_per_epoch i
    #### validation_steps... vale tocant el fitxer de CHEST_X_RAY...

    ## PARAMETRES IMPORTANTS PER MODIFICAR EL RITME DE LEARNING SON ALPHA I STEPS PER EPOCH...