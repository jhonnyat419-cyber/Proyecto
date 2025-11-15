import random
import numpy as np
import os
import time

# =============================
# Clase del Entorno / Tablero
# =============================
class Ambiente:
    def __init__(self, filas, columnas, prob_hojas=0.5):
        self.filas = filas
        self.columnas = columnas
        self.tablero = np.zeros((filas, columnas), dtype=int)
        for i in range(filas):
            for j in range(columnas):
                if random.random() < prob_hojas:
                    self.tablero[i][j] = 1  # 1 = hoja

    def hay_hojas(self):
        return np.sum(self.tablero) > 0

    def mostrar(self, fila_robot, columna_robot):
        os.system("cls" if os.name == "nt" else "clear")
        for i in range(self.filas):
            fila_str = ""
            for j in range(self.columnas):
                if i == fila_robot and j == columna_robot:
                    fila_str += "🤖 "  # posición del robot
                elif self.tablero[i][j] == 1:
                    fila_str += "🍃 "   # hoja
                else:
                    fila_str += ". "   # limpio
            print(fila_str)
        print()


# =============================
# Clase del Agente con Estado
# =============================
class RobotAspiradoraConEstado:
    MOVIMIENTOS = {
        0: (-1, 0),  # norte
        1: (0, 1),   # este
        2: (1, 0),   # sur
        3: (0, -1)   # oeste
    }

    def __init__(self, ambiente, energia_inicial, fila, columna):
        self.ambiente = ambiente
        self.energia = energia_inicial
        self.fila = fila
        self.columna = columna
        self.direccion = 0
        self.hojas_recogidas = 0
        self.visitadas = set()
        self.objetivo = None

    # -------------------------
    # Acciones
    # -------------------------
    def avanzar(self):
        if self.energia <= 0:
            return False
        delta_fila, delta_columna = RobotAspiradoraConEstado.MOVIMIENTOS[self.direccion]
        nueva_fila = self.fila + delta_fila
        nueva_columna = self.columna + delta_columna
        if 0 <= nueva_fila < self.ambiente.filas and 0 <= nueva_columna < self.ambiente.columnas:
            self.fila = nueva_fila
            self.columna = nueva_columna
        self.energia -= 1
        self.visitadas.add((self.fila, self.columna))
        return True

    def girar(self, grados):
        if self.energia <= 0:
            return False
        giros = grados // 90
        self.direccion = (self.direccion + giros) % 4
        self.energia -= 1
        return True

    def aspirar(self):
        if self.energia <= 0:
            return False
        if self.ambiente.tablero[self.fila][self.columna] == 1:
            self.ambiente.tablero[self.fila][self.columna] = 0
            self.hojas_recogidas += 1
        self.energia -= 1
        return True

    # -------------------------
    # Percepciones
    # -------------------------
    def percibir_actual(self):
        return self.ambiente.tablero[self.fila][self.columna] == 1

    def percibir_vecinos(self):
        if self.energia <= 0:
            return []
        self.energia -= 1  # usar sensor cuesta energía
        vecinos = []
        for dir, (df, dc) in RobotAspiradoraConEstado.MOVIMIENTOS.items():
            nf, nc = self.fila + df, self.columna + dc
            if 0 <= nf < self.ambiente.filas and 0 <= nc < self.ambiente.columnas:
                if self.ambiente.tablero[nf][nc] == 1:
                    vecinos.append((nf, nc))
        return vecinos

    # -------------------------
    # Estrategia con estado
    # -------------------------
    def decidir(self):
        if self.energia <= 0:
            return False

        # Aspirar si hay hoja
        if self.percibir_actual():
            self.aspirar()
            self.objetivo = None
            return True

        # Si tengo un objetivo previo
        if self.objetivo and (self.objetivo != (self.fila, self.columna)):
            nf, nc = self.objetivo
            if nf < self.fila:
                self.direccion = 0
            elif nf > self.fila:
                self.direccion = 2
            elif nc > self.columna:
                self.direccion = 1
            elif nc < self.columna:
                self.direccion = 3
            self.avanzar()
            return True

        # Detectar hojas vecinas
        hojas_cercanas = self.percibir_vecinos()
        if hojas_cercanas:
            self.objetivo = hojas_cercanas[0]
            return True

        # Explorar celda no visitada
        movs = list(RobotAspiradoraConEstado.MOVIMIENTOS.values())
        random.shuffle(movs)
        for df, dc in movs:
            nf, nc = self.fila + df, self.columna + dc
            if (0 <= nf < self.ambiente.filas and 0 <= nc < self.ambiente.columnas
                and (nf, nc) not in self.visitadas):
                for dir, (dff, dcc) in RobotAspiradoraConEstado.MOVIMIENTOS.items():
                    if (df, dc) == (dff, dcc):
                        self.direccion = dir
                        break
                self.avanzar()
                return True

        # Si todo visitado, moverse al azar
        df, dc = random.choice(list(RobotAspiradoraConEstado.MOVIMIENTOS.values()))
        for dir, (dff, dcc) in RobotAspiradoraConEstado.MOVIMIENTOS.items():
            if (df, dc) == (dff, dcc):
                self.direccion = dir
                break
        self.avanzar()
        return True


