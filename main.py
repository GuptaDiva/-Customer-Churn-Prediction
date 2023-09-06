import pickle
from flask import Flask, request, jsonify
from ChurnDetection.ipynb import predict_msg

app = Flask('app')

@app.route('/test', methods=['GET'])
def test():
    return "Model Application!"

@app.route('/predict', methods=['POST'])
def predict():
    msg = request.json['v2']

    with open('model.pkl', 'rb') as f_in:
        model = pickle.load(f_in)
        f_in.close()

    prediction = predict_msg(msg, model)

    return prediction

if __name__ == '__main__':
    app.run(debug=True)