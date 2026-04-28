from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import re
from collections import defaultdict
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔹 Compilar regex una sola vez (más rápido)
REGEX_ESPECIALIDAD = re.compile(r"ESPECIALIDAD:\s*(.+)")
REGEX_SI = re.compile(r"\b(SI|S)\b", re.IGNORECASE)

@app.route('/')
def index():
    return jsonify({"status": "API funcionando"})

@app.route('/analizar', methods=['POST'])
def analizar():
    try:
        # 🔐 Seguridad básica
        if request.headers.get("API-KEY") != "12345":
            return jsonify({"error": "No autorizado"}), 403

        if 'pdf' not in request.files:
            return jsonify({"error": "No PDF recibido"}), 400

        archivo = request.files['pdf']

        resultados = defaultdict(lambda: {"total": 0, "admitidos": 0})
        especialidad_actual = None

        # 🔥 Abrir PDF directamente desde stream (menos RAM)
        pdf_bytes = archivo.read()

        with fitz.open(stream=pdf_bytes, filetype="pdf") as pdf:
            for pagina in pdf:
                texto = pagina.get_text()

                if not texto:
                    continue

                for linea in texto.split("\n"):
                    linea = linea.strip()

                    if len(linea) < 3:
                        continue

                    # Detectar especialidad
                    match = REGEX_ESPECIALIDAD.search(linea)
                    if match:
                        especialidad_actual = match.group(1).strip()
                        continue

                    # Detectar "SI" o "S"
                    if REGEX_SI.search(linea):
                        if especialidad_actual:
                            resultados[especialidad_actual]["total"] += 1
                            resultados[especialidad_actual]["admitidos"] += 1

        return jsonify(resultados)

    except Exception as e:
        return jsonify({
            "error": str(e),
            "type": type(e).__name__
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
