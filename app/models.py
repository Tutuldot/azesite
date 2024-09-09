from. import db
from flask_sqlalchemy import SQLAlchemy



class Pages(db.Model):

    __tablename__ = 'pages'
    __table_args__ = {'schema': 'trans'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    content = db.Column(db.Text)

    def __init__(self, name, content):
        self.name = name
        self.content = content

    def __repr__(self):
        return f"Pages('{self.name}', '{self.content}')"
