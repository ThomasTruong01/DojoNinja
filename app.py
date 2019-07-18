from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func
app = Flask(__name__)
# configurations to tell our app about the database we'll be connecting to
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dojo_n_ninjas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# an instance of the ORM
db = SQLAlchemy(app)
# a tool for allowing migrations/creation of tables
migrate = Migrate(app, db)


class Dojo(db.Model):
    __tablename__ = "dojos"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    city = db.Column(db.String(45))
    state = db.Column(db.String(45))
    created_on = db.Column(db.DateTime, server_default=func.now())
    updated_on = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now())


class Ninja(db.Model):
    __tablename__ = "ninjas"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    dojo_id = db.Column(
        db.Integer, db.ForeignKey("dojos.id"), nullable=False)
    dojo = db.relationship('Dojo', foreign_keys=[
        dojo_id], backref="ninjas", cascade="all")
    created_on = db.Column(db.DateTime, server_default=func.now())
    updated_on = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now())


@app.route('/')
def root():
    dojoList = Dojo.query.all()
    return render_template('index.html', dojos=dojoList)


@app.route('/addDojo', methods=['POST'])
def addDojo():
    newDojo = Dojo(name=request.form['name'],
                   city=request.form['city'],
                   state=request.form['state'])
    db.session.add(newDojo)
    db.session.commit()
    return redirect('/')


@app.route('/addNinja', methods=['POST'])
def addNinja():
    newNinja = Ninja(
        first_name=request.form['fName'], last_name=request.form['lName'], dojo_id=request.form['dojoLocation'])
    db.session.add(newNinja)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
