import os
import sys

import pytest

from app.models import VendingMachine, Item

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture(scope="module")
def new_vending_machine():
    return VendingMachine(name="VM1", location="Location1")


@pytest.fixture(scope="module")
def new_item(new_vending_machine):
    return Item(
        name="Item1", price=1.00, quantity=10, vending_machine=new_vending_machine
    )


def test_vending_machine_creation(new_vending_machine):
    assert new_vending_machine.name == "VM1"
    assert new_vending_machine.location == "Location1"


def test_item_creation(new_item):
    assert new_item.name == "Item1"
    assert new_item.price == 1.0
    assert new_item.quantity == 10
    assert new_item.vending_machine.name == "VM1"
    assert new_item.vending_machine.location == "Location1"
