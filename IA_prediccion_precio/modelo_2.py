# Librerias necesarias
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

#Tamaño de casas (m**2)
tamano = np.array([50,80,120,150,200]).reshape(-1,1)

#Precios (Unidad: Mil de dinero OPA)
precio = np.array([150,230,350,420,850])

#Crear y entrenar el modelo
modelo = LinearRegression()
modelo.fit(tamano,precio)

#Coeficientes aprendidos
print(f"Pendiente: {modelo.coef_[0]:.2f}")
print(f"Intercepto: {modelo.intercept_:.2f}")

#Hacer predicciones
nueva_casa = np.array([[100]])
prediccion = modelo.predict(nueva_casa)
print(f"Precio estimado: {prediccion[0]:.0f} OPA")

#Visualizar datos y modelo
plt.scatter(tamano, precio, color="#2150fe", label="Datos reales")

#LInea de prediccion
plt.plot(tamano, modelo.predict(tamano), color="#04318f", linewidth=2, label="Modelo entrenado")

plt.xlabel("Tamaño (m**2)")
plt.ylabel("Precio (miles OPA)")
plt.legend()
plt.title("Prediccion de precio")
plt.show()