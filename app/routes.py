from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def hello_world():
    return jsonify({'message': 'Welcome to JESS API!'})