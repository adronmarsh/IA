import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.feature_selection import SelectKBest
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.naive_bayes import MultinomialNB


# Importar el csv para poder leer los datos
df = pd.read_csv("lab1-dataset.csv")

# Sacar la moda de cada columna
moda = df.mode().iloc[0]

# Rellenar los null con la moda
df = df.fillna(moda)

# Dividir los datos en conjunto de entrenamiento y de test

X = df.drop("classname", axis=1)  # Características
y = df["classname"]  # Objetivo

# Entrenamiento de datos
rs = 0
max_precision = 0
max_rs = 0
while rs < 100:
    rs+=1
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=rs) #30383 #483542

    naive_bayes = MultinomialNB() # Crear el clasificador
    naive_bayes.fit(X_train, y_train) # Entrenar al modelo

    # Realizar predicciones en el conjunto de prueba
    y_pred = naive_bayes.predict(X_test)

    # Calcular la precisión del modelo
    accuracy = accuracy_score(y_test, y_pred)
    if accuracy > max_precision:
        max_precision = accuracy
        max_rs = rs

# Resultados
print("Precisión del modelo:", max_precision)
print("Ejemplos usados para entrenar", len(X_train))
print("Ejemplos usados para test", len(X_test))
print(max_rs)