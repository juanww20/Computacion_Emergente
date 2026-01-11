# 🖥️ Computación Emergente - Explorando la Inteligencia Artificial ( •̀ ω •́ )✧

Bienvenido al repositorio de **Computación Emergente**, una materia dedicada a explorar las fronteras de la inteligencia artificial y sus aplicaciones innovadoras. El objetivo principal de esta materia es comprender y desarrollar sistemas inteligentes que simulen capacidades cognitivas humanas, utilizando algoritmos emergentes y técnicas avanzadas de machine learning.  
  
## 📁 Programas del Repositorio

Este repositorio contiene los siguientes proyectos implementados:

### 1. **Chatbot OwO**
   - Implementación Google Gemini API
   - Sencillo system_instruction

### 2. **ChatbotRegla**
   - Un ejemplo de que funciona como un chatbot basado en reglas
   - La pagina apoya Dark-Mode

### 3. **Modelo_SpeechToText**
   - Usando el proyecto Automatic Speech Recognition using CTC
   - Modificando que permite la continuacion de entrenar el modelo mismo
   - Usando Flask para ejecutar el modelo entrenado
   - Debe utilizar las librerias indicadas desde la carpeta **Modelo_SpeechToText** en *requirements.txt*

### 4. **IA_prediccion_precio**
   - Ejemplo para modelo de regresión lineal para predecir el precio de viviendas basándose en su tamaño (m²), utilizando un dataset expandido mediante interpolación
   - Técnica ML: Regresión Lineal Simple
   - Preprocesamiento: expansión de dataset vía interpolación + ruido
   - Visualización: gráfico completo con datos y modelo

### 5. **Labubu-vs-Lafufu**
   - Clasificador de imágenes usando deep learning con Torch que distingue entre dos personajes populares: Labubu y Lafufu
   - Utiliza una red neuronal convolucional (CNN) entrenada desde cero, incluye una interfaz web interactiva con Gradio
   - Puede probar con sus propias imágenes usando la función *predict_image()*
   
### 6. **model_csv**
   - Ejemplo para Proyecto de clasificación
   - Sistema de clasificación de machine learning para predecir el nivel de consumo de alcohol en estudiantes de secundaria
   - Utiliza datos demográficos, académicos y sociales para entrenar un modelo de Random Forest que identifica patrones de riesgo, con aplicaciones potenciales en intervenciones educativas y políticas de salud escolar

## 🛠️ Librerías Utilizadas

Los proyectos utilizan las siguientes librerías de Python está en   
**`requirements.txt`** 📖  
  
## 🚀 Instalación y Ejecución

Sigue estos pasos para configurar el entorno y ejecutar los programas (Debe tener versión de Python mayor que 3.9, en el repositorio presente usa **Python 3.12.3**):

### Prerrequisitos
```bash
# Clonar el repositorio
git clone https://github.com/juanww20/Computacion_Emergente

# Crear entorno virtual (recomendado)
python -m venv nombre_de_carpeta_entorno_virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# Luego, crea el descarga la libreria que tiene en requirements.txt tras de activar el entorno virtual, 
# OJO debe estar ubicado en el mismo de raiz de carpeta para descargar bien la librería
pip install -r requirements.txt 
# Luego, ¡happy ejecutar los programas!
```
  
### ¡Frase Animo!  
#### 💫 La programación no es solo código, es el arte de dar vida a ideas abstractas. ¡Que tus algoritmos siempre converjan hacia soluciones elegantes!