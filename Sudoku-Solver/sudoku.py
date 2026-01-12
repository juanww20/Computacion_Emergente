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

# Posiciones fijas que no se pueden modificar
FIJAS = [(i, j) for i in range(9) for j in range(9) if SUDOKU_BASE[i][j] != 0]

class SudokuSolver:
    def __init__(self, poblacion_size=200, max_generaciones=1000, 
                 elitismo_count=10, mutation_rate=0.2, intentos_busqueda=30):
        self.historial_fitness = []
        self.poblacion_size = poblacion_size
        self.max_generaciones = max_generaciones
        self.elitismo_count = elitismo_count
        self.mutation_rate = mutation_rate
        self.intentos_busqueda = intentos_busqueda
        
    # Crea una solución candidata respetando números fijos
    def crear_individuo(self):
        
        individuo = copy.deepcopy(SUDOKU_BASE)
        for i in range(9):
            disponibles = [n for n in range(1, 10) 
                         if n not in [individuo[i][j] for j in range(9) 
                                    if individuo[i][j] != 0]]
            random.shuffle(disponibles)
            for j in range(9):
                if individuo[i][j] == 0:
                    individuo[i][j] = disponibles.pop()
        return individuo

    # Calcula la calidad de una solución (0 = perfecta)
    def fitness(self, individuo):
        
        errores = 0
        # Verificar filas y columnas
        for i in range(9):
            fila = individuo[i]
            columna = [individuo[j][i] for j in range(9)]
            errores += 18 - len(set(fila)) - len(set(columna))

        # Verificar bloques 3x3
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                bloque = [individuo[x][y] for x in range(i, i+3) 
                         for y in range(j, j+3)]
                errores += 9 - len(set(bloque))

        return errores

    # Selección por torneo de 3 individuos
    def seleccion(self, poblacion):
        torneo = random.sample(poblacion, 3)
        return min(torneo, key=self.fitness)

    # Cruce de un punto (intercambia una fila completa)
    def cruzar(self, p1, p2):
        hijo = copy.deepcopy(p1)
        punto = random.randint(0, 8)
        hijo[punto] = p2[punto][:]
        return hijo

    # Mutación por intercambio de dos celdas no fijas en una fila
    def mutar(self, individuo):
        if random.random() < self.mutation_rate:
            fila = random.randint(0, 8)
            celdas = [j for j in range(9) if (fila, j) not in FIJAS]
            if len(celdas) >= 2:
                a, b = random.sample(celdas, 2)
                individuo[fila][a], individuo[fila][b] = individuo[fila][b], individuo[fila][a]

    # Optimización local mediante intercambios aleatorios
    def busqueda_local(self, individuo):
        mejor = copy.deepcopy(individuo)
        mejor_fitness = self.fitness(mejor)
        
        for _ in range(self.intentos_busqueda):
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

    # Algoritmo genético híbrido para resolver Sudoku
    def resolver(self):
        # Generar población inicial
        poblacion = [self.crear_individuo() for _ in range(self.poblacion_size)]
        
        # Ciclo evolutivo
        for generacion in range(self.max_generaciones):
            # Ordenar por fitness (menor es mejor)
            poblacion.sort(key=self.fitness)
            mejor = poblacion[0]
            mejor_fit = self.fitness(mejor)
            self.historial_fitness.append(mejor_fit)
            
            # Verificar solución perfecta
            if mejor_fit == 0:
                print(f"Solución encontrada en generación {generacion}")
                return mejor
            
            # Aplicar elitismo
            nueva = poblacion[:self.elitismo_count]
            
            # Generar nueva población
            while len(nueva) < self.poblacion_size:
                p1 = self.seleccion(poblacion)
                p2 = self.seleccion(poblacion)
                hijo = self.cruzar(p1, p2)
                self.mutar(hijo)
                hijo = self.busqueda_local(hijo)
                nueva.append(hijo)
            
            poblacion = nueva
            
            # Mostrar progreso
            if generacion % 100 == 0:
                print(f"Gen {generacion:4d}: Fitness {mejor_fit}")
        
        print(f"Mejor solución aproximada (fitness: {self.fitness(poblacion[0])})")
        return poblacion[0]

    # Muestra el tablero de Sudoku formateado
    def mostrar_sudoku(self, sudoku):
        print("\n" + "="*31)
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("-"*31)
            fila = []
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    fila.append("|")
                fila.append(str(sudoku[i][j]) if sudoku[i][j] != 0 else ".")
            print(" ".join(fila))
        print("="*31)

# Configuración y ejecución
print("="*50)
print("Resolviendo Sudoku con Algoritmos Genéticos Híbridos")
print("="*50)

# Crear solver y ejecutar
solver = SudokuSolver() # Usar parámetros por defecto
solucion = solver.resolver()

# Mostrar resultados
print("\n" + "="*50 + "\n")
print("SUDOKU ORIGINAL:")
solver.mostrar_sudoku(SUDOKU_BASE)

print("\nSOLUCIÓN ENCONTRADA:")
solver.mostrar_sudoku(solucion)

fitness_final = solver.fitness(solucion)
if fitness_final == 0:
    print(f"Fitness final: {fitness_final} (SOLUCIÓN PERFECTA)")
else:
    print(f"Fitness final: {fitness_final} (SOLUCIÓN APROXIMADA)")