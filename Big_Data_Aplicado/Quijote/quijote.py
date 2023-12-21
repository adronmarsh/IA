import string
import pandas as pd
import os

def getActualPath():
    return os.path.abspath(os.path.dirname(__file__))

def countWords(archivo):
    with open(archivo, 'r', encoding='latin-1') as file:
        # Separa las palabras y las guarda en un DataFrame
        content = file.read().lower()
        translator = str.maketrans('', '', string.punctuation)
        words = content.translate(translator).split()
        df = pd.DataFrame(words, columns=['Palabra'])
        
        # Cuenta las veces que se repite cada palabra
        contador = df['Palabra'].value_counts().to_dict()

        return contador

# Guarda el DataFrame en un archivo CSV
def saveCSV(contador, nombre_archivo):
    currentPath = getActualPath()
    filePath = os.path.join(currentPath, nombre_archivo)
    df = pd.DataFrame(list(contador.items()), columns=['Palabra', 'Frecuencia'])
    df.to_csv(filePath, index=False)

def main():
    currentPath = getActualPath()
    file = os.path.join(currentPath, 'quijote-es.txt')

    if os.path.exists(file):
        contador = countWords(file)
        saveCSV(contador, 'resultsQuijote.csv')
    else:
        print(f'Error: El archivo "{file}" no existe.')

if __name__ == "__main__":
    main()
