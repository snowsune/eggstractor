from flask import Flask
from celery import Celery
from .config import config


def make_celery(app):
    celery = Celery(
        app.import_name, broker=app.config["REDIS_URL"], backend=app.config["REDIS_URL"]
    )
    celery.conf.update(app.config)
    return celery


app = Flask(__name__)
app.config.from_object(config)
celery = make_celery(app)

from . import main  # Import routes
