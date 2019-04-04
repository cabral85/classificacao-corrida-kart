from flask import Flask
from flask import request
from flask import json
import pandas as pd
import corrida

app = Flask(__name__)

@app.route('/', methods=['GET'])
def resultado():
    retorno = corrida.resultadoCorrida()
    response = app.response_class(
        response=retorno.to_json(),
        status=200,
        mimetype='application/json'
    )
    return response

app.run(host='0.0.0.0', port=8080)