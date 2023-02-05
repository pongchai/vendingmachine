import pytest

from app.models import db, VendingMachine
from run import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()

    yield app


def test_create_vm(app):
    with app.test_client() as client:
        response = client.post(
            "/vending-machines",
            json={"name": "Vending Machine TEST", "location": "Location TEST"},
        )
        assert response.status_code == 201
        assert response.json == {"message": "Vending Machine created successfully"}

        vm = VendingMachine.query.exists()
        assert vm is not None


def test_delete_vm(app):
    with app.test_client() as client:
        client.post(
            "/vending-machines",
            json={"name": "Vending Machine TEST", "location": "Location TEST"},
        )
        vm = VendingMachine.query.order_by(VendingMachine.id.desc()).first()
        response = client.delete(f"/vending-machines/{vm.id}")
        assert response.status_code == 200
        assert response.json == {"message": "Vending Machine deleted successfully"}


def test_create_item(app):
    with app.test_client() as client:
        client.post(
            "/vending-machines",
            json={"name": "Vending Machine TEST", "location": "Location TEST"},
        )
        vm = VendingMachine.query.order_by(VendingMachine.id.desc()).first()
        response = client.post(
            f"/create_item/{vm.id}",
            json={"name": "Item TEST", "price": 10.0, "quantity": 10},
        )
        assert response.status_code == 201
        assert response.json == {"message": "Item created successfully"}
