from flask import url_for
from flask_admin import form
from flask_admin.form import rules
from flask_admin.contrib import sqla
from flask_admin.contrib.sqlamodel import ModelView
from jinja2 import Markup
from app import file_path

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
