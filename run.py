"""
This file is the entry point for the application.

It creates the Flask application and adds the routes to it.
"""

from flask import Flask

# Import the database
from app.models import db

# Import the routes from app/routes.py
from app.routes import add_routes

# Import the configuration
from config import Config


def create_app():
    # Create the Flask application
    app = Flask(__name__)

    app.config["WTF_CSRF_ENABLED"] = False  # Sensitive
    app.config.from_object(Config)
    db.init_app(app)

    # Add the routes to the application
    add_routes(app)

    return app


# If this file is run directly, run the application
if __name__ == "__main__":
    app = create_app()
    app.run()
