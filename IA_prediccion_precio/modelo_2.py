# Librerías necesarias
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# EXPANSIÓN DE DATOS - Opción 1 (Interpolación)
tamano_original = np.array([50, 80, 120, 150, 200])
precio_original = np.array([150, 230, 350, 420, 850])

# Generar 15 puntos interpolados
tamano_expandido = np.linspace(50, 200, 15)
precio_expandido = np.interp(tamano_expandido, tamano_original, precio_original)

# Agregar pequeño ruido para hacerlo más realista
np.random.seed(42)
ruido = np.random.normal(0, 10, len(precio_expandido))  # ±10 mil OPA
precio_final = precio_expandido + ruido

# Preparar datos para el modelo
tamano = tamano_expandido.reshape(-1, 1)
precio = precio_final

print(f"Dataset expandido: {len(tamano)} puntos")
print("Tamaños:", tamano.flatten().astype(int))
print("Precios:", precio_final.astype(int))

# Crear y entrenar el modelo
modelo = LinearRegression()
modelo.fit(tamano, precio)

# Coeficientes aprendidos
print(f"\nPendiente: {modelo.coef_[0]:.2f}")
print(f"Intercepto: {modelo.intercept_:.2f}")
print(f"R²: {modelo.score(tamano, precio):.3f}")

# Hacer predicciones
nueva_casa = np.array([[100]])
prediccion = modelo.predict(nueva_casa)
print(f"\nPrecio estimado para 100m²: {prediccion[0]:.0f} miles OPA")

# Visualizar datos y modelo
plt.figure(figsize=(10, 6))

# Puntos originales
plt.scatter(tamano_original, precio_original, color='red', s=80, 
           label='Datos originales', zorder=5)

# Puntos expandidos
plt.scatter(tamano, precio, color='#2150fe', alpha=0.7, 
           label='Datos expandidos')

# Línea de predicción
tamano_rango = np.linspace(40, 220, 100).reshape(-1, 1)
plt.plot(tamano_rango, modelo.predict(tamano_rango), color='#04318f', 
         linewidth=2, label='Modelo entrenado')

plt.xlabel("Tamaño (m²)")
plt.ylabel("Precio (miles OPA)")
plt.legend()
plt.title("Predicción de precio - Dataset Expandido")
plt.grid(True, alpha=0.3)
plt.show()