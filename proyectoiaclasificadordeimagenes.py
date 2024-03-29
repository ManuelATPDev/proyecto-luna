# -*- coding: utf-8 -*-
"""ProyectoIAClasificadordeImagenes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EKRoLojYhtFL4I7YXQG2CMk8T4Th0YsV

# **PROYECTO LUNA:**
Permite clasificar imagenes e imprimir su resultado en el equivalente a lenguaje de señas.

El sistema tiene el potencial de ser una herramienta valiosa para las personas que son sordas o tienen problemas de audición. Les permitirá comunicarse más fácilmente con el mundo que los rodea. El sistema también tiene el potencial de ser una herramienta valiosa para la educación. Se puede utilizar para ayudar a las personas a aprender lenguaje de señas y para proporcionar subtítulos para videos y películas.

## **Librerias Necesarias**
"""

import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt
import cv2 #se usa para modificar el tamaño y color de las imagenes
from tensorflow.keras.callbacks import TensorBoard #se usa para ver graficas
from tensorflow.keras.preprocessing.image import ImageDataGenerator #generar nuevas imagenes
plt.style.use('fivethirtyeight')

"""## Cargamos el dataset a utilizar
CIFAR-10 es un conjunto de datos de imágenes de entrenamiento y prueba para la clasificación de imágenes de objetos. El conjunto de datos contiene 60.000 imágenes de 10 clases diferentes: avión, automóvil, pájaro, gato, ciervo, perro, rana, caballo, barco y camión. Cada clase tiene 6.000 imágenes, 5.000 para entrenamiento y 1.000 para pruebas. Todas las imágenes son de 32x32 píxeles y están en color.
"""

datos, metadatos = tfds.load('cifar10', as_supervised=True, with_info=True)

"""# Miramos los tipos de datos"""

metadatos

"""## Mostramos ejemplos de las imagenes contenidas en CIFAR-10.

*   0 -> airplane
*   1 -> automobile
*   2 -> bird
*   3 -> cat
*   4 -> deer
*   5 -> dog
*   6 -> frog
*   7 -> horse
*   8 -> ship
*   9 -> truck
"""

tfds.show_examples(datos['train'], metadatos)

"""## Para obtener mayor informacion de las imagenes se usa matplotlib"""

#Para configurar el tamaño que se muestran las imagenes
plt.figure(figsize=(20,20))

#Se recorre las imagenes de 20 en 20 ordenados en una matriz de 5x5
for i, (imagen, etiqueta) in enumerate(datos['train'].take(20)):
  plt.subplot(5,5,i+1)
  plt.imshow(imagen)

"""## Se crea la matriz de entrenamiento y de test"""

datos_entrenamiento = []
for i, (imagen, etiqueta) in enumerate(datos['train']):
    imagen = cv2.resize(imagen.numpy(), (32,32))
    imagen = imagen.reshape(32,32,3)
    datos_entrenamiento.append([imagen, etiqueta])

datos_test = []
for i, (imagen, etiqueta) in enumerate(datos['test']):
   imagen = cv2.resize(imagen.numpy(), (32,32))
   imagen = imagen.reshape(32,32,3)
   datos_test.append([imagen, etiqueta])

"""## Verificamos el tamaño del arreglo (50.000 para train y 10.000 para test)"""

len(datos_entrenamiento)

len(datos_test)

"""## Leemos el dato de la posicion 0 del arreglo y asignamos las imagenes y las etiquetas a unos arreglos especificos"""

x_train = [] #imagenes de entrenamiento (pixeles)
y_train = [] #etiquetas

for imagen,etiqueta in datos_entrenamiento:
  x_train.append(imagen)
  y_train.append(etiqueta)

x_test = [] #imagenes de test (pixeles)
y_test = [] #etiquetas

for imagen,etiqueta in datos_test:
  x_test.append(imagen)
  y_test.append(etiqueta)

"""Posicion 0 en la matriz principal"""

datos_entrenamiento[0]

datos_test[0]

"""Posicion 0 en la matriz x"""

x_train[0]

x_test[0]

"""Posicion 0 en la matriz y"""

y_train[1]

clasificacion = ['avión', 'carro', 'ave', 'gato', 'ciervo', 'perro', 'rana', 'caballo', 'barco', 'camión']

print('La clase de la imagen es:', clasificacion[y_train[1]])

y_test[0]

"""## Convertimos las etiquetas en un conjunto de 10 numeros categorizados para la red neuronal"""

y_train_cat = to_categorical(y_train)
y_test_cat = to_categorical(y_test)

print(y_train_cat)
print('\n',y_train_cat[0])

"""## Procedemos a normalizar los valores de los pixeles (x)"""

x_train = np.array(x_train).astype(float) / 255
x_test = np.array(x_test).astype(float) / 255

x_train[0]

x_test[0]

"""## Definimos el modelo a utilizar.
 Sera una red neuronal convolucional (CNN). Las CNN son un tipo de red neuronal que se caracteriza por el uso de filtros convolucionales, que son operaciones matemáticas que se aplican a las imágenes para extraer características locales.
"""

