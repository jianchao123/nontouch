# coding:utf-8
try:
    from flask_sqlalchemy import SQLAlchemy
    from app import app
except:
    import traceback
    print traceback.format_exc()

db = SQLAlchemy(app)


