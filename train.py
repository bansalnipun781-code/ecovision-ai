# 1. Imports
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# 2. Load data
train_dir = r"C:\Users\asus\OneDrive\Documents\split_data\train"
val_dir = r"C:\Users\asus\OneDrive\Documents\split_data\val"

train_gen = ImageDataGenerator(rescale=1./255)
val_gen = ImageDataGenerator(rescale=1./255)

train_data = train_gen.flow_from_directory(train_dir, target_size=(224,224))
val_data = val_gen.flow_from_directory(val_dir, target_size=(224,224))

# 3. Build model
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models

base_model = MobileNetV2(input_shape=(224,224,3), include_top=False, weights='imagenet')
base_model.trainable = False

x = layers.GlobalAveragePooling2D()(base_model.output)
x = layers.Dense(256, activation='relu')(x)
x = layers.Dropout(0.3)(x)
output = layers.Dense(train_data.num_classes, activation='softmax')(x)

model = models.Model(inputs=base_model.input, outputs=output)

# 4. Compile
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 5. Train
print("Starting training...")
from tensorflow.keras.callbacks import EarlyStopping

early_stop = EarlyStopping(patience=3, restore_best_weights=True)

model.fit(
    train_data,
    validation_data=val_data,
    epochs=1,
    callbacks=[early_stop]
)
print(train_data.class_indices)
model.save("recycle_model.h5")