modeloCNN = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(32,32,3)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(500, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

"""## Se compila el modelo"""

modeloCNN.compile(optimizer='adam',
                    loss='categorical_crossentropy',
                    metrics = ['accuracy'])

"""## Se entrena el modelo y se utiliza TensorBoard para guardar los resultados de las epocas"""

tensorboardCNN = TensorBoard(log_dir='logs/CNN')
modeloCNN.fit(x_train,y_train_cat, batch_size=256,
                validation_split=0.2,
                epochs=200,
                callbacks=[tensorboardCNN]) #guardar en un archivo el resultado de la epoca

"""## Abrir gráfica"""

# Commented out IPython magic to ensure Python compatibility.
# %load_ext tensorboard
# %tensorboard --logdir logs

"""## Tratamiento con Aumento de Datos"""

plt.figure(figsize=(20,8))
for i in range(10):
  plt.subplot(2,5,i+1)
  plt.imshow(x_train[i])

datagen = ImageDataGenerator(
    rotation_range=50, #angulo maximo aleatoria de las imagenes
    width_shift_range=0.2, #mover
    height_shift_range=0.2,
    shear_range=15,
    zoom_range=[0.7, 1.4],
    horizontal_flip=True,
    vertical_flip=True
)

datagen.fit(x_train)

plt.figure(figsize=(20,8))

for imagen, etiqueta in datagen.flow(x_train, y_train, batch_size=10, shuffle=False):
  for i in range(10):
    plt.subplot(2,5,i+1)
    plt.imshow(imagen[i])
  break

modeloCNN_2 = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(32,32,3)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(500, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

modeloCNN_2.compile(optimizer='adam',
                    loss='categorical_crossentropy',
                    metrics = ['accuracy'])

x_entrenamiento = x_train[:40000]
x_validacion = x_train[40000:]

y_entrenamiento = y_train_cat[:40000]
y_validacion = y_train_cat[40000:]

data_gen_entrenamiento = datagen.flow(x_entrenamiento, y_entrenamiento, batch_size=256)

tensorboardCNN_2 = TensorBoard(log_dir='logs/CNN2')

modeloCNN_2.fit(
    data_gen_entrenamiento,
    epochs=200, batch_size=256,
    validation_data=(x_validacion, y_validacion),
    steps_per_epoch=int(np.ceil(len(x_entrenamiento)/float(256))),
    validation_steps=int(np.ceil(len(x_validacion)/float(256))),
    callbacks=[tensorboardCNN_2]
)

"""## Comparación de ambos modelos
Podemos observar que para el modelo con tratamiento de datos tiene una tendencia todavia bastante fuerte al alza, y la perdida a la baja. El modelo sin aumento de datos posee una mayor precisión, pero un leve estancamiento en la precisión y la perdida.
"""

# Commented out IPython magic to ensure Python compatibility.
# %load_ext tensorboard
# %tensorboard --logdir logs

"""## Evaluar el modelo CNN y CNN2"""

modeloCNN.evaluate(x_test,y_test_cat)[1]
modeloCNN_2.evaluate(x_test,y_test_cat)[1]

from google.colab import files
uploaded = files.upload()

# Mostrar la imagen
for name in uploaded.keys():
    nombre = name

new_image = plt.imread(nombre)
img = plt.imshow(new_image)

# Cambiar el tamaño
from skimage.transform import resize
new_image_resize = resize(new_image, (32,32,3))
img = plt.imshow(new_image_resize)

# Obtener la prediccion
prediccion = modeloCNN.predict(np.array([new_image_resize]))

prediccion

list_index = [0,1,2,3,4,5,6,7,8,9]
x = prediccion

for i in range(10):
  for j in range(10):
    if x[0][list_index[i]] > x[0][list_index[j]]:
      temp = list_index[i]
      list_index[i] = list_index[j]
      list_index[j] = temp

print(list_index)

for i in range(5):
  print(clasificacion[list_index[i]], ':', round(prediccion[0][list_index[i]]*100, 2), '%')

prediccion2 = modeloCNN_2.predict(np.array([new_image_resize]))

prediccion2

list_index2 = [0,1,2,3,4,5,6,7,8,9]
x2 = prediccion2

for i in range(10):
  for j in range(10):
    if x[0][list_index2[i]] > x2[0][list_index2[j]]:
      temp2 = list_index2[i]
      list_index2[i] = list_index2[j]
      list_index2[j] = temp2

print(list_index2)

for i in range(5):
  print(clasificacion[list_index2[i]], ':', round(prediccion2[0][list_index2[i]]*100, 2), '%')

"""## Reproducir el video equivalente a lenguaje de señas"""

from google.colab import drive
drive.mount("/content/drive/")

import imageio
import matplotlib.animation as animation
from skimage.transform import resize
from IPython.display import HTML

def display_video(video):
    fig = plt.figure(figsize=(3,3))  #Display size specification

    mov = []
    for i in range(len(video)):  #Append videos one by one to mov
        img = plt.imshow(video[i], animated=True)
        plt.axis('off')
        mov.append([img])

    #Animation creation
    anime = animation.ArtistAnimation(fig, mov, interval=50, repeat_delay=1000)

    plt.close()
    return anime

"""*Videos creados por: [Lengua de Señas Colombiana - LSC](https://www.youtube.com/@lenguadesenascolombiana-ls5517)*

*Realizado por una estudiante de LSC, Susan Renee English y por Ximena Flórez Castrillón, Magíster en Comunicación Transmedia.*
"""

nombre_video = '/content/drive/MyDrive/Colab Notebooks/videos/'+str(clasificacion[list_index[0]])+'.mp4'

video = imageio.mimread(nombre_video)  #cargar el video
HTML(display_video(video).to_html5_video())  #ejecutarlo en formato HTML

"""## Exportamos el modelo para ser usado en HTML"""

modeloCNN.save('ProyectoLuna.h5')
modeloCNN_2.save('ProyectoLuna2.h5')

!pip install tensorflowjs

!mkdir carpeta_salida

!mkdir carpeta_salida2

!tensorflowjs_converter --input_format keras ProyectoLuna.h5 carpeta_salida

!tensorflowjs_converter --input_format keras ProyectoLuna2.h5 carpeta_salida2