import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Загрузка датасета MNIST
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Нормализация данных
x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

# Преобразование меток в one-hot encoding
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# Изменение формы данных для CNN: (28, 28) -> (28, 28, 1)
x_train = x_train.reshape(-1, 28, 28, 1)
x_test = x_test.reshape(-1, 28, 28, 1)

# Создание генератора с аугментацией
datagen = ImageDataGenerator(
    rotation_range=15,     # Поворот
    width_shift_range=0.1,  # Сдвиг по ширине
    height_shift_range=0.1,  # Сдвиг по высоте
    zoom_range=0.1,        # Масштабирование
    horizontal_flip=False,  # Отражение
    fill_mode='nearest'    # Заполнение пустых пикселей
)

# Подгонка генератора к обучающим данным
datagen.fit(x_train)

model = keras.Sequential([
    layers.Conv2D(16, kernel_size=(3, 3), activation='relu',
                  input_shape=(28, 28, 1)),  # Первый сверточный слой
    layers.MaxPooling2D(pool_size=(2, 2)),  # Слой подвыборки
    # Второй сверточный слой
    layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2, 2)),  # Второй слой подвыборки
    layers.Flatten(),  # Преобразование 2D в 1D
    layers.Dense(128, activation='relu'),  # Полносвязный слой
    layers.Dropout(0.5),  # Дропаут для регуляризации
    layers.Dense(10, activation='softmax')  # Выходной слой
])

model.compile(optimizer='adam', loss='categorical_crossentropy',
              metrics=['accuracy'])
model.summary()  # Вывод структуры модели

# history = model.fit(datagen.flow(x_train, y_train, batch_size=128),
#                     epochs=5, validation_data=(x_test, y_test), verbose=0)

history = model.fit(x_train, y_train, epochs=5,
                    batch_size=128, validation_split=0.2, verbose=0)

loss, accuracy = model.evaluate(x_train, y_train)
test_loss, test_accuracy = model.evaluate(x_test, y_test)

print(f"Потери: {loss:.4f}, Точность: {accuracy:.4f}")
print(f'Потери на тесте: {
      test_loss:.4f}, Точность на тесте: {test_accuracy:.4f}')

# model.save('cnn_1.keras')
