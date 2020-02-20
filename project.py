from flask_admin import Admin
from flask_admin.contrib.sqlamodel import ModelView
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column
from sqlalchemy import String, Integer, ForeignKey
from flask import render_template,request
import json
app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)


class Menu_str(db.Model):
    __tablename__='Menu_str'
    id = db.Column(db.Integer(), primary_key=True)
    dish_id = db.Column(db.Integer(), ForeignKey('Dish.id'))
    restaurant_id = db.Column(db.Integer(), ForeignKey('Restaurant.id'))  
    cost = db.Column(db.Integer()) 
    rstaurant = db.relationship("Restaurant")
    dish = db.relationship("Dish")


class Dish(db.Model):
    __tablename__='Dish'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String()) 
    desc = db.Column(db.String())
    image = db.Column(db.String())
    category_id = db.Column(db.Integer(), ForeignKey('Category.id'))
    dish = db.relationship("Category")
      
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



admin = Admin(app)


admin.add_view(ModelView(Menu_str, db.session))
admin.add_view(ModelView(Dish, db.session))
admin.add_view(ModelView(Restaurant, db.session))
admin.add_view(ModelView(Category, db.session))


#app.run()

@app.route('/каталог/<string:kat_name>')
def hello_world_again(kat_name):
    cat = db.session.query(Category).all()
    query=db.session.query(Category,Dish)
    query=query.join(Dish, Dish.category_id == Category.id)
    lst=[]
    dishes=query.filter(Category.name==kat_name).all()
    for category,dish in dishes:
        lst.append(dish)
    #last_ds=lst
    return render_template('index.html',catlst=cat,dishlst=lst)

@app.route("/check_cart", methods=['POST'])
def check_cart():
    lst = request.values.dicts[1]['dishlst']
    cat = db.session.query(Category).all()
    query = db.session.query(Dish)
    dish_cart_list = []
    data = json.loads(lst)
    for item in data:
        cart_dish_id = item["dish"]
        dishes = query.filter(Dish.id == int(cart_dish_id)).all()
        dish_cart_list.append(dishes[0])
    return render_template('index.html', catlst=cat, dishlst=dish_cart_list, cart=cart)

@app.route('/')
def hello_world():
    cat = db.session.query(Category).all()
    return render_template('index.html',catlst=cat)

