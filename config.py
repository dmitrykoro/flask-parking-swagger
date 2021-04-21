from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask_apispec.extension import FlaskApiSpec
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Flask-parking',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
    'APISPEC_SWAGGER_UI_URL': '/api/'
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