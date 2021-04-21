from flask import request
from flask_apispec import marshal_with, doc, use_kwargs
from flask_jwt_extended import jwt_required, create_access_token
from marshmallow import Schema, fields
from werkzeug.security import check_password_hash
import request_handler
from config import *


class AcceptSchema(Schema):
    type = fields.Str()


class TotalSchema(Schema):
    total = fields.Str()


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
@marshal_with(AuthorizationSchema)
def login_page(**kwargs):
    username = request.json.get("username")
    password = request.json.get("password")

    if username in users:
        if check_password_hash(users.get(username), password):
            access_token = create_access_token(identity=username)
            response = {"access_token": access_token}
            return response, 200
            #OR
            #return access_token, 200

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
@app.route('/admin/log', methods=['GET'])
#@marshal_with(AcceptSchema)
@jwt_required()
def handle_log(**kwargs):
    data = request_handler.log()
    return data


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
@app.route('/admin/history', methods=['GET'])
#@marshal_with(AcceptSchema)
@jwt_required()
def handle_history(**kwargs):
    return request_handler.history()


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
@app.route('/admin/total', methods=['GET'])
@marshal_with(TotalSchema)
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
    app.run()
