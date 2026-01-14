import random
import copy

MATERIAS = [
    "Sistemas de Base de Datos", 
    "Control e Instrumentación", 
    "Sistemas de Programas", 
    "Organización del Computador", 
    "Estructuras de Discretas II", 
    "Comunicación de Datos"
]
PROFESORES = ["Prof. Francisco", "Prof. Alexander", "Prof. Rosa", "Prof. Susan"]
AULAS = ["Aula 4404", "Aula 4P52", "Aula 4440", "Aula 4423", "Aula 4438", "Aula 4349"]
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

HORA_INICIO_MIN = 17
HORA_INICIO_MAX = 19 

# Formatea la hora de 24h a 12h con AM/PM
def formatear_hora(hora_24):
    if hora_24 < 12:
        momento = "AM"
    else:
        momento = "PM"
    
    if hora_24 <= 12:
        hora_12 = hora_24
    else:
        hora_12 = hora_24 - 12
        
    return f"{hora_12:02d}:00 {momento}"

# Se crea un horario al azar
def crear_individuo():
    horario = []
    for materia in MATERIAS:
        clase = {
            "materia": materia,
            "profesor": random.choice(PROFESORES),
            "aula": random.choice(AULAS),
            "dia": random.choice(DIAS),
            "inicio": random.randint(HORA_INICIO_MIN, HORA_INICIO_MAX),
            "duracion": 2 
        }
        horario.append(clase)
    return horario

# Calcula el fitness de un individuo (menor es mejor)
def fitness(individuo):
    errores = 0
    
    for i in range(len(individuo)):
        for j in range(i + 1, len(individuo)):
            c1 = individuo[i]
            c2 = individuo[j]
            
            if c1["dia"] == c2["dia"]:
                inicio1 = c1["inicio"]
                fin1 = c1["inicio"] + c1["duracion"]
                inicio2 = c2["inicio"]
                fin2 = c2["inicio"] + c2["duracion"]
                
                # REGLA: ¿Se chocan las clases?
                if inicio1 < fin2 and inicio2 < fin1:
                    
                    # Error 1: No pueden haber dos clases a la vez para el alumno
                    errores = errores + 1
                    
                    # Error 2: Misma aula a la misma hora
                    if c1["aula"] == c2["aula"]:
                        errores = errores + 1
                    else:
                        pass # No hacemos nada si esta bien
                    
                    # Error 3: Mismo profesor a la misma hora
                    if c1["profesor"] == c2["profesor"]:
                        errores = errores + 1
                    else:
                        pass
    
    # Regla extra: penalizar si hay clases el viernes
    for clase in individuo:
        if clase["dia"] == "Viernes":
            errores = errores + 0.1
            
    return round(errores, 1)

# Se elige al mejor de 3
def seleccion(poblacion):
    torneo = random.sample(poblacion, 3)
    torneo.sort(key=lambda x: fitness(x))
    
    return torneo[0]

# Se cruzan dos padres
def cruzar(padre1, padre2):
    # Cortamos a la mitad
    punto = len(padre1) // 2
    hijo = padre1[:punto] + padre2[punto:]
    
    return copy.deepcopy(hijo)

# Mutamos un individuo al azar
def mutar(individuo, prob=0.2):
    if random.random() < prob:
        clase = random.choice(individuo)
        que_cambiar = random.randint(0, 3)
        
        if que_cambiar == 0:
            clase["aula"] = random.choice(AULAS)
        elif que_cambiar == 1:
            clase["profesor"] = random.choice(PROFESORES)
        elif que_cambiar == 2:
            clase["dia"] = random.choice(DIAS)
        else:
            clase["inicio"] = random.randint(HORA_INICIO_MIN, HORA_INICIO_MAX)

# Columna del algoritmo genético
def algoritmo_genetico():
    # Creamos 250 horarios al azar para empezar
    poblacion = []
    for _ in range(250):
        poblacion.append(crear_individuo())
    
    for generacion in range(1000):
        # Ordenamos del mejor al peor
        poblacion.sort(key=lambda x: fitness(x))
        
        mejor = poblacion[0]
        valor_fit = fitness(mejor)
        
        # Si ya no hay errores graves, terminamos (that's what she said)
        if valor_fit <= 0.5:
            print(f"Gen {generacion} - Solucion encontrada!")
            return mejor
            
        # Nos quedamos con los 20 mejores 
        nueva_poblacion = poblacion[:20]
        
        # Hacemos hijos hasta completar 250
        while len(nueva_poblacion) < 250:
            p1 = seleccion(poblacion)
            p2 = seleccion(poblacion)
            
            hijo = cruzar(p1, p2)
            mutar(hijo)
            
            nueva_poblacion.append(hijo)
            
        poblacion = nueva_poblacion
        
    return poblacion[0]

def mostrar_resultado(horario):
    # Se ordena por día y hora
    horario.sort(key=lambda x: (DIAS.index(x['dia']), x['inicio']))
    
    print("\n--- HORARIO OPTIMIZADO ---")
    print(f"{'DÍA':<10} | {'HORA':<20} | {'MATERIA':<28} | {'PROFESOR':<15} | {'AULA'}")
    print("-" * 100)
    
    for c in horario:
        hora_i = formatear_hora(c['inicio'])
        hora_f = formatear_hora(c['inicio'] + c['duracion'])
        rango = f"{hora_i} - {hora_f}"
        
        print(f"{c['dia']:<10} | {rango:<20} | {c['materia']:<28} | {c['profesor']:<15} | {c['aula']}")

# Ejecución
resultado_final = algoritmo_genetico()
mostrar_resultado(resultado_final)

conflicto_final = fitness(resultado_final)
print(f"\nConflictos finales: {conflicto_final}")