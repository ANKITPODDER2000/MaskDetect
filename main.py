# -*- coding: utf-8 -*-
"""mask.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bH-jh9o9yKqtyuNB-7eoUH-JZoNupQfW
"""

from google.colab import files
 files.upload()

! mkdir ~/.kaggle
! cp kaggle.json ~/.kaggle/

!kaggle datasets download -d ashishjangra27/face-mask-12k-images-dataset

import shutil

shutil.copy("/content/face-mask-12k-images-dataset.zip","/content/drive/My Drive/CNN/MaskDetect")

# Commented out IPython magic to ensure Python compatibility.
import os
import PIL
import tensorflow as tf
import matplotlib.pyplot as plt
# %matplotlib inline
import numpy as np
import zipfile
import cv2

os.chdir("/content/drive/My Drive/CNN/MaskDetect")
print(os.getcwd())

fl = zipfile.ZipFile("face-mask-12k-images-dataset.zip" , "r")
os.mkdir("./data")

fl.extractall("./data")

os.listdir("./data/Face Mask Dataset")

os.listdir("./data/Face Mask Dataset/Test")

print("No of Images(./data/Face Mask Dataset/Train/WithMask) : ",len(os.listdir("./data/Face Mask Dataset/Train/WithMask")))
print("No of images(./data/Face Mask Dataset/Train/WithoutMask) : ",len("./data/Face Mask Dataset/Train/WithoutMask"))

train_dir = "/content/drive/My Drive/CNN/MaskDetect/data/Face Mask Dataset/Train"
test_dir  = "/content/drive/My Drive/CNN/MaskDetect/data/Face Mask Dataset/Test"

train_data_gen = tf.keras.preprocessing.image.ImageDataGenerator(rescale = (1.0 / 255.0) ,
                                                                 height_shift_range = 0.15 ,
                                                                 width_shift_range = 0.15 ,
                                                                 zoom_range = 0.15 ,
                                                                 horizontal_flip = True)

test_data_gen  = tf.keras.preprocessing.image.ImageDataGenerator(rescale = (1.0 / 255.0))

a = cv2.imread("/content/drive/My Drive/CNN/MaskDetect/data/Face Mask Dataset/Test/WithoutMask/4179.png")
a.shape

train_data = train_data_gen.flow_from_directory(train_dir , batch_size = 32 , target_size = (128 , 128) , class_mode = "binary")
test_data  = train_data_gen.flow_from_directory(test_dir , batch_size = 32 , target_size = (128 , 128) , class_mode = "binary")

_ , ax = plt.subplots(1,5,figsize=(20,5))
for i in range(5):
  ax[i].imshow(train_data[0][0][10])
  ax[i].set_title(str(train_data[0][1][10]))

train_data.class_indices

model1 = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(16 , (3,3) , activation = "relu" , input_shape = (128 , 128 , 3)),
    tf.keras.layers.MaxPool2D((2,2)),
    tf.keras.layers.Conv2D(32 , (3,3) , activation = "relu"),
    tf.keras.layers.MaxPool2D((2,2)),
    tf.keras.layers.Conv2D(64 , (3,3) , activation = "relu"),
    tf.keras.layers.MaxPool2D((2,2)),
    tf.keras.layers.Conv2D(64 , (3,3) , activation = "relu"),
    tf.keras.layers.MaxPool2D((2,2)),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(256 , activation = "relu"),
    tf.keras.layers.Dense(256 , activation = "relu"),
    tf.keras.layers.Dense(1 , activation = "sigmoid")
])
model1.compile(optimizer = "rmsprop" , loss = tf.keras.losses.binary_crossentropy , metrics = ['acc'])
#model1.summary()

his1 = model1.fit(train_data ,
                  steps_per_epoch = train_data.n//train_data.batch_size ,
                  epochs = 15 ,
                  validation_data = test_data ,
                  validation_steps = test_data.n // test_data.batch_size)

model2 = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(16 , (3,3) , activation = "relu" , input_shape = (128 , 128 , 3)),
    tf.keras.layers.MaxPool2D((2,2)),
    tf.keras.layers.Conv2D(32 , (3,3) , activation = "relu"),
    tf.keras.layers.MaxPool2D((2,2)),
    tf.keras.layers.Conv2D(64 , (3,3) , activation = "relu"),
    tf.keras.layers.MaxPool2D((2,2)),
    tf.keras.layers.Conv2D(64 , (3,3) , activation = "relu"),
    tf.keras.layers.MaxPool2D((2,2)),
    tf.keras.layers.Conv2D(64 , (3,3) , activation = "relu"),
    tf.keras.layers.MaxPool2D((2,2)),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(256 , activation = "relu"),
    tf.keras.layers.Dense(256 , activation = "relu"),
    tf.keras.layers.Dense(1 , activation = "sigmoid")
])
model2.compile(optimizer = "rmsprop" , loss = tf.keras.losses.binary_crossentropy , metrics = ['acc'])
#model1.summary()

