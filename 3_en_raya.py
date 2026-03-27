import tkinter as tk
from tkinter import messagebox
import random

class TresEnRaya:
    def __init__(self, root):
        self.root = root
        self.root.title("3 en Raya: Humillación Artificial")
        self.root.geometry("400x550")
        self.root.configure(bg="#2c3e50") # Fondo elegante oscuro

        # Variables de estado
        self.usuario = "O"
        self.maquina = "X"
        self.victorias = "0"
        self.derrotas = 0
        self.tablero = [""] * 9
        self.juego_activo = True

        # --- Interfaz ---
        self.label_puntos = tk.Label(
            self.root, 
            text=f"Tú (O): {self.victorias} | Máquina (X): {self.derrotas}",
            font=("Arial", 14, "bold"), bg="#2c3e50", fg="#ecf0f1", pady=20
        )
        self.label_puntos.pack()

        # Contenedor del tablero
        self.frame_tablero = tk.Frame(self.root, bg="#34495e", padx=10, pady=10)
        self.frame_tablero.pack()

        self.botones = []
        for i in range(9):
            btn = tk.Button(
                self.frame_tablero, text="", font=("Arial", 24, "bold"),
                width=5, height=2, bg="#ecf0f1", relief="flat",
                command=lambda i=i: self.click_usuario(i)
            )
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.botones.append(btn)

        self.btn_reset = tk.Button(
            self.root, text="Reiniciar Marcador", command=self.reset_total,
            bg="#e74c3c", fg="white", font=("Arial", 10, "bold")
        )
        self.btn_reset.pack(pady=20)

    def click_usuario(self, i):
        if self.tablero[i] == "" and self.juego_activo:
            self.hacer_movimiento(i, self.usuario)
            if self.juego_activo:
                # La máquina responde tras un breve retraso
                self.root.after(500, self.movimiento_maquina)

    def hacer_movimiento(self, i, jugador):
        self.tablero[i] = jugador
        color = "#3498db" if jugador == "O" else "#e67e22"
        self.botones[i].config(text=jugador, fg=color, state="disabled", disabledforeground=color)

        if self.verificar_ganador(jugador):
            self.finalizar_partida(jugador)
        elif "" not in self.tablero:
            self.finalizar_partida("Empate")

    def movimiento_maquina(self):
        if not self.juego_activo: return
        
        # IA básica: busca ganar, si no, bloquea, si no, al azar
        vacias = [i for i, x in enumerate(self.tablero) if x == ""]
        if vacias:
            eleccion = random.choice(vacias)
            self.hacer_movimiento(eleccion, self.maquina)

    def verificar_ganador(self, j):
        combos = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        return any(self.tablero[a] == self.tablero[b] == self.tablero[c] == j for a,b,c in combos)

    def finalizar_partida(self, resultado):
        self.juego_activo = False
        insultos = [
            "¿Tu cerebro funciona con pilas de botón?",
            "¡Patético! Hasta un error 404 tiene más sentido que tu juego.",
            "Mi algoritmo de limpieza es más inteligente que tú.",
            "¿Te has rendido o es que juegas así de mal siempre?",
            "He visto routers con más visión de juego."
        ]

        if resultado == self.usuario:
            self.victorias += 1
            titulo = "¡Milagro!"
            msg = "Has ganado... Seguramente he tenido un lag cuántico."
        elif resultado == self.maquina:
            self.derrotas += 1
            titulo = "¡HUMILLACIÓN!"
            msg = random.choice(insultos)
        else:
            titulo = "Empate"
            msg = "Un empate. Qué aburrido, como tu forma de jugar."

        self.actualizar_puntos()
        
        # Preguntar si quiere seguir
        respuesta = messagebox.askyesno(titulo, f"{msg}\n\n¿Quieres otra ración de derrota?")
        if respuesta:
            self.reiniciar_tablero()
        else:
            self.root.destroy()

    def actualizar_puntos(self):
        self.label_puntos.config(text=f"Tú (O): {self.victorias} | Máquina (X): {self.derrotas}")

    def reiniciar_tablero(self):
        self.tablero = [""] * 9
        self.juego_activo = True
        for btn in self.botones:
            btn.config(text="", state="normal", bg="#ecf0f1")

    def reset_total(self):
        self.victorias = 0
        self.derrotas = 0
        self.actualizar_puntos()
        self.reiniciar_tablero()

if __name__ == "__main__":
    root = tk.Tk()
    app = TresEnRaya(root)
    root.mainloop()