import os
import os.path as op

from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
import json

app = Flask(__name__,  static_folder = 'files')
app.config.from_object('config.Config')

db = SQLAlchemy(app)

file_path = op.join(op.dirname(__file__), 'files')
try:
    os.mkdir(file_path)
except OSError:
    pass


admin = Admin(app)

from app.models import Menu_str, Dish, Restaurant, Category
from app.views import ImageView, ModelView
admin.add_view(ModelView(Menu_str, db.session))
admin.add_view(ImageView(Dish, db.session))
admin.add_view(ImageView(Restaurant, db.session))
admin.add_view(ModelView(Category, db.session))



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

@app.route("/cart", methods=['POST'])
def cart():
    lst = request.values.dicts[1]['dishlst']
    global cart
    cat = db.session.query(Category).all()
    dish_cart_list=[]
    query = db.session.query(Dish)
    data = json.loads(lst)
    for item in data:
        cart_dish_id = item["dish"]
        dishes = query.filter(Dish.id == int(cart_dish_id)).all()
        dish_cart_list.append({"dish":dishes[0],"quantity":item["quantity"]})
    return render_template('cart.html',catlst=cat,cart=dish_cart_list)

@app.route('/')
def hello_world():
    cat = db.session.query(Category).all()
    return render_template('index.html',catlst=cat)

