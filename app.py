from flask import Flask, request, jsonify, render_template
import pdfplumber
import re
from collections import defaultdict
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 👈 ahora sí está bien

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analizar', methods=['POST'])
def analizar():
    try:
        if request.headers.get("API-KEY") != "12345":
            return jsonify({"error": "No autorizado"}), 403

        if 'pdf' not in request.files:
            return jsonify({"error": "No PDF recibido"}), 400

        archivo = request.files['pdf']
        pdf_bytes = archivo.read()

        resultados = defaultdict(lambda: {"total": 0, "admitidos": 0})

        regex_especialidad = re.compile(r"ESPECIALIDAD:\s*(.+)")
        especialidad_actual = None

        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text()
                if not texto:
                    continue

                for linea in texto.split("\n"):

                    match = regex_especialidad.search(linea)
                    if match:
                        especialidad_actual = match.group(1).strip()
                        continue

                    if re.search(r"\*{4}\d{3,4}\*", linea):
                        if especialidad_actual:
                            resultados[especialidad_actual]["total"] += 1

                            # 👇 mejora aquí
                            if re.search(r"\b(S|SI)\b", linea):
                                resultados[especialidad_actual]["admitidos"] += 1

        return jsonify(resultados)

    except Exception as e:
        return jsonify({
            "error": str(e),
            "type": type(e).__name__
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
