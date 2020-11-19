from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
import config as cf
config = cf.config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()


def create_app(config_name):
    app = Flask(__name__)
    conf = config[config_name]
    app.config.from_object(conf)
    conf.init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