his2 = model2.fit(train_data ,
                  steps_per_epoch = train_data.n//train_data.batch_size ,
                  epochs = 15 ,
                  validation_data = test_data ,
                  validation_steps = test_data.n // test_data.batch_size)

class_gen = {}
for k,v in train_data.class_indices.items():
    class_gen[v] = k
print(class_gen)

#prediction for model1
img = tf.keras.utils.get_file("img1.jpg","https://i.insider.com/5e7cded7ba85ee690669c204?width=1035&format=jpeg")
img = tf.keras.preprocessing.image.load_img(img , target_size = (128 , 128))
img_ = tf.keras.preprocessing.image.img_to_array(img)
print("Shape of img : ",img_.shape)
#plt.imshow(img_)
#plt.show()
img_ = img_ / 255
plt.imshow(img)
plt.title(class_gen[model1.predict_classes(img_[np.newaxis , :])[0,0]])

#prediction for model1
img = tf.keras.utils.get_file("img1.jpg","https://i.insider.com/5e7cded7ba85ee690669c204?width=1035&format=jpeg")
img = tf.keras.preprocessing.image.load_img(img , target_size = (128 , 128))
img_ = tf.keras.preprocessing.image.img_to_array(img)
print("Shape of img : ",img_.shape)
#plt.imshow(img_)
#plt.show()
img_ = img_ / 255
plt.imshow(img)
plt.title(class_gen[model2.predict_classes(img_[np.newaxis , :])[0,0]])
plt.show()

img = tf.keras.utils.get_file("img2.jpg","https://post.healthline.com/wp-content/uploads/2020/04/Male_Face_Mask_732x549-thumbnail-2.jpg")
print(img)
img = tf.keras.preprocessing.image.load_img(img , target_size = (128 , 128))
img_ = tf.keras.preprocessing.image.img_to_array(img)
print("Shape of img : ",img_.shape)
#plt.imshow(img_)
#plt.show()
img_ = img_ / 255
plt.imshow(img)
plt.title(class_gen[model1.predict_classes(img_[np.newaxis , :])[0,0]])

#prediction for model2
img = tf.keras.utils.get_file("img2.jpg","https://post.healthline.com/wp-content/uploads/2020/04/Male_Face_Mask_732x549-thumbnail-2.jpg")
print(img)
img = tf.keras.preprocessing.image.load_img(img , target_size = (128 , 128))
img_ = tf.keras.preprocessing.image.img_to_array(img)
print("Shape of img : ",img_.shape)
#plt.imshow(img_)
#plt.show()
img_ = img_ / 255
plt.imshow(img)
plt.title(class_gen[model2.predict_classes(img_[np.newaxis , :])[0,0]])

validation_data_gen = tf.keras.preprocessing.image.ImageDataGenerator(rescale = (1 / 255))

validation_data = validation_data_gen.flow_from_directory("/content/drive/My Drive/CNN/MaskDetect/data/Face Mask Dataset/Validation" , 
                                                          class_mode = "binary",
                                                          target_size = (128 , 128))

print("Model1 accurecy for validation data : %.3f"%(model1.evaluate(validation_data)[1] * 100))
print("Model2 accurecy for validation data : %.3f"%(model2.evaluate(validation_data)[1] * 100))

a = files.upload()

def pred(path , ax , model = model1):
    #prediction for model
    img = tf.keras.preprocessing.image.load_img(path , target_size = (128 , 128))
    img_ = tf.keras.preprocessing.image.img_to_array(img)
    print("Shape of img : ",img_.shape)
    #plt.imshow(img_)
    #plt.show()
    img_ = img_ / 255
    ax.imshow(img)
    ax.set_title(class_gen[model.predict_classes(img_[np.newaxis , :])[0,0]])

_ , ax = plt.subplots(1,2,figsize = (9,4))
pred("/content/drive/My Drive/CNN/MaskDetect/mask.jpg" , ax[0] , model1)
pred("/root/.keras/datasets/img2.jpg" , ax[1] , model1)