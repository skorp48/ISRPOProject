from flask_admin import Admin
from flask_admin.contrib.sqlamodel import ModelView
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column,union,intersect
from sqlalchemy import String, Integer, ForeignKey
from flask import render_template,request,redirect,session,url_for
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




@app.route('/каталог/<string:kat_name>')
def hello_world_again(kat_name):
    cat = db.session.query(Category).all()
    query = db.session.query(Category, Dish)
    query = query.join(Dish, Dish.category_id == Category.id)
    lst = []
    dishes = query.filter(Category.name == kat_name).all()
    for category, dish in dishes:
        lst.append(dish)
    return render_template('index.html', catlst=cat, dishlst=lst, cart=cart)


@app.route("/cart/add", methods=['POST'])
def add_to_cart():
    session['cart'] = request.values.dicts[1]['dishlst']
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/cart/search", methods=['POST', 'GET'])
def search_place():
    lst = session['cart']
    queryA = db.session.query(Restaurant.id)
    queryA = queryA.join(Menu_str, Menu_str.restaurant_id == Restaurant.id)
    data = json.loads(lst)
    q_lst = []
    for item in data:
        q_lst.append(queryA.filter(Menu_str.dish_id == int(item["dish"])))
    queryB = intersect(*q_lst)
    rez = db.session.execute(queryB).fetchall()
    if len(rez) == 0:
        cat = db.session.query(Category).all()
        return render_template('found_restaurant.html', catlst=cat, r_lst=[])
    else:
        queryC = db.session.query(Restaurant)
        f_rez = []
        for r in rez:
            rest = queryC.filter(Restaurant.id == int(r[0])).first()
            f_rez.append(rest)
            cat = db.session.query(Category).all()

        query = db.session.query(Dish)
        dish_cart_list = []
        for item in data:
            cart_dish_id = item["dish"]
            dishes = query.filter(Dish.id == int(cart_dish_id)).all()
            dish_cart_list.append(dishes[0])
        return render_template('found_restaurant.html', catlst=cat, cart=dish_cart_list, r_lst=f_rez)


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
    return render_template('index.html', catlst=cat, dishlst=dish_cart_list, cart=cart, mode=True)


@app.route("/cart", methods=['POST', 'GET'])
def cart():
    cat = db.session.query(Category).all()
    if 'cart' in session:
        lst = session['cart']
    else:
        return render_template('cart.html', catlst=cat, cart=[])
    cat = db.session.query(Category).all()
    dish_cart_list = []
    query = db.session.query(Dish)
    data = json.loads(lst)
    for item in data:
        cart_dish_id = item["dish"]
        dishes = query.filter(Dish.id == int(cart_dish_id)).all()
        dish_cart_list.append({"dish": dishes[0], "quantity": item["quantity"]})
    return render_template('cart.html', catlst=cat, cart=dish_cart_list, mode=True)


@app.route('/')
def hello_world():
    cat = db.session.query(Category).all()
    return render_template('index.html', catlst=cat, cart=cart)


app.run()
