from flask import Flask,request, jsonify
#from flask_wtf.csrf import CSRFProtect
app = Flask(__name__)
app.secret_key = 'FBOWw0LbSJoXo1MXgjAbQw'
#csrf = CSRFProtect(app)
from app import routes