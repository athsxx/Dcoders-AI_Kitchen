import zipfile
import os
from PIL import Image
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

def unzip_file(zip_file_path, extract_to_dir):
    if not os.path.isfile(zip_file_path):
        raise FileNotFoundError(f"The zip file {zip_file_path} does not exist.")

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_dir)

zip_file_path = 'testing-20240714T155116Z-001.zip'
extract_to_dir = 'testing'
zip_file = 'training-20240715T162634Z-001.zip'
extract = 'training'

os.makedirs(extract_to_dir, exist_ok=True)
os.makedirs(extract, exist_ok=True)
try:
    unzip_file(zip_file_path, extract_to_dir)
    print("Unzipping completed successfully.")
except FileNotFoundError as e:
    print(e)
try:
    unzip_file(zip_file, extract)
    print("Unzipping completed successfully.")
except FileNotFoundError as e:
    print(e)


def verify_and_remove_images(directory):
    corrupted_images = []
    for root, _, files in os.walk(directory):
        for file in files:
            try:
                img_path = os.path.join(root, file)
                img = Image.open(img_path)
                img.verify()  
            except (IOError, SyntaxError) as e:
                print(f"Corrupted image: {img_path}")
                corrupted_images.append(img_path)
                os.remove(img_path)  
                print(f"Removed corrupted image: {img_path}")
    return corrupted_images

dire1 = 'testing/testing'
dire2='training/training'

corrupted_train_images = verify_and_remove_images(dire2)
corrupted_test_images = verify_and_remove_images(dire1)
print(f"Found and removed {len(corrupted_train_images)} corrupted images in the training set.")
print(f"Found and removed {len(corrupted_test_images)} corrupted images in the test set.")

train_datagen = ImageDataGenerator(rescale=1./255,
                                   validation_split=0.2,  
                                   rotation_range=40,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True,
                                   fill_mode='nearest')

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(dire2,
                                                    target_size=(224, 224),
                                                    batch_size=128,
                                                    class_mode='categorical',
                                                    subset='training')

val_generator = train_datagen.flow_from_directory(dire2,
                                                  target_size=(224, 224),
                                                  batch_size=32,
                                                  class_mode='categorical',
                                                  subset='validation')
test_generator = test_datagen.flow_from_directory(dire1,
                                                  target_size=(224, 224),
                                                  batch_size=64,
                                                  class_mode='categorical')

base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(train_generator.num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(train_generator,
          validation_data=val_generator,
          epochs=5,
          steps_per_epoch=train_generator.samples // train_generator.batch_size,
          validation_steps=val_generator.samples // val_generator.batch_size)

loss, accuracy = model.evaluate(test_generator)
print(f'Test accuracy: {accuracy}')
