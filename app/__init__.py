from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy
#from flask_wtf.csrf import CSRFProtect
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgresadm:3fnosUd8krVC@ep-autumn-recipe-a1i2wgsj.ap-southeast-1.pg.koyeb.app:5432/resume'
db = SQLAlchemy(app)
app.secret_key = 'FBOWw0LbSJoXo1MXgjAbQw'
#csrf = CSRFProtect(app)




from app import routes