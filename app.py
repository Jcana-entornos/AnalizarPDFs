from flask import Flask, request, jsonify
import pdfplumber
import re
from collections import defaultdict

app = Flask(__name__)
@app.route('/analizar', methods=['POST'])
def analizar():

    if request.headers.get("API-KEY") != "12345":
        return jsonify({"error": "No autorizado"}), 403

    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF recibido"}), 400

    archivo = request.files['pdf']

    resultados = defaultdict(lambda: {"total": 0, "admitidos": 0})

    regex_especialidad = re.compile(r"ESPECIALIDAD:\s*(.+)")
    VALORES_ADMITIDO = {"S", "SI"}

    especialidad_actual = None

    with pdfplumber.open(archivo) as pdf:
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

                        if any(val in linea.split() for val in VALORES_ADMITIDO):
                            resultados[especialidad_actual]["admitidos"] += 1

    return jsonify(resultados)
