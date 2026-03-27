import tkinter as tk
from tkinter import messagebox
import random

# Definimos una Clase para organizar todo. En interfaces gráficas (GUI), 
# las clases son vitales para mantener el estado (puntos, tablero) unido.
class TresEnRaya:
    def __init__(self, root):
        """
        El 'Constructor'. Aquí se configura la ventana inicial y las variables.
        'root' es la ventana principal que nos da Tkinter.
        """
        self.root = root
        self.root.title("3 en Raya: Humillación Artificial")
        self.root.geometry("400x550")
        self.root.configure(bg="#2c3e50")

        # Variables de control del juego
        self.usuario = "O"
        self.maquina = "X"
        self.victorias = 0
        self.derrotas = 0
        self.tablero = [""] * 9  # Representación interna: una lista de 9 textos vacíos
        self.juego_activo = True

        # --- SECCIÓN DE INTERFAZ (UI) ---
        # Creamos el marcador de puntos
        self.label_puntos = tk.Label(
            self.root, 
            text=f"Tú (O): {self.victorias} | Máquina (X): {self.derrotas}",
            font=("Arial", 14, "bold"), bg="#2c3e50", fg="#ecf0f1", pady=20
        )
        self.label_puntos.pack() # .pack() coloca el elemento en la ventana

        # El 'Frame' es como un contenedor para agrupar los botones del tablero
        self.frame_tablero = tk.Frame(self.root, bg="#34495e", padx=10, pady=10)
        self.frame_tablero.pack()

        self.botones = []
        for i in range(9):
            # Creamos 9 botones. 
            # El truco 'command=lambda i=i: ...' es para que cada botón 
            # sepa qué número de posición (0-8) le corresponde al pulsarlo.
            btn = tk.Button(
                self.frame_tablero, text="", font=("Arial", 24, "bold"),
                width=5, height=2, bg="#ecf0f1", relief="flat",
                command=lambda i=i: self.click_usuario(i)
            )
            # .grid() coloca los botones en formato de tabla (filas y columnas)
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.botones.append(btn)

        # Botón para resetear los puntos
        self.btn_reset = tk.Button(
            self.root, text="Reiniciar Marcador", command=self.reset_total,
            bg="#e74c3c", fg="white", font=("Arial", 10, "bold")
        )
        self.btn_reset.pack(pady=20)

    def click_usuario(self, i):
        """Gestiona qué pasa cuando haces clic en una casilla."""
        # Solo actuamos si la casilla está vacía y el juego no ha terminado
        if self.tablero[i] == "" and self.juego_activo:
            self.hacer_movimiento(i, self.usuario)
            
            # Si tras tu movimiento el juego sigue, le toca a la máquina
            if self.juego_activo:
                # Usamos .after(ms, función) para que la máquina no responda al instante.
                # Da la sensación de que está 'procesando' tu derrota.
                self.root.after(500, self.movimiento_maquina)

    def hacer_movimiento(self, i, jugador):
        """Escribe en el tablero y comprueba si hay ganador."""
        self.tablero[i] = jugador
        color = "#3498db" if jugador == "O" else "#e67e22"
        
        # Actualizamos el aspecto del botón pulsado
        self.botones[i].config(
            text=jugador, 
            fg=color, 
            state="disabled", # Desactivamos el botón para que no se pulse dos veces
            disabledforeground=color
        )

        # Lógica de fin de partida
        if self.verificar_ganador(jugador):
            self.finalizar_partida(jugador)
        elif "" not in self.tablero:
            self.finalizar_partida("Empate")

    def movimiento_maquina(self):
        """Lógica simple para que la IA elija dónde poner su X."""
        if not self.juego_activo: return
        
        # Buscamos qué índices de la lista están vacíos ("")
        vacias = [i for i, x in enumerate(self.tablero) if x == ""]
        if vacias:
            eleccion = random.choice(vacias) # Elige una al azar
            self.hacer_movimiento(eleccion, self.maquina)

    def verificar_ganador(self, j):
        """Compara el tablero con las 8 posibles líneas ganadoras."""
        combos = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        # any() devuelve True si al menos una de las combinaciones se cumple
        return any(self.tablero[a] == self.tablero[b] == self.tablero[c] == j for a,b,c in combos)

    def finalizar_partida(self, resultado):
        """Muestra el mensaje de victoria/derrota y gestiona el reinicio."""
        self.juego_activo = False
        insultos = [
            "¿Tu cerebro funciona con pilas de botón?",
            "¡Patético! Hasta un error 404 tiene más sentido que tu juego.",
            "He visto routers con más visión de juego."
        ]

        if resultado == self.usuario:
            self.victorias += 1
            titulo, msg = "¡Milagro!", "Has ganado... Seguramente he tenido un lag cuántico."
        elif resultado == self.maquina:
            self.derrotas += 1
            titulo, msg = "¡HUMILLACIÓN!", random.choice(insultos)
        else:
            titulo, msg = "Empate", "Un empate. Qué aburrido, como tu forma de jugar."

        self.actualizar_puntos()
        
        # messagebox.askyesno crea una ventana con botones de Sí/No
        respuesta = messagebox.askyesno(titulo, f"{msg}\n\n¿Quieres otra ración de derrota?")
        if respuesta:
            self.reiniciar_tablero()
        else:
            self.root.destroy() # Cierra la ventana y el programa

    def actualizar_puntos(self):
        """Refresca el texto del marcador en la ventana."""
        self.label_puntos.config(text=f"Tú (O): {self.victorias} | Máquina (X): {self.derrotas}")

    def reiniciar_tablero(self):
        """Limpia la lógica y los botones para una nueva partida."""
        self.tablero = [""] * 9
        self.juego_activo = True
        for btn in self.botones:
            btn.config(text="", state="normal", bg="#ecf0f1")

    def reset_total(self):
        """Pone el contador de victorias a cero."""
        self.victorias = 0
        self.derrotas = 0
        self.actualizar_puntos()
        self.reiniciar_tablero()

# --- ARRANQUE DEL PROGRAMA ---
if __name__ == "__main__":
    root = tk.Tk()           # Crea el motor de la ventana
    app = TresEnRaya(root)   # Instancia nuestra clase
    root.mainloop()          # Mantiene la ventana abierta y escuchando clics