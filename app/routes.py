from flask import jsonify, request
from app.models import VendingMachine, Item, db

# Create a vending machine
def create_vm():
    '''
    Create a vending machine.

    Returns:
        A message indicating the vending machine was created.   

    Raises:
        400: If the name or location are missing.
 
    '''
    name = request.json.get('name')
    location = request.json.get('location')
    if not all([name, location]):
        return jsonify({"error": "Name and location are required"}), 400
    vm = VendingMachine(name=name, location=location)
    db.session.add(vm)
    db.session.commit()
    return jsonify({'message': 'Vending Machine created successfully'}), 201


# Delete vending machine
def delete_vm(vm_id: int):
    '''
    Delete a vending machine.

    Args:
        vm_id: The id of the vending machine.

    Returns:
        A message indicating the vending machine was deleted.
    '''
    vm = VendingMachine.query.get(vm_id)
    if not vm:
        return jsonify({"error": "Vending machine not found"}), 404
    db.session.delete(vm)
    db.session.commit()
    return jsonify({'message': 'Vending Machine deleted successfully'}), 200


# Create item in vending machine
def create_item(vm_id: int):
    '''
    Create an item in the vending machine stock.

    Args:
        vm_id: The id of the vending machine.

    Returns:
        A message indicating the item was created.

    Raises:
        400: If the name, price, or quantity are missing.
        404: If the vending machine is not found.
        500: If an error occurs.

    '''
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
def add_item_stock(vm_id: int, item_id: int):
    '''
    Add quantity to an item in the vending machine stock.

    Args:
        vm_id: The id of the vending machine.
        item_id: The id of the item.

    Returns:
        A message indicating the item stock was added.

    Raises:
        404: If the vending machine or item is not found.
        500: If an error occurs.


    '''
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
def edit_item_stock(vm_id: int, item_id: int):
    '''
    Edit the quantity of an item in the vending machine stock.
    
    Args:
        vm_id: The id of the vending machine.
        item_id: The id of the item.

    Returns:
        A message indicating the item stock was updated.
    '''
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
def remove_item_from_stock(vm_id: int, item_id: int):
    '''
    Remove an item from the vending machine stock.

    Args:
        vm_id: The id of the vending machine.
        item_id: The id of the item.

    Returns:
        A message indicating the item was removed from stock.
    ''' 
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
def get_stock_by_vm(vm_id: int):
    '''
    Retrieve all items in a vending machine and return them as a list of dictionaries.

    Args:
        vm_id: The id of the vending machine.

    Returns:
        A list of dictionaries containing the item id, name, price and quantity.

    '''
    vm = VendingMachine.query.get(vm_id)
    if not vm:
        return jsonify({'message': 'Vending Machine not found, please call the correct ID'})
    items = [{'id': item.id, 'name': item.name, 'price': item.price, 'quantity': item.quantity} for item in
             vm.items]
    return jsonify(items)


# Get all Vending Machine
def view_vm():
    '''
    Get all vending machines in the database and return them as a list of dictionaries.

    Returns:
        A list of dictionaries containing the vending machine id, name and location.
    
    '''
    vending_machines = VendingMachine.query.all()
    vm_lst = [{'id': vm.id, 'name': vm.name, 'location': vm.location} for vm in vending_machines]
    if not vm_lst:
        return jsonify({'message': 'No Vending Machine found'})
    return jsonify(vm_lst)
