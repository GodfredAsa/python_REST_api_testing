"""
THIS CLASS IS THE PARENT CLASS TO NON-UNIT TEST
ALLOWS FOR INSTANTIATION OF DATABASE DYNAMICALLY
ENSURES THAT IT A NEW, BLANK DATABASE EACH TIME

1. SET UP THE DATABASE AND GIVE THE TEST CLIENT
"""

from unittest import TestCase
from starter_code.app import app
from starter_code.db import db
import os


class BaseTest(TestCase):
    def setUp(self) -> None:
        # make sure DB exists
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite///'
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///')

        with app.app_context():
            db.init_app(app)
            db.create_all()
        # Get a test client
        self.app = app.test_client()
        self.app_context = app.app_context

    def tearDown(self) -> None:
        # ensure the DB is blanked and dropped
        with app.app_context():
            db.session.remove()
            db.drop_all()

