def crear_tablero(filas, columnas):
    tablero = [["_"] * columnas for _ in range(filas)]
    return tablero

def imprimir_tablero(tablero):
    # Imprimir números de columna
    print(" ".join(str(i) for i in range(1, len(tablero[0]) + 1)))
    for fila in tablero:
        for ficha in fila:
            print(ficha, end=" ")
        print()


def introducir_ficha(tablero, jugador, columna):
    if 1 <= columna <= len(tablero[0]):
        for fila in range(len(tablero) - 1, -1, -1):
            if tablero[fila][columna - 1] == "_":
                tablero[fila][columna - 1] = jugador
                return True
    return False

def es_victoria(tablero, jugador):
    # Lógica para verificar la victoria
    pass

def juego_4_en_raya():
    filas = 6
    columnas = 7
    tablero = crear_tablero(filas, columnas)
    jugador_actual = "X"

    while True:
        imprimir_tablero(tablero)

        columna = int(input(f"Jugador {jugador_actual}, elige una columna (1-{columnas}): "))
        if introducir_ficha(tablero, jugador_actual, columna):
            if es_victoria(tablero, jugador_actual):
                imprimir_tablero(tablero)
                print(f"¡El jugador {jugador_actual} ha ganado!")
                break
            jugador_actual = "O" if jugador_actual == "X" else "X"
        else:
            print("La columna está llena o no es válida. Elige otra.")

if __name__ == "__main__":
    juego_4_en_raya()
