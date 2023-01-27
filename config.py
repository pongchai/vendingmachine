import os

basedir = os.path.abspath(os.path.dirname(__file__)) 

class Config(object):
    """
    Configuration class for the application

    Attributes:
        SQLALCHEMY_DATABASE_URI: Path to the database
        SQLALCHEMY_TRACK_MODIFICATIONS: track modifications to the database (default: True)
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'identifier.sqlite') # Path to the database
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Disable tracking of modifications
