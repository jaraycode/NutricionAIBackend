import time, cv2, os # type: ignore
import numpy as np
import pandas as pd # type: ignore
from random import shuffle
from matplotlib import pyplot as plt # type: ignore

PATH = "../../dataset/food-101/food-101/meta/labels.txt"
LABELS = []
with open(PATH, "r") as labels:
    for line in labels:
        LABELS.append(line[:-1])
df_labels = pd.DataFrame(data=LABELS, columns=["Labels"])
df_labels.index = range(1, len(df_labels) + 1)
df_labels
PATH = "../../dataset/food-101/food-101/meta/test.txt"
IMG_NAMES = []
print("Extracting data for show images...")
time.sleep(2)

with open(PATH, "r") as train: 
    for line in train:
        IMG_NAMES.append(line[:-1])
    shuffle(IMG_NAMES)
    IMG_NAMES = IMG_NAMES[:1500]
    IMG_NAMES_COPY = IMG_NAMES[:2]

df_img_names = pd.DataFrame(columns=["Name","Label"])
for name in IMG_NAMES:
    new_row = pd.DataFrame(data=[[name.split("/")[1], name.split("/")[0]]], columns=["Name","Label"])
    df_img_names = pd.concat([df_img_names, new_row]).reset_index(drop=True)
df_img_names        

# %% [markdown]
# ## Extracción de las imagenes
# 
# Por medio de la extracción del nombre de las imágenes en el proceso anterior las pasamos por la función *imread* de la librería *cv2* que nos permitirá leer las imágenes y tenerlas en un arreglo para su posterior presentación con la librería **matplotlib**

# %%
images = [cv2.imread(f'/home/jonasaray/Workspace/NutricionAI/nutricionBackend/dataset/food-101/food-101/images/{img}.jpg') for img in IMG_NAMES_COPY]

# %%
plt.subplot(1,2,1)
plt.imshow(cv2.cvtColor(images[0], cv2.COLOR_BGR2RGB))
plt.xlabel(IMG_NAMES[0].split("/")[0])
plt.margins(y=10)

plt.subplot(1,2,2)
plt.imshow(cv2.cvtColor(images[1], cv2.COLOR_BGR2RGB))
plt.xlabel(IMG_NAMES[1].split("/")[0])

plt.show()

del images
del IMG_NAMES_COPY

# %% [markdown]
# # Vista minable
# 
# A partir del preview anterior tenemos una idea del proceso del cuál será parte la extracción de los datos para el modelo que se desea entrenar. Tomamos el mismo proceso anterior pero apartando 1000 imágenes que serán tomadas como imágenes de entrenamiento y prueba del modelo basado en las etiquetas que se tomen primero que serán guardadas en un archivo aparte para poder usarlas posteriormente.

# %%
del IMG_NAMES
del new_row
df_img_names

# %%
df_labels = pd.DataFrame(data=df_img_names["Label"].unique(), columns=["Label"])
df_labels = df_labels.sort_values(by='Label', ascending=True).reset_index(drop=True)
df_labels

# %%
os.makedirs('../../dataset/vista_minable/meta', exist_ok=True)
df_img_names.to_csv('../../dataset/vista_minable/meta/train_test_labels.csv', encoding='utf-8', index=False)
df_labels.to_csv('../../dataset/vista_minable/meta/labels.csv', encoding='utf-8', index=False)
del df_img_names
del df_labels

# %% [markdown]
# ## Procesamiento de las imagenes para entrenamiento
# 
# Una vez procesada la información de las imágenes que serán usadas para el entrenamiento del modelo procedemos a identificar las imágenes con un algoritmo que nos permite redimencionarlas para que sea más fácil para el modelo identificar las diferencias entre las mismas para de esta forma clasificarlas. Utilizaremos los siguientes pasos
# 
# 1. Sacar la información guardada en el archivo de la vista minable.
# 2. Pasar cada imagen por la función resize de nuestra librería para asegurarnos que la misma tenga el formato deseado (28x28).
# 3. Bajo un esquema similar al de la extracción de imágenes que se muestra con anterioridad pero con las 1000 imágenes que fueron apartadas.

# %%
df_img = pd.read_csv('../../dataset/vista_minable/meta/train_test_labels.csv')
df_img

# %%
df_labels = pd.read_csv('../../dataset/vista_minable/meta/labels.csv')
df_labels.index = range(1, len(df_labels) + 1)
df_labels

# %%
images_training = [cv2.imread(f'/home/jonasaray/Workspace/NutricionAI/nutricionBackend/dataset/food-101/food-101/images/{label}/{name}.jpg') for name, label in df_img.values]

images_training = [cv2.resize(img, (100, 100)) for img in images_training]

plt.subplot(1,2,1)
plt.imshow(cv2.cvtColor(images_training[0], cv2.COLOR_BGR2RGB))
plt.xlabel(df_img.values[0][1])
plt.margins(y=10)

