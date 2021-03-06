from flask import Flask, request, jsonify, make_response
import joblib
import os
import pandas as pd

model = joblib.load("model_wine.pkl")  # Load "model.pkl"

app = Flask(__name__)

@app.route('/predict', methods=['GET'])

def predict_single():

    try:
        fixed_acidity = float(request.args.get('fixed_acidity'))
        residual_sugar = float(request.args.get('residual_sugar'))
        pH = float(request.args.get('pH'))
        alcohol = float(request.args.get('alcohol'))
        lst = pd.DataFrame.from_dict({'fixed_acidity': [fixed_acidity], 'residual_sugar': [residual_sugar], 'pH': [pH], 'alcohol': [alcohol]})
        prediction = model.predict(lst)

    except:
        return "couldn't provide a prediction, please check your request"

    return jsonify({'prediction': str(prediction)})

@app.route("/json", methods=["POST"])
def predict_multi():
        print(request.is_json)
        if request.is_json:

            req = request.get_json()
            print(req)
            query = pd.json_normalize(req)
            print(query)
            prediction = list(model.predict(query))
            print(prediction)

            response_body = {
                "message": "JSON received!",
                "prediction":  str(prediction)
            }

            res = make_response(jsonify(response_body), 200)
            print(res)

            return res

        else:

            return make_response(jsonify({"message": "Request body must be JSON"}), 400)

if __name__ == '__main__':
    port = os.environ.get('PORT')
    app.run(host='0.0.0.0', port=int(port))