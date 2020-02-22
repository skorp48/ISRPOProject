from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column
from sqlalchemy import String, Integer, ForeignKey
from app import db

class Menu_str(db.Model):
    __tablename__='Menu_str'
    id = db.Column(db.Integer(), primary_key=True)
    dish_id = db.Column(db.Integer(), ForeignKey('Dish.id'))
    restaurant_id = db.Column(db.Integer(), ForeignKey('Restaurant.id'))  
    cost = db.Column(db.Integer()) 
    restaurant = db.relationship("Restaurant")
    dish = db.relationship("Dish")

class Dish(db.Model):
    __tablename__='Dish'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False) 
    desc = db.Column(db.String())
    image = db.Column(db.String())
    category_id = db.Column(db.Integer(), ForeignKey('Category.id'))
    category = db.relationship("Category")
      
    def __str__(self):
        return "{}".format(self.name)

class Restaurant(db.Model):
    __tablename__='Restaurant'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.String())
    phone = db.Column(db.String())
    coord = db.Column(db.String())
    image = db.Column(db.String())

    def __str__(self):
        return "{}".format(self.name)
   
class Category(db.Model):
    __tablename__='Category'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())

    def __str__(self):
        return "{}".format(self.name)

    __tablename__='Category'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())

    def __str__(self):
        return "{}".format(self.name)

