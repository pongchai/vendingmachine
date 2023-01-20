from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'identifier.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Init db
db = SQLAlchemy(app)


class VendingMachine(db.Model):
    """
    A Class to represent Vending Machine Object

    Attributes
    ----------
    id : int
        the identification of each Vending Machine
    name: String
        name of each Vending Machine
    location: String
        location of each Vending Machine
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    location = db.Column(db.String(50))


class Item(db.Model):
    """
    A Class to represent Item

    Attributes
    ----------
    id : int
        the identification of each Item
    name: String
        name of each Item
    price: Float
        price of each Item
    quantity: Int
        quantity of each Item
    vending_machine_id : vending_machine.id
        link of vending machine id where relationship with the item
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    vending_machine_id = db.Column(db.Integer, db.ForeignKey('vending_machine.id'))
    vending_machine = db.relationship("VendingMachine", back_populates="items")


VendingMachine.items = db.relationship("Item", order_by=Item.id, back_populates="vending_machine")


# Create a vending machine
@app.route('/create_vm', methods=['POST'])
def create_vm():
    name = request.json['name']
    location = request.json['location']
    vm = VendingMachine(name=name, location=location)
    db.session.add(vm)
    db.session.commit()
    return jsonify({'message': 'Vending Machine created successfully'})


# Delete vending machine
@app.route('/delete_vm/<int:id>', methods=['DELETE'])
def delete_vm(id):
    vm = VendingMachine.query.get(id)
    db.session.delete(vm)
    db.session.commit()
    return jsonify({'message': 'Vending Machine deleted successfully'})


# Create item in vending machine
@app.route('/create_item/<int:vm_id>', methods=['POST'])
def create_item(vm_id):
    name = request.json['name']
    price = request.json['price']
    quantity = request.json['quantity']
    vm = VendingMachine.query.get(vm_id)
    item = Item(name=name, price=price, quantity=quantity, vending_machine=vm)
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Item created successfully'})


# Add product to the vending machine
@app.route('/add_item_to_stock/<int:vm_id>/<int:item_id>', methods=['PUT'])
def add_item_to_stock(vm_id, item_id):
    quantity = request.json['quantity']
    vm = VendingMachine.query.get(vm_id)
    if vm:
        item = Item.query.get(item_id)
        if item:
            item.quantity += quantity
            db.session.commit()
            return jsonify({'message': 'Item stock added successfully'})
        else:
            return jsonify({'message': 'Item not found'}), 404
    else:
        return jsonify({'message': 'Vending Machine not found'}), 404


# Edit stock
@app.route('/edit_item_stock/<int:vm_id>/<int:item_id>', methods=['PUT'])
def edit_item_stock(vm_id, item_id):
    quantity = request.json['quantity']
    vm = VendingMachine.query.get(vm_id)
    if vm:
        item = Item.query.get(item_id)
        if item:
            item.quantity = quantity
            db.session.commit()
            return jsonify({'message': 'Item stock updated successfully'})
        else:
            return jsonify({'message': 'Item not found'}), 404
    else:
        return jsonify({'message': 'Vending Machine not found'}), 404


# Remove item
@app.route('/remove_item_from_stock/<int:vm_id>/<int:item_id>', methods=['PUT'])
def remove_item_from_stock(vm_id, item_id):
    quantity = request.json['quantity']
    vm = VendingMachine.query.get(vm_id)
    if vm:
        item = Item.query.get(item_id)
        if item:
            if item.quantity - quantity < 0:
                return jsonify({"error": "Not enough items in stock"}), 400
            else:
                item.quantity = item.quantity - quantity
                db.session.commit()
                return jsonify({"message": "Item removed from stock"}), 200
        else:
            return jsonify({"error": "Item not found"}), 404
    else:
        return jsonify({"error": "Vending machine not found"}), 404


# Get Item in Vending Machine
@app.route('/get_vending_machines_items/<int:vm_id>', methods=['GET'])
def get_stock_by_vm(vm_id):
    vm = VendingMachine.query.get(vm_id)
    if vm:
        items = vm.items
        items_lst = []
        for item in items:
            items_lst.append({'id': item.id, 'name': item.name, 'price': item.price, 'quantity': item.quantity})
        return jsonify(items_lst)
    else:
        return jsonify({'message': 'Vending Machine not found, please call the correct ID'})


# Get all Vending Machine
@app.route('/get_vending_machines', methods=['GET'])
def view_vm():
    vending_machines = VendingMachine.query.all()
    vm_lst = []
    for vm in vending_machines:
        vm_lst.append({'id': vm.id, 'name': vm.name, 'location': vm.location})
    return jsonify(vm_lst)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
