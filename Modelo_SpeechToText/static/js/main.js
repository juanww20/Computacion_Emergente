// static/js/main.js

document.addEventListener('DOMContentLoaded', () => {

    const TARGET_SAMPLE_RATE = 22050; // La tasa de muestreo de tu modelo (LJSpeech)

    // --- NUEVA FUNCIÓN DE PROCESAMIENTO DE AUDIO EN EL NAVEGADOR ---
    async function processAudio(audioBlob) {
        // Usamos AudioContext para decodificar y remuestrear
        const audioContext = new (window.AudioContext || window.webkitAudioContext)({
            sampleRate: TARGET_SAMPLE_RATE // Le pedimos que trabaje a nuestra tasa objetivo
        });

        // Convertimos el Blob (o File) a un ArrayBuffer
        const arrayBuffer = await audioBlob.arrayBuffer();

        // Decodificamos el audio a un AudioBuffer
        const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

        // Si el audio no está ya a la tasa objetivo, lo remuestreamos.
        // El OfflineAudioContext es la forma más fácil y de mayor calidad para hacerlo.
        if (audioBuffer.sampleRate !== TARGET_SAMPLE_RATE) {
            console.log(`Remuestreando de ${audioBuffer.sampleRate} Hz a ${TARGET_SAMPLE_RATE} Hz`);
            const offlineContext = new OfflineAudioContext(
                audioBuffer.numberOfChannels,
                audioBuffer.duration * TARGET_SAMPLE_RATE,
                TARGET_SAMPLE_RATE
            );
            const source = offlineContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(offlineContext.destination);
            source.start();
            const resampledBuffer = await offlineContext.startRendering();
            return resampledBuffer.getChannelData(0); // Devolvemos el audio mono
        }

        // Si ya estaba en la tasa correcta, simplemente lo devolvemos
        return audioBuffer.getChannelData(0); // Devolvemos el audio mono
    }

    // --- FUNCIÓN GENÉRICA PARA ENVIAR EL AUDIO AL SERVIDOR ---
    async function sendAudioToServer(audioFloatArray, statusElement, resultElement) {
        statusElement.textContent = 'Analizando... ⏳';
        resultElement.textContent = '';
        
        try {
            // Enviamos los datos como JSON
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                // Convertimos el array de floats a una lista de Python
                body: JSON.stringify({ audio_data: Array.from(audioFloatArray) })
            });

            if (!response.ok) {
                throw new Error(`Error del servidor: ${response.statusText}`);
            }

            const data = await response.json();
            
            if (data.error) {
                resultElement.textContent = `Error: ${data.error}`;
            } else {
                resultElement.textContent = data.transcription || 'No se pudo transcribir.';
            }
            statusElement.textContent = 'Análisis completo. ✅';

        } catch (error) {
            console.error('Error al enviar el audio:', error);
            statusElement.textContent = `Error: ${error.message}`;
        }
    }


    // --- LÓGICA PARA SUBIR ARCHIVOS ---
    const audioFileInput = document.getElementById('audioFile');
    const uploadButton = document.getElementById('uploadButton');
    const fileStatus = document.getElementById('fileStatus');
    const fileResult = document.getElementById('fileResult');

    uploadButton.addEventListener('click', async () => {
        const file = audioFileInput.files[0];
        if (!file) {
            fileStatus.textContent = 'Por favor, selecciona un archivo primero.';
            return;
        }
        
        try {
            fileStatus.textContent = 'Procesando audio en el navegador...';
            const audioData = await processAudio(file);
            await sendAudioToServer(audioData, fileStatus, fileResult);
        } catch (error) {
            fileStatus.textContent = `Error al procesar el archivo: ${error.message}`;
        }
    });

    // --- LÓGICA PARA GRABACIÓN EN VIVO ---
    const startButton = document.getElementById('startButton');
    const stopButton = document.getElementById('stopButton');
    const liveStatus = document.getElementById('liveStatus');
    const liveResult = document.getElementById('liveResult');

    let mediaRecorder;
    let audioChunks = [];

    startButton.addEventListener('click', async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/webm' }); // El formato nativo suele ser webm u ogg
                audioChunks = [];

                try {
                    liveStatus.textContent = 'Procesando audio en el navegador...';
                    const audioData = await processAudio(audioBlob);
                    await sendAudioToServer(audioData, liveStatus, liveResult);
                } catch (error) {
                    liveStatus.textContent = `Error al procesar la grabación: ${error.message}`;
                }
            };

            mediaRecorder.start();
            startButton.disabled = true;
            stopButton.disabled = false;
            liveStatus.textContent = 'Grabando... 🔴';
            liveResult.textContent = '';

        } catch (error) {
            console.error('Error al acceder al micrófono:', error);
            liveStatus.textContent = 'Error: No se pudo acceder al micrófono.';
        }
    });

    stopButton.addEventListener('click', () => {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
        }
        startButton.disabled = false;
        stopButton.disabled = true;
        liveStatus.textContent = 'Grabación detenida. Procesando...';
    });
});