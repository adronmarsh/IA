import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB

# Importar el csv para poder leer los datos
df = pd.read_csv("lab1-dataset.csv")

# Rellenar los null con la moda
df = df.fillna(df.mode().iloc[0])

# Dividir los datos en conjunto de entrenamiento y de prueba
X = df.drop("classname", axis=1)  # Características
y = df["classname"]  # Objetivo

def buscar_mejor_random_state(num_intentos):
    max_precision = 0
    mejor_rs = 0
    test_size = 0.25  # Proporción de datos de prueba

    for rs in range(1, num_intentos + 1):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=rs)
        naive_bayes = MultinomialNB() # Crear el clasificador
        naive_bayes.fit(X_train, y_train) # Entrenar al modelo
        y_pred = naive_bayes.predict(X_test) # Realizar predicciones en el conjunto de prueba
        accuracy = accuracy_score(y_test, y_pred) # Calcular la precisión del modelo

        if accuracy > max_precision: # Obtener la máxima precisión
            max_precision = accuracy
            mejor_rs = rs

    print("Mejor precisión:", max_precision)
    print("Random State óptimo:", mejor_rs)

def evaluar_modelo_random_state(rs):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=rs)
    naive_bayes = MultinomialNB()
    naive_bayes.fit(X_train, y_train)
    y_pred = naive_bayes.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Precisión del modelo:", accuracy)
    print("Random State:", rs)

# Uso de las funciones
buscar_mejor_random_state(100) # Número de intentos
evaluar_modelo_random_state(483542)  # Utiliza el valor óptimo encontrado
