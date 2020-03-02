import os
import os.path as op

from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_security import Security, SQLAlchemyUserDatastore
import json


app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

file_path = op.join(op.dirname(__file__), 'static/images')
try:
    os.mkdir(file_path)
except OSError:
    pass



from app.models import Menu_str, Dish, Restaurant, Category, User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

admin = Admin(app)
security = Security(app, user_datastore)

from app.views import MyModelView, MyImageView

admin.add_view(MyModelView(Menu_str, db.session))
admin.add_view(MyImageView(Dish, db.session))
admin.add_view(MyImageView(Restaurant, db.session))
admin.add_view(MyModelView(Category, db.session))
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Role, db.session))

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )
