

import numpy as np
import os
import PIL
import PIL.Image
import tensorflow as tf
import pathlib

flowers = tf.keras.utils.get_file(
    'flower_photos',
    'https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz',
    untar=True)

img_gen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255, rotation_range=20)

#train_batches = image_data_generator.flow_from_directory(
#        directory=training_dataset_train_path,
#        target_size=(224, 224),
#        classes=['PNEUMONIA', 'NORMAL'],
#        batch_size=self.client_config.batch_size)

images = img_gen.flow_from_directory(flowers)
print(type(images))

ds = tf.data.Dataset.from_generator(
    lambda: images,
    output_types=(tf.float32, tf.float32),
    output_shapes=([32,256,256,3], [32,5])
)

print(type(ds))











