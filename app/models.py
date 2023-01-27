from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class VendingMachine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    location = db.Column(db.String(50))


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    vending_machine_id = db.Column(db.Integer, db.ForeignKey('vending_machine.id'))
    vending_machine = db.relationship("VendingMachine", back_populates="items")


VendingMachine.items = db.relationship("Item", order_by=Item.id, back_populates="vending_machine")
