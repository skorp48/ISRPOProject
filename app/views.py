from flask import url_for, render_template, request
from flask_admin import form
from flask_admin.form import rules
from flask_admin.contrib import sqla
from flask_admin.contrib.sqlamodel import ModelView
from jinja2 import Markup
from app import file_path, app, db
from app.models import Menu_str, Dish, Restaurant, Category
import json

class ImageView(sqla.ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return ''
        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.image)))

    column_formatters = {
        'image': _list_thumbnail
    }

    form_extra_fields = {
        'image': form.ImageUploadField('Image',
                                      base_path=file_path,
                                      thumbnail_size=(200, 200, True))
    }

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