plt.subplot(1,2,2)
plt.imshow(cv2.cvtColor(images_training[1], cv2.COLOR_BGR2RGB))
plt.xlabel(df_img.values[1][1])

plt.show()

# %% [markdown]
# ## Diseño del modelo
# 
# Se busca con el mismo poder analizar imágenes, ya sea provenientes del módulo de la aplicación así como dentro de las pruebas internas para asegurar que el modelo fue entrenado de manera adecuada. Se busca utilizar las siguientes capas para este modelo, cómo lo son:
# 
# * *Conv2D*: capa encargada de analizar la imagen por medio de una mátriz o kernel que busca identificar las características más relevantes de la misma. Entendiendo que mientras más capas existan dentro de la jerarquía puede analizar características mucho más complejas de la imagen en cuestión.
# * *MaxPooling2D*: Reduce el tamaño del mapa generado por la capa anterior para de esta manera preservar las características más relevantes de los datos suministrados.
# * *Flatten*: permite moldear los datos a un arreglo lineal para posterior análisis dependiendo de los datos que se tengan producto de las capas anteriores.
# * *Dense*: las capas densas son la forma más básica dentro de los modelos que permiten realizar cálculos con respecto a los valores previamente presentados con su respectiva capa de activación, para este caso se va a usar *ReLU* para el análisis preliminar antes de brindar una respuesta definitiva usando la capa *softmax*.

# %%
import tensorflow # type: ignore
from tensorflow.keras.models import Sequential, save_model # type: ignore
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout # type: ignore
from tensorflow.keras.metrics import SparseCategoricalAccuracy # type: ignore
from tensorflow.keras.losses import SparseCategoricalCrossentropy # type: ignore

# %%
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 3), padding='same'),
    MaxPooling2D((2,2)),
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.03),
    Dense(512, activation='relu'),
    Dropout(0.03),
    Dense(len(df_labels) + 1, activation='softmax') 
])

model.compile(loss=SparseCategoricalCrossentropy(from_logits=True), optimizer='adam', metrics=[SparseCategoricalAccuracy()])

model.summary()

# %%
def grafic_loss(modelo):
    epochs = range(len(modelo.history["loss"]))
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.plot(epochs, modelo.history["loss"], "-b", label="Training loss")
    plt.plot(epochs, modelo.history["val_loss"], "-r", label="Validation loss")    
    plt.legend(loc="upper right")
    plt.show()

def grafic_accuracy(modelo):
    epochs = range(len(modelo.history["sparse_categorical_accuracy"]))
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.plot(epochs, modelo.history["sparse_categorical_accuracy"], "-b", label="Training accuracy")
    plt.plot(epochs, modelo.history["val_sparse_categorical_accuracy"], "-r", label="Validation accuracy")    
    plt.legend(loc="upper right")
    plt.show()

# %%
def compare_row(row):
    for index, value in df_labels.iterrows():
        if row['Label'] == value.values[0]:
            return index

df_img['Label'] = df_img.apply(compare_row, axis=1)
df_img

# %%
def toFloat(img):
    return img/255.
images_training = list(map(toFloat, images_training))
ds_train = tensorflow.convert_to_tensor(images_training[:1200], tensorflow.float32)
ds_labels_train = tensorflow.convert_to_tensor(df_img["Label"].values[:1200], tensorflow.int32)
ds_test = tensorflow.convert_to_tensor(images_training[1200:], tensorflow.float32)
ds_labels_test = tensorflow.convert_to_tensor(df_img["Label"].values[1200:], tensorflow.int32)

# %%
historial = model.fit(ds_train, ds_labels_train, epochs=10, validation_data=[ds_test, ds_labels_test])

# %%
grafic_loss(historial)
grafic_accuracy(historial)

# %%
# model.save("my_model.keras")
model.export("my_model")
# save_model(model,"../app/Utils/trainnedModel")

# %%
prueba = model.predict(ds_test)

# %% [markdown]
# # Pruebas
# 
# Por medio del comando **predict** podemos analizar una serie de imágenes para identificar si el modelo es capaz de analizar las imágenes previamente procesadas de la misma forma como se procesaron las imágenes para el entrenamiento así el modelo es tomado a prueba a ver que tipo de respuestas nos puede entregar, podemos ver casos tanto de error como de aciertos como los siguientes:

# %%
plt.subplot(1,1,1)
plt.imshow(cv2.cvtColor((images_training[1202]*255).astype(np.uint8), cv2.COLOR_BGR2RGB))
plt.xlabel(df_labels.iloc[df_img["Label"].values[1202]])
plt.margins(y=10)

plt.show()

# %%
df_labels.iloc[np.argmax(prueba[2])].values[0]

# %%
model2 = tensorflow.keras.models.load_model("my_model.keras")



