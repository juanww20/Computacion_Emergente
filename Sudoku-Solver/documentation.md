# 🧬 Resolución de Sudoku con Algoritmo Genético

## 📋 Descripción
Sistema de resolución de Sudoku que utiliza **Algoritmos Genéticos Híbridos** para encontrar soluciones válidas, combinando evolución genética con búsqueda local.

## 🚀 Ejecución
1. **Ejecutar programa:** `python sudoku_solver.py`
2. **Ver resultados:** Sudoku resuelto y gráficos de evolución

## 🏗️ Componentes del Modelo

### Representación del Individuo
- Tablero 9x9 que respeta números fijos iniciales
- Cada fila contiene números 1-9 sin repetición en la generación inicial

### Función de Fitness
```python
# Calcula errores en:
# - Filas (9 - elementos únicos por fila)
# - Columnas (9 - elementos únicos por columna)  
# - Subcuadrículas 3x3 (9 - elementos únicos por bloque)
# Fitness 0 = solución perfecta
```

### Operadores Genéticos
- **Selección por Torneo**: Elige el mejor de 3 individuos aleatorios
- **Cruce de Un Punto**: Intercambia una fila completa entre padres
- **Mutación por Intercambio**: Intercambia dos celdas no fijas en misma fila
- **Elitismo**: Conserva los 10 mejores individuos cada generación
- **Búsqueda Local**: Optimización local con intercambios en misma fila

## 📊 Proceso Evolutivo
1. **Inicialización**: Crear población de 200 individuos
2. **Evaluación**: Calcular fitness de cada individuo
3. **Condición de Término**: Si fitness=0 → solución encontrada
4. **Selección**: Seleccionar padres por torneo
5. **Reproducción**: Cruce → Mutación → Búsqueda Local
6. **Reemplazo**: Nueva generación (elitismo + nuevos hijos)
7. **Repetición**: Volver al paso 2 hasta solución o 1000 generaciones

## ⚙️ Parámetros Configurables
- `poblacion_size`: 200 (tamaño de población)
- `max_generaciones`: 1000 (límite de generaciones)
- `elitismo_count`: 10 (individuos conservados)
- `mutation_rate`: 0.2 (probabilidad de mutación)
- `intentos_busqueda`: 30 (optimizaciones locales por individuo)

## 📊 Diagrama del Proceso
```
GENERACIÓN N
Población → Evaluación → Selección → Cruce → Mutación → Búsqueda Local
     ↑                                      ↓
     └────── Elitismo ← Nueva Población ←──┘
```

El algoritmo combina exploración global (operadores genéticos) con explotación local (búsqueda local) para converger más rápido a soluciones válidas.