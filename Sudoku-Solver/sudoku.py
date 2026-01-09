import random
import copy

SUDOKU_BASE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

FIJAS = [(i, j) for i in range(9) for j in range(9) if SUDOKU_BASE[i][j] != 0]

class SudokuSolver:
    def __init__(self):
        self.historial_fitness = []
        
    def crear_individuo(self):
        individuo = copy.deepcopy(SUDOKU_BASE)
        for i in range(9):
            disponibles = [n for n in range(1, 10) if n not in [individuo[i][j] for j in range(9) if individuo[i][j] != 0]]
            random.shuffle(disponibles)
            for j in range(9):
                if individuo[i][j] == 0:
                    individuo[i][j] = disponibles.pop()
        return individuo

    def fitness(self, individuo):
        errores = 0
        for i in range(9):
            fila = individuo[i]
            columna = [individuo[j][i] for j in range(9)]
            errores += 18 - len(set(fila)) - len(set(columna))
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                bloque = [individuo[x][y] for x in range(i, i+3) for y in range(j, j+3)]
                errores += 9 - len(set(bloque))
        return errores

    def seleccion(self, poblacion):
        torneo = random.sample(poblacion, 3)
        return min(torneo, key=self.fitness)

    def cruzar(self, p1, p2):
        hijo = copy.deepcopy(p1)
        punto = random.randint(0, 8)
        hijo[punto] = p2[punto][:]
        return hijo

    def mutar(self, individuo):
        if random.random() < 0.2:
            fila = random.randint(0, 8)
            celdas = [j for j in range(9) if (fila, j) not in FIJAS]
            if len(celdas) >= 2:
                a, b = random.sample(celdas, 2)
                individuo[fila][a], individuo[fila][b] = individuo[fila][b], individuo[fila][a]

    def busqueda_local(self, individuo, intentos=30):
        mejor = copy.deepcopy(individuo)
        mejor_fitness = self.fitness(mejor)
        
        for _ in range(intentos):
            candidato = copy.deepcopy(mejor)
            fila = random.randint(0, 8)
            celdas = [j for j in range(9) if (fila, j) not in FIJAS]
            if len(celdas) >= 2:
                a, b = random.sample(celdas, 2)
                candidato[fila][a], candidato[fila][b] = candidato[fila][b], candidato[fila][a]
                nuevo_fitness = self.fitness(candidato)
                if nuevo_fitness < mejor_fitness:
                    mejor, mejor_fitness = candidato, nuevo_fitness
        return mejor

    def resolver(self):
        poblacion = [self.crear_individuo() for _ in range(200)]
        
        for generacion in range(1000):
            poblacion.sort(key=self.fitness)
            mejor = poblacion[0]
            mejor_fit = self.fitness(mejor)
            self.historial_fitness.append(mejor_fit)
            
            if mejor_fit == 0:
                print(f"Solución encontrada en generación {generacion}")
                return mejor
            
            # Elitismo
            nueva = poblacion[:10]
            
            while len(nueva) < 200:
                p1 = self.seleccion(poblacion)
                p2 = self.seleccion(poblacion)
                hijo = self.cruzar(p1, p2)
                self.mutar(hijo)
                hijo = self.busqueda_local(hijo)
                nueva.append(hijo)
            
            poblacion = nueva
            
            if generacion % 100 == 0:
                print(f"Gen {generacion}: Fitness {mejor_fit}")
        
        print("No se encontró solución perfecta")
        return poblacion[0]

    def mostrar_sudoku(self, sudoku):
        print("\n" + "="*31)
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("-"*31)
            fila = []
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    fila.append("|")
                fila.append(str(sudoku[i][j]))
            print(" ".join(fila))
        print("="*31)

# Ejecutar
print("Resolviendo Sudoku con Algoritmos Genéticos Híbridos...")
solver = SudokuSolver()
solucion = solver.resolver()

print("\nSUDOKU ORIGINAL:")
solver.mostrar_sudoku(SUDOKU_BASE)

print("\nSOLUCIÓN ENCONTRADA:")
solver.mostrar_sudoku(solucion)
print(f"Fitness final: {solver.fitness(solucion)}")
