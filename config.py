class Config:
    # Тема bootstrap
    FLASK_ADMIN_SWATCH = 'Flatly'

    SECRET_KEY = '123456790'

    # БД
    DATABASE_FILE = 'project.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
