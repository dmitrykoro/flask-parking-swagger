from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask import request, jsonify
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.extension import FlaskApiSpec
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from marshmallow import Schema, fields
from werkzeug.security import check_password_hash, generate_password_hash

import request_handler

app = Flask(__name__)  # Flask app instance initiated
# api = Api(app)  # Flask restful wraps Flask app around it.
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Flask-parking',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/api/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)

jwt = JWTManager(app)

app.config.update(
    JWT_SECRET_KEY="0000",
)

users = {
    "admin": generate_password_hash("0000"),
    "string": generate_password_hash("string")
}


class AcceptSchema(Schema):
    type = fields.Str()


class CheckoutSchema(Schema):
    type = fields.Str()
    amount = fields.Int()


class AuthorizationSchema(Schema):
    access_token = fields.Str()


@app.route('/')
def status():
    return 'Parking Service is running'


@doc(
    description='Token access',
    params={
        'Authorization': {
            'description':
            'Authorization: Bearer <jws-token>',
            'in': 'header',
            'type': 'string',
            'required': True
        }
    })
@app.route("/login", methods=["POST"])
@use_kwargs({'username': fields.Str(), 'password': fields.Str()})
#@marshal_with(AuthorizationSchema)
def login_page(**kwargs):
    username = request.json.get("username")
    password = request.json.get("password")

    if username in users:
        if check_password_hash(users.get(username), password):
            print('Checked successfully')
            access_token = create_access_token(identity=username)
            print(access_token)
            token = str(jsonify(access_token=access_token))
            return token, 200

    return "Wrong user or password", 400


@app.route('/user/park', methods=['POST'])
@use_kwargs({'number': fields.Str()})
@marshal_with(AcceptSchema)
def handle_park(**kwargs):
    request_data = request.get_json()
    return request_handler.park(request_data)


@app.route('/user/unpark', methods=['POST'])
@use_kwargs({'number': fields.Str()})
@marshal_with(CheckoutSchema)
def handle_unpark(**kwargs):
    request_data = request.get_json()
    return request_handler.unpark(request_data)


@app.route('/admin/log', methods=['GET'])
@marshal_with(AcceptSchema)
@jwt_required()
def handle_log(**kwargs):
    return request_handler.log()


@app.route('/admin/history', methods=['GET'])
@marshal_with(AcceptSchema)
@jwt_required()
def handle_history(**kwargs):
    return request_handler.history()


@app.route('/admin/total', methods=['GET'])
@marshal_with(AcceptSchema)
@jwt_required()
def handle_total(**kwargs):
    return request_handler.total()


docs.register(login_page)
docs.register(status)
docs.register(handle_park)
docs.register(handle_unpark)
docs.register(handle_log)
docs.register(handle_history)
docs.register(handle_total)

if __name__ == '__main__':
    app.run(debug=True)
