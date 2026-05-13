import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

model_params = {"w": 0.8020, "b": 1.9888}

def train_on_start():
    try:
        df = pd.read_csv('TRAIN2.xlsx - Sheet1.csv')
        X, Y = df['midterm'].values, df['final'].values
        w, b, lr, n = 0.0, 0.0, 0.01, float(len(X))
        for _ in range(1000):
            y_p = w * X + b
            dw = (2/n) * np.sum(X * (y_p - Y))
            db = (2/n) * np.sum(y_p - Y)
            w -= lr * dw
            b -= lr * db
        return round(w, 4), round(b, 4)
    except:
        return 0.8020, 1.9888

model_params["w"], model_params["b"] = train_on_start()

# Route phục vụ giao diện Web
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Route xử lý dự đoán
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    x = float(data['midterm'])
    y = model_params["w"] * x + model_params["b"]
    return jsonify({
        "final": round(max(0, min(10, y)), 2),
        "w": model_params["w"],
        "b": model_params["b"]
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)