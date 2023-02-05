import os
import sys

import pytest

from run import create_app

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
    )
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def test_app_exists(app):
    assert app is not None


def test_app_is_testing(app):
    assert app.config["TESTING"]


def test_app_is_connected_to_db(app):
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"


def test_app_is_CSRF_disabled(app):
    assert app.config["WTF_CSRF_ENABLED"] is False
