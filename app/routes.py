"""
Vending Machine Operations.

This module contains functions to perform operations related to
vending machines such as creating and deleting vending machines,
creating and updating items in vending machine stock, and editing stock.

This module makes use of the Flask library to handle HTTP requests and
responses and SQLAlchemy ORM to interact with a database.

Functions:
create_vm: Create a vending machine.
delete_vm: Delete a vending machine.
create_item: Create an item in the vending machine stock.
add_item_stock: Add quantity to an item in the vending machine stock.
edit_item_stock: Edit the quantity of an item in the vending machine stock.
remove_item_from_stock: Remove an item from the vending machine stock.

"""
from typing import Union

from flask import Flask, Response, jsonify, request

from app.models import Item, VendingMachine, db


# Create a vending machine
def create_vm() -> tuple[Response, int]:
    """Create a vending machine.

    Returns:
        A message indicating the vending machine was created.

    Raises:
        400: If the name or location are missing.

    """
    name = request.json.get("name")
    location = request.json.get("location")
    if not all([name, location]):
        return jsonify({"error": "Name and location are required"}), 400
    vm = VendingMachine(name=name, location=location)
    db.session.add(vm)
    db.session.commit()
    return jsonify({"message": "Vending Machine created successfully"}), 201


# Delete vending machine
def delete_vm(vm_id: int) -> tuple[Response, int]:
    """Delete a vending machine.

    Args:
        vm_id: The id of the vending machine.

    Returns:
        A message indicating the vending machine was deleted.

    """
    vm = VendingMachine.query.get(vm_id)
    if not vm:
        return jsonify({"error": "Vending machine not found"}), 404
    db.session.delete(vm)
    db.session.commit()
    return jsonify({"message": "Vending Machine deleted successfully"}), 200


# Create item in vending machine
def create_item(vm_id: int) -> tuple[Response, int]:
    """Create an item in the vending machine stock.

    Args:
        vm_id: The id of the vending machine.

    Returns:
        A message indicating the item was created.

    Raises:
        400: If the name, price, or quantity are missing.
        404: If the vending machine is not found.
        500: If an error occurs.

    """
    try:
        name = request.json.get("name")
        price = request.json.get("price")
        quantity = request.json.get("quantity")

        if not name or not price or not quantity:
            return (
                jsonify(
                    {
                        "error": "Missing required parameters"
                        ": "
                        "name, price, quantity"
                    }
                ),
                400,
            )

        vm = VendingMachine.query.get(vm_id)
        if not vm:
            return jsonify({"error": "Vending machine not found"}), 404

        item = Item(name=name, price=price, quantity=quantity, vending_machine=vm)
        db.session.add(item)
        db.session.commit()
        return jsonify({"message": "Item created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Add product quantity to the vending machine
def add_item_stock(vm_id: int, item_id: int) -> tuple[Response, int]:
    """
    Add quantity to an item in the vending machine stock.

    Args:
        vm_id: The id of the vending machine.
        item_id: The id of the item.

    Returns:
        A message indicating the item stock was added.

    Raises:
        404: If the vending machine or item is not found.
        500: If an error occurs.


    """
    try:
        quantity = request.json.get("quantity")
        vm = VendingMachine.query.get(vm_id)
        item = Item.query.get(item_id)
        if not vm:
            return jsonify({"error": "Vending machine not found"}), 404
        if not item:
            return jsonify({"error": "Item not found"}), 404
        item.quantity += quantity
        db.session.commit()
        return jsonify({"message": "Item stock added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Edit stock
def edit_item_stock(vm_id: int, item_id: int) -> tuple[Response, int]:
    """
    Edit the quantity of an item in the vending machine stock.

    Args:
        vm_id: The id of the vending machine.
        item_id: The id of the item.

    Returns:
        A message indicating the item stock was updated.
    """
    try:
        quantity = request.json.get("quantity")
        vm = VendingMachine.query.get(vm_id)
        if not vm:
            return jsonify({"error": "Vending machine not found"}), 404
        item = Item.query.get(item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404
        item.quantity = quantity
        db.session.commit()
        return jsonify({"message": "Item stock updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Remove item
def remove_item_from_stock(vm_id: int, item_id: int) -> tuple[Response, int]:
    """
    Remove an item from the vending machine stock.

    Args:
        vm_id: The id of the vending machine.
        item_id: The id of the item.

    Returns:
        A message indicating the item was removed from stock.
    """
    try:
        quantity = request.json.get("quantity")
        vm = VendingMachine.query.get(vm_id)
        item = Item.query.get(item_id)
        if not vm:
            return jsonify({"error": "Vending machine not found"}), 404
        if not item:
            return jsonify({"error": "Item not found"}), 404
        if item.quantity - quantity < 0:
            return jsonify({"error": "Not enough items in stock"}), 400
        item.quantity = item.quantity - quantity
        db.session.commit()
        return jsonify({"message": "Item removed from stock"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get Item in Vending Machine by ID
def get_stock_by_vm(vm_id: int) -> Union[Response, tuple[Response, int]]:
    """Retrieve all items in a vending machine and return them as a list of dictionaries.

    Args:
        vm_id: The id of the vending machine.

    Returns:
        A list of dictionaries containing the item id, name,
        price and quantity.
    """
    vm = VendingMachine.query.get(vm_id)
    if not vm:
        return jsonify(
            {"message": "Vending Machine not found, please " "call the correct ID"}, 404
        )
    items = [
        {
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "quantity": item.quantity,
        }
        for item in vm.items
    ]
    return jsonify(items), 200


# Get all Vending Machine
def view_vm() -> Response:
    """Get all vending machines in the database and return them
    as a list of dictionaries.

    Returns:
        A list of dictionaries containing the vending machine

    """
    vending_machines = VendingMachine.query.all()
    vm_lst = [
        {"id": vm.id, "name": vm.name, "location": vm.location}
        for vm in vending_machines
    ]
    if not vm_lst:
        return jsonify({"message": "No Vending Machine found"})
    return jsonify(vm_lst)


def add_routes(app: Flask) -> None:
    """
    Add routes to the Flask application.

    Args:
        app: The Flask application instance.

    Returns:
        None
    """
    app.add_url_rule("/vending-machines", view_func=create_vm, methods=["POST"])
    app.add_url_rule(
        "/vending-machines/<int:vm_id>", view_func=delete_vm, methods=["DELETE"]
    )
    app.add_url_rule(
        "/create_item/<int:vm_id>", view_func=create_item, methods=["POST"]
    )
    app.add_url_rule(
        "/add_item_stock/<int:vm_id>/<int:item_id>",
        view_func=add_item_stock,
        methods=["PUT"],
    )
    app.add_url_rule(
        "/edit_item_stock/<int:vm_id>/<int:item_id>",
        view_func=edit_item_stock,
        methods=["PUT"],
    )
    app.add_url_rule(
        "/remove_item_from_stock/<int:vm_id>/<int:item_id>",
        view_func=remove_item_from_stock,
        methods=["PUT"],
    )
    app.add_url_rule(
        "/view_items_in_vending_machine/<int:vm_id>",
        view_func=get_stock_by_vm,
        methods=["GET"],
    )
    app.add_url_rule("/get_vending_machines", view_func=view_vm, methods=["GET"])
