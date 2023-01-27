from flask import jsonify, request
from app.models import VendingMachine, Item, db


# Create a vending machine
def create_vm():
    name = request.json.get('name')
    location = request.json.get('location')
    if not all([name, location]):
        return jsonify({"error": "Name and location are required"}), 400
    vm = VendingMachine(name=name, location=location)
    db.session.add(vm)
    db.session.commit()
    return jsonify({'message': 'Vending Machine created successfully'}), 201


# Delete vending machine
def delete_vm(vm_id):
    vm = VendingMachine.query.get(vm_id)
    if not vm:
        return jsonify({"error": "Vending machine not found"}), 404
    db.session.delete(vm)
    db.session.commit()
    return jsonify({'message': 'Vending Machine deleted successfully'}), 200


# Create item in vending machine
def create_item(vm_id):
    try:
        name = request.json.get('name')
        price = request.json.get('price')
        quantity = request.json.get('quantity')

        if not name or not price or not quantity:
            return jsonify({"error": "Missing required parameters: name, price, quantity"}), 400

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
def add_item_stock(vm_id, item_id):
    try:
        quantity = request.json.get('quantity')
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
def edit_item_stock(vm_id, item_id):
    try:
        quantity = request.json.get('quantity')
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
def remove_item_from_stock(vm_id, item_id):
    try:
        quantity = request.json.get('quantity')
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
def get_stock_by_vm(vm_id):
    vm = VendingMachine.query.get(vm_id)
    if not vm:
        return jsonify({'message': 'Vending Machine not found, please call the correct ID'})
    items = [{'id': item.id, 'name': item.name, 'price': item.price, 'quantity': item.quantity} for item in
             vm.items]
    return jsonify(items)


# Get all Vending Machine
def view_vm():
    vending_machines = VendingMachine.query.all()
    vm_lst = [{'id': vm.id, 'name': vm.name, 'location': vm.location} for vm in vending_machines]
    return jsonify(vm_lst)
