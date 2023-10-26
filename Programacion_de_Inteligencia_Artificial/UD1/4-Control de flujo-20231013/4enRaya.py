def menu():
    while True:
        
        header = """

    ██╗  ██╗    ███████╗███╗   ██╗    ██████╗  █████╗ ██╗   ██╗ █████╗ 
    ██║  ██║    ██╔════╝████╗  ██║    ██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗
    ███████║    █████╗  ██╔██╗ ██║    ██████╔╝███████║ ╚████╔╝ ███████║
    ╚════██║    ██╔══╝  ██║╚██╗██║    ██╔══██╗██╔══██║  ╚██╔╝  ██╔══██║
        ██║    ███████╗██║ ╚████║    ██║  ██║██║  ██║   ██║   ██║  ██║
        ╚═╝    ╚══════╝╚═╝  ╚═══╝    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
                                                                    

    """
        print(header)

        print("1. Jugar")
        print("2. Salir")
        
        choice = input("Elige una opción (1 o 2): ")
        
        if choice == "1":
            gameplay()
        elif choice == "2":
            print("Gracias por jugar. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, elige 1 para jugar o 2 para salir.")

def create_dashboard(rows, columns):
    dashboard = [["➖"] * columns for _ in range(rows)]
    return dashboard

def print_dashboard(dashboard):
    """ Imprimir números de columna """
    # print("   ".join(str(i) for i in range(1, len(dashboard[0]) + 1)))
    print("1️⃣  2️⃣  3️⃣  4️⃣  5️⃣  6️⃣  7️⃣")
    for row in dashboard:
        for card in row:
            print(card, end=" ")
        print()

def insert_card(dashboard, player, column):
    if 1 <= column <= len(dashboard[0]):
        for row in range(len(dashboard) - 1, -1, -1):
            if dashboard[row][column - 1] == "➖":
                dashboard[row][column - 1] = player
                return True
    return False

def is_victory(dashboard, player):
    # Verificar filas
    for row in dashboard:
        if "".join(row).count(player * 4) > 0:
            return True

    # Verificar columnas
    for col in range(len(dashboard[0])):
        column = [row[col] for row in dashboard]
        if "".join(column).count(player * 4) > 0:
            return True

    # Verificar diagonales principales
    for i in range(len(dashboard) - 3):
        for j in range(len(dashboard[0]) - 3):
            diagonal = [dashboard[i + k][j + k] for k in range(4)]
            if "".join(diagonal).count(player * 4) > 0:
                return True

    # Verificar diagonales secundarias
    for i in range(len(dashboard) - 3):
        for j in range(3, len(dashboard[0])):
            diagonal = [dashboard[i + k][j - k] for k in range(4)]
            if "".join(diagonal).count(player * 4) > 0:
                return True

    return False

def gameplay():
    rows = 6
    columns = 7
    dashboard = create_dashboard(rows, columns)
    current_player = "🔵"

    while True:
        print_dashboard(dashboard)
        try:
            column = int(input(f"Pulsa 9 para acabar en empate\nTurno de {current_player}, elige una columna (1-{columns}): "))
            if column == 9 : print("La partida ha terminado en empate!"); break
            if insert_card(dashboard, current_player, column):
                if is_victory(dashboard, current_player):
                    print_dashboard(dashboard)
                    print(f"¡El jugador {current_player} ha ganado!")
                    break
                current_player = "🔵" if current_player == "❌" else "❌"
            else:
                print("La columna está llena o no es válida. Elige otra.")
        except ValueError:
            pass

if __name__ == "__main__":
    menu()
