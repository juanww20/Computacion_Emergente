# app.py

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from flask import Flask, request, render_template, jsonify

# --- 1. CONFIGURACIÓN INICIAL Y CARGA DEL MODELO ---
# (Esta parte se mantiene igual)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
app = Flask(__name__)
characters = [x for x in "abcdefghijklmnopqrstuvwxyz'?! "]
char_to_num = keras.layers.StringLookup(vocabulary=characters, oov_token="")
num_to_char = keras.layers.StringLookup(
    vocabulary=char_to_num.get_vocabulary(), oov_token="", invert=True
)
frame_length = 256
frame_step = 160
fft_length = 384
def CTCLoss(y_true, y_pred):
    batch_len = tf.cast(tf.shape(y_true)[0], dtype="int64")
    input_length = tf.cast(tf.shape(y_pred)[1], dtype="int64")
    label_length = tf.cast(tf.shape(y_true)[1], dtype="int64")
    input_length = input_length * tf.ones(shape=(batch_len, 1), dtype="int64")
    label_length = label_length * tf.ones(shape=(batch_len, 1), dtype="int64")
    loss = keras.backend.ctc_batch_cost(y_true, y_pred, input_length, label_length)
    return loss
try:
    model = keras.models.load_model(
        "mi_modelo_asr.keras", custom_objects={"CTCLoss": CTCLoss} #Advertencia: debe verificar que si esta el archivo de modelo Keras, si no al contrario te dice un error
    )
    print(">>> Modelo cargado exitosamente.")
except Exception as e:
    print(f">>> Error al cargar el modelo: {e}")
    model = None

# --- 2. FUNCIONES DE PRE-PROCESAMIENTO Y DECODIFICACIÓN ---

# Ya no necesitamos librosa aquí.
def preprocess_audio(audio_array):
    """
    Función para pre-procesar el array de audio crudo.
    """
    audio = tf.convert_to_tensor(audio_array, dtype=tf.float32)
    
    # El resto del pre-procesamiento es idéntico al original
    spectrogram = tf.signal.stft(
        audio, frame_length=frame_length, frame_step=frame_step, fft_length=fft_length
    )
    spectrogram = tf.abs(spectrogram)
    spectrogram = tf.math.pow(spectrogram, 0.5)
    means = tf.math.reduce_mean(spectrogram, 1, keepdims=True)
    stddevs = tf.math.reduce_std(spectrogram, 1, keepdims=True)
    spectrogram = (spectrogram - means) / (stddevs + 1e-10)
    return spectrogram

def decode_prediction(pred):
    # Esta función no necesita cambios
    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0]
    output_text = []
    for result in results:
        result = tf.strings.reduce_join(num_to_char(result)).numpy().decode("utf-8")
        output_text.append(result)
    return output_text

# --- 3. RUTAS DE LA API FLASK ---

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Recibe un JSON con el array de audio pre-procesado
    desde el navegador.
    """
    if model is None:
        return jsonify({"error": "El modelo no se ha cargado correctamente."}), 500
    
    # Obtenemos los datos JSON del cuerpo de la solicitud
    data = request.get_json()
    if 'audio_data' not in data:
        return jsonify({"error": "No se encontraron datos de audio."}), 400

    # Los datos ya son una lista de números (floats)
    audio_array = np.array(data['audio_data'], dtype=np.float32)
    
    try:
        # 1. Procesar el array de audio para obtener el espectrograma
        spectrogram = preprocess_audio(audio_array)
        
        # 2. Añadir la dimensión del "batch" que el modelo espera
        spectrogram = tf.expand_dims(spectrogram, axis=0)

        # 3. Realizar la predicción
        prediction = model.predict(spectrogram)
        
        # 4. Decodificar el resultado a texto
        decoded_text = decode_prediction(prediction)
        
        return jsonify({"transcription": decoded_text[0]})

    except Exception as e:
        print(f"Error durante la predicción: {e}")
        return jsonify({"error": "Ocurrió un error al procesar el audio."}), 500

# --- 4. INICIAR LA APLICACIÓN ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)