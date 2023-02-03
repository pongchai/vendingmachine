"""
Module for handling application configuration.

This module contains a single class Config which represents
the configuration for the application.

Classes:
Config: A class that holds the configuration for the application, including
the SQLAlchemy database URI and the SQLAlchemy modification tracking setting.

"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Configuration class for the application.

    Attributes:
        SQLALCHEMY_DATABASE_URI: Path to the database
        SQLALCHEMY_TRACK_MODIFICATIONS: track modifications to the db
    """

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        basedir, "identifier.sqlite"
    )  # Path to the database
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable tracking of modifications
