VERSION 1:
<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8" /><title>Kokoro TTS Demo</title></head>
<body>
  <h2>Kokoro TTS Prueba</h2>
  <textarea id="texto" rows="4" cols="50">Hola, esta es una prueba con Kokoro TTS.</textarea><br>
  <button onclick="hablar()">Hablar</button>
  <audio id="audio" controls></audio>

  <script>
    async function hablar() {
      const texto = document.getElementById("texto").value;
      const response = await fetch('http://localhost:8880/v1/audio/speech', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: "kokoro",
          voice: "af_sky+af_bella",
          input: texto
        })
      });

      if (!response.ok) {
        alert("Error: " + response.status);
        return;
      }

      const blob = await response.blob();
      const audio = document.getElementById("audio");
      audio.src = URL.createObjectURL(blob);
      audio.play();
    }
  </script>
</body>
</html>















<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>Grabar y Reproducir con Kokoro TTS</title>
</head>
<body>
  <h2>Graba tu voz y escucha la transcripción con voz Kokoro TTS</h2>

  <button id="btnGrabar">Grabar</button><br><br>
  <p><b>Texto reconocido:</b> <span id="textoReconocido"></span></p>
  <audio id="audio" controls></audio>

  <script>
    const btn = document.getElementById("btnGrabar");
    const textoSpan = document.getElementById("textoReconocido");
    const audio = document.getElementById("audio");

    let recorder;
    let chunks = [];

    // Usaremos la API de Web Speech para reconocimiento
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Tu navegador no soporta Speech Recognition");
    }
    const recognition = new SpeechRecognition();
    recognition.lang = "es-ES";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    btn.onclick = () => {
      textoSpan.textContent = "";
      recognition.start();
      btn.disabled = true;
      btn.textContent = "Grabando...";
    };

    recognition.onresult = async (event) => {
      const texto = event.results[0][0].transcript;
      textoSpan.textContent = texto;
      btn.textContent = "Grabado ✔";

      // Enviar a Kokoro TTS para reproducir
      const resp = await fetch('http://localhost:8880/v1/audio/speech', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: "kokoro",
          voice: "af_heart",
          input: texto
        })
      });

      if (resp.ok) {
        const blob = await resp.blob();
        audio.src = URL.createObjectURL(blob);
        audio.play();
      } else {
        alert("Error en TTS: " + resp.status);
      }

      btn.disabled = false;
      btn.textContent = "Grabar";
    };

    recognition.onerror = (e) => {
      alert("Error en reconocimiento: " + e.error);
      btn.disabled = false;
      btn.textContent = "Grabar";
    };

    recognition.onspeechend = () => {
      recognition.stop();
    };
  </script>
</body>
</html>





USAR DOCKER VERSION:
docker run -p 8880:8880 --name kokoro-tts-cpu ghcr.io/remsky/kokoro-fastapi-cpu:v0.2.2



