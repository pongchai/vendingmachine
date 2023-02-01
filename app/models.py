from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Create a SQLAlchemy instance


# Create a VendingMachine model
class VendingMachine(db.Model):
    '''
    Vending Machine model responsible for storing the vending machine data.

    Attributes:
        id: The id of the vending machine.
        name: The name of the vending machine.
        location: The location of the vending machine.
        items: The items in the vending machine.

    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    location = db.Column(db.String(50))


# Create an Item model
class Item(db.Model):
    ''' 
    Item model responsible for storing the item data.
    
    Attributes:
        id: The id of the item.
        name: The name of the item.
        price: The price of the item.
        quantity: The quantity of the item.
        vending_machine_id: The id of the vending machine.
        vending_machine: The vending machine the item belongs to.
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    vending_machine_id = db.Column(db.Integer, db.ForeignKey('vending_machine.id'))
    vending_machine = db.relationship("VendingMachine", back_populates="items")


VendingMachine.items = db.relationship("Item", order_by=Item.id,
                                       back_populates="vending_machine")  # Create a relationship between the VendingMachine and Item models
