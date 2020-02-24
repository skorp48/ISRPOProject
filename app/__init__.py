import os
import os.path as op

from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
import json

app = Flask(__name__,  static_folder = 'static')
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
