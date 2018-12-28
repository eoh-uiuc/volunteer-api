from flask import Flask, request

import auth
from models.user import User
from mongo import DBClient

app = Flask(__name__)
client = None

@app.route('/', methods=['GET'])
def index():
    return 'EOH Volunteer API'

@app.route('/register/', methods=['POST'])
def register():
    return auth.register(client, request)

@app.route('/login/', methods=['POST'])
def login():
    return auth.login(client, request)

@app.route('/delete_user/', methods=['POST'])
def remove():
    return auth.delete(client, request)

if __name__ == '__main__':
    client = DBClient()
    app.run(debug=True, threaded=True)