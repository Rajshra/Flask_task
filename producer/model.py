from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/pydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column('id', db.Integer(), primary_key=True)
    pname = db.Column('name', db.String(100))
    pqty = db.Column('qty', db.String(100))
    pprice = db.Column('price', db.String(100))
    active = db.Column(db.String(100),default='Y')

#Product(pname,pqty,pprice)

