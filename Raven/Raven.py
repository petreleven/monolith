from flask import Flask, jsonify
from typing import DefaultDict, List
from werkzeug.exceptions import default_exceptions, HTTPException, abort
import uuid
from flask_wtf import CSRFProtect

app = Flask(__name__)


def create_jsonApp(blueprints: List = [], isJSon=True):
    def error_handling(error):
        result: DefaultDict = {}
        if isinstance(error, HTTPException):
            result = {'code': error.code, 'description': error.description,
                      'message': str(error)}
        else:
            description = abort.mapping[500].description
            result = {'code': 500, 'description': description,
                      'message': str(error)}

        response = jsonify(result)
        response.status_code = result['code']
        return response

    #HANDLE ERRORS AS JSON
    if isJSon:
        for code in default_exceptions.keys():
            app.register_error_handler(code, error_handling)

    if len(blueprints)>0:
        for bluprnt in blueprints:
            app.register_blueprint(bluprnt)

    #ADD SECRET KEY
    app.secret_key = uuid.uuid4().hex

    # Add csrf protection
    csrf = CSRFProtect()
    csrf.init_app(app)
    
    return app
