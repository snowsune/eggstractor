import logging

from flask import Flask
from .config import config


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask
app = Flask(__name__)
app.config.from_object(config)

from . import main  # Import routes
