import os
import os.path as op

from flask_admin import Admin
from flask_admin.contrib.sqlamodel import ModelView
from flask_admin import form
from flask_admin.form import rules
from flask_admin.contrib import sqla
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column,union,intersect
from sqlalchemy import String, Integer, ForeignKey
from flask import render_template,request,redirect,session,url_for
import json
from jinja2 import Markup

from flask_admin import helpers as admin_helpers
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security import UserMixin, RoleMixin
from flask_security.utils import hash_password
from flask_security import current_user

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

file_path = op.join(op.dirname(__file__), 'static/images')

class Menu_str(db.Model):
    __tablename__='Menu_str'
    id = db.Column(db.Integer(), primary_key=True)
    dish_id = db.Column(db.Integer(), ForeignKey('Dish.id'))
    restaurant_id = db.Column(db.Integer(), ForeignKey('Restaurant.id'))  
    cost = db.Column(db.Integer()) 
    rstaurant = db.relationship("Restaurant")
    dish = db.relationship("Dish")

class MyImageView(sqla.ModelView):
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('admin')
        )

    def _handle_view(self, name, **kwargs):
            if not self.is_accessible():
                if current_user.is_authenticated:
                    # permission denied
                    abort(403)
                else:
                    return redirect(url_for('security.login', next=request.url))
    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return ''
        return Markup('<img src="%s">' % url_for('static',
                                                 filename='images/'+form.thumbgen_filename(model.image)))

    column_formatters = {
        'image': _list_thumbnail
    }

    form_extra_fields = {
        'image': form.ImageUploadField('Image',
                                      base_path=file_path,
                                      thumbnail_size=(200, 200, True))
    }

class MyModelView(sqla.ModelView):
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('admin')
        )

    def _handle_view(self, name, **kwargs):
            if not self.is_accessible():
                if current_user.is_authenticated:
                    # permission denied
                    abort(403)
                else:
                    return redirect(url_for('security.login', next=request.url))

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



roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('User.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('Role.id')))

class User(db.Model, UserMixin):
    __tablename__='User'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    active = db.Column(db.Boolean)
    #role_id = db.Column(db.Integer(), ForeignKey('Role.id'))
    #roles = db.relationship("Role")
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    __tablename__='Role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())

    def __str__(self):
        return self.name

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

admin = Admin(app)
security = Security(app, user_datastore)

admin.add_view(MyModelView(Menu_str, db.session))
admin.add_view(MyImageView(Dish, db.session))
admin.add_view(MyImageView(Restaurant, db.session))
admin.add_view(MyModelView(Category, db.session))
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Role, db.session))

@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


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
    return render_template('index.html',catlst=cat,dishlst=lst,cart=cart)

@app.route("/cart/add", methods=['POST'])
def add_to_cart():
    session['cart'] = request.values.dicts[1]['dishlst']
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

# улучшенный вариант 
@app.route("/cart/search", methods=['POST','GET'])
def search_place():
    #session['cart'] = request.values.dicts[1]['dishlst']
    lst=session['cart']
    queryA=db.session.query(Restaurant.id)
    queryA=queryA.join(Menu_str, Menu_str.restaurant_id == Restaurant.id)
    data = json.loads(lst)
    q_lst=[]
    for item in data:
        q_lst.append(queryA.filter(Menu_str.dish_id==int(item["dish"])))
    queryB=intersect(*q_lst)
    rez=db.session.execute(queryB).fetchall()
    cat = db.session.query(Category).all()
    if len(rez)==0:
        return render_template('cart.html', catlst=cat, cart=[],r_lst=[],mode=False)
    else:
        queryC=db.session.query(Restaurant)
        f_rez=[]
        for r in rez:
            rest=queryC.filter(Restaurant.id==int(r[0])).first()
            #f_rez.append(rest)
            pr=0
            owc=[]
            for item in data:
                pr=pr+int(item["quantity"])* (db.session.query(Menu_str.cost).filter(Menu_str.dish_id==int(item["dish"])).filter(Menu_str.restaurant_id==int(r[0])).first()[0])
                owp=(db.session.query(Menu_str.cost).filter(Menu_str.dish_id==int(item["dish"])).filter(Menu_str.restaurant_id==int(r[0])).first()[0])
                own=db.session.query(Dish.name).filter(Dish.id==int(item["dish"])).first()[0]
                owq=int(item["quantity"])
                owc.append([own,owp,owq])
            f_rez.append({'rest':rest,'total':pr,'dl':owc})
        query = db.session.query(Dish)
        dish_cart_list = []
        for item in data:
            cart_dish_id = item["dish"]
            dishes = query.filter(Dish.id == int(cart_dish_id)).all()
            dish_cart_list.append(dishes[0])
        return render_template('found_restaurant.html', catlst=cat, cart=dish_cart_list, r_lst=f_rez)
        #return render_template('cart.html', catlst=cat, cart=[],r_lst=f_rez,mode=False)
    return redirect(url_for('cart'))


@app.route("/cart", methods=['POST','GET'])
def cart():
    cat = db.session.query(Category).all()
    if 'cart' in session:
        lst=session['cart']
    else:
        return render_template('cart.html',catlst=cat,cart=[])
    cat = db.session.query(Category).all()
    dish_cart_list=[]
    query = db.session.query(Dish)
    data = json.loads(lst)
    for item in data:
        cart_dish_id = item["dish"]
        dishes = query.filter(Dish.id == int(cart_dish_id)).all()
        dish_cart_list.append({"dish":dishes[0],"quantity":item["quantity"]})
    return render_template('cart.html',catlst=cat,cart=dish_cart_list)

@app.route("/admin", methods=['POST'])
def add_user():
    if request.method == 'POST':
        email = request.form.get('login')
        password = request.form.get('password')
        user_datastore.create_user(email=email, password=hash_password(password))
        db.session.commit()

    return redirect(url_for("admin.index"))
@app.route('/')
def hello_world():
    cat = db.session.query(Category).all()
    return render_template('index.html',catlst=cat,cart=cart)

