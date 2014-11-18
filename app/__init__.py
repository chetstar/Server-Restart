from flask import Flask
from flask_bootstrap import Bootstrap

# import datetime

app = Flask(__name__)


app.config.from_object('config')


# @app.template_filter('reverse')
# def reverse_filter(s):
#     if s > datetime.date.today():
#       return 0
#     else:
#        return 1



Bootstrap(app)
# from flask.ext.mail import Mail
# mail = Mail(app)
from app import views
