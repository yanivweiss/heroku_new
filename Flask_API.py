from flask import Flask, request, jsonify, make_response
import joblib
import pandas as pd
import os

app = Flask(__name__)

@app.route("/predict", methods=["GET"])

def predict_single():

    try:
        fixed_acidity = float(request.args.get("fixed_acidity"))
        residual_sugar = float(request.args.get("residual_sugar"))
        pH = float(request.args.get("pH"))
        alcohol = float(request.args.get("alcohol"))
        lst = pd.DataFrame.from_dict({"fixed_acidity": [fixed_acidity], "residual_sugar": [residual_sugar], "pH": [pH], "alcohol": [alcohol]})
        prediction = model.predict(lst)

    except:
        return "couldn't provide a prediction, please check your request"

    return jsonify({"prediction": str(prediction)})

@app.route("/json", methods=["POST"])
def predict_multi():
        if request.is_json:

            req = request.get_json()
            query = pd.json_normalize(req)
            prediction = list(model.predict(query))

            response_body = {
                "message": "JSON received!",
                "prediction":  str(prediction)
            }

            res = make_response(jsonify(response_body), 200)

            return res

        else:

            return make_response(jsonify({"message": "Request body must be JSON"}), 400)

if __name__ == "__main__":
    app.jinja_env.cache = {}
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    model = joblib.load("model_wine.pkl")  # Load "model.pkl"
    port = os.environ.get('PORT')
    app.run(host='0.0.0.0', port=int(port) , debug=True, use_reloader=True)
