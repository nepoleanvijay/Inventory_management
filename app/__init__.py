from flask import Flask
from .shop.routes import shop
from .customer.routes import customer

def create_app():
    app = Flask(__name__)
    # app.config.from_object('config.Config')

    app.register_blueprint(shop)
    app.register_blueprint(customer)


    return app