# =============================
# Simulación visual
# =============================
def ejecutar_simulacion_visual(filas, columnas, energia_inicial):
    ambiente = Ambiente(filas, columnas)
    robot = RobotAspiradoraConEstado(ambiente, energia_inicial, 0, 0)

    energia_inicial_total = robot.energia
    hojas_totales = np.sum(ambiente.tablero)

    while robot.energia > 0 and ambiente.hay_hojas():
        ambiente.mostrar(robot.fila, robot.columna)
        print(f"Energía restante: {robot.energia}")
        print(f"Hojas recogidas: {robot.hojas_recogidas}")
        robot.decidir()
        time.sleep(0.15)  # retardo visual

    energia_usada = energia_inicial_total - robot.energia
    hojas_recogidas = robot.hojas_recogidas

    ambiente.mostrar(robot.fila, robot.columna)
    print("🧹 Limpieza completada")
    print(f"Energía usada: {energia_usada}")
    print(f"Hojas recogidas: {hojas_recogidas} / {hojas_totales}")
    print()


# =============================
# Múltiples simulaciones (sin visual)
# =============================
def ejecutar_simulaciones(repeticiones=50, filas=6, columnas=6, energia_inicial=100):
    energia_total = 0
    hojas_total = 0
    hojas_totales_ambiente = 0

    for _ in range(repeticiones):
        ambiente = Ambiente(filas, columnas)
        robot = RobotAspiradoraConEstado(ambiente, energia_inicial, 0, 0)
        energia_inicial_total = robot.energia
        hojas_totales = np.sum(ambiente.tablero)

        while robot.energia > 0 and ambiente.hay_hojas():
            robot.decidir()

        energia_usada = energia_inicial_total - robot.energia
        energia_total += energia_usada
        hojas_total += robot.hojas_recogidas
        hojas_totales_ambiente += hojas_totales

    print("\n==============================")
    print(f"Simulaciones ejecutadas: {repeticiones}")
    print(f"Energía promedio usada: {energia_total / repeticiones:.2f}")
    print(f"Hojas promedio recogidas: {hojas_total / repeticiones:.2f}")
    print(f"Promedio de hojas totales por ambiente: {hojas_totales_ambiente / repeticiones:.2f}")
    print("==============================\n")


# =============================
# MAIN
# =============================
if __name__ == "__main__":
    # 1️⃣ Visualizar una ejecución paso a paso
    ejecutar_simulacion_visual(filas=6, columnas=6, energia_inicial=100)

    # 2️⃣ Ejecutar 50 simulaciones automáticas para promediar
    ejecutar_simulaciones()