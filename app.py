from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/analizar', methods=['POST'])
def analizar():
    return jsonify({"ok": True})

if __name__ == '__main__':
    app.run()
