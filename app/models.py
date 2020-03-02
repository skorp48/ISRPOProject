from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column
from sqlalchemy import String, Integer, ForeignKey
from app import db
from flask_security import UserMixin, RoleMixin


class Menu_str(db.Model):
    __tablename__ = 'Menu_str'
    id = db.Column(db.Integer(), primary_key=True)
    dish_id = db.Column(db.Integer(), ForeignKey('Dish.id'))
    restaurant_id = db.Column(db.Integer(), ForeignKey('Restaurant.id'))
    cost = db.Column(db.Integer())
    restaurant = db.relationship("Restaurant")
    dish = db.relationship("Dish")


class Dish(db.Model):
    __tablename__ = 'Dish'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    desc = db.Column(db.String())
    image = db.Column(db.String())
    category_id = db.Column(db.Integer(), ForeignKey('Category.id'))
    category = db.relationship("Category")

    def __str__(self):
        return "{}".format(self.name)


class Restaurant(db.Model):
    __tablename__ = 'Restaurant'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())

    def __str__(self):
        return "{}".format(self.name)

class RestAddress(db.Model):
    __tablename__ = 'RestAddress'
    id = db.Column(db.Integer(), primary_key=True)
    address = db.Column(db.String())
    phone = db.Column(db.String())
    coord = db.Column(db.String())
    image = db.Column(db.String())
    rest_id = db.Column(db.Integer(), ForeignKey('Restaurant.id'))
    restaurant = db.relationship("Restaurant")



class Category(db.Model):
    __tablename__ = 'Category'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())

    def __str__(self):
        return "{}".format(self.name)


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('User.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('Role.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    active = db.Column(db.Boolean)
    #role_id = db.Column(db.Integer(), ForeignKey('Role.id'))
    #roles = db.relationship("Role")
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'Role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())

    def __str__(self):
        return self.name
