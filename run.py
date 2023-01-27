from flask import Flask
from config import Config
from app.models import db
from app.routes import create_vm, delete_vm, create_item, add_item_stock, edit_item_stock, remove_item_from_stock, get_stock_by_vm, view_vm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.add_url_rule('/vending-machines', view_func=create_vm, methods=['POST'])
app.add_url_rule('/vending-machines/<int:vm_id>', view_func=delete_vm, methods=['DELETE'])
app.add_url_rule('/create_item/<int:vm_id>', view_func=create_item, methods=['POST'])
app.add_url_rule('/add_item_stock/<int:vm_id>/<int:item_id>', view_func=add_item_stock, methods=['PUT'])
app.add_url_rule('/edit_item_stock/<int:vm_id>/<int:item_id>', view_func=edit_item_stock, methods=['PUT'])
app.add_url_rule('/remove_item_from_stock/<int:vm_id>/<int:item_id>', view_func=remove_item_from_stock, methods=['PUT'])
app.add_url_rule('/view_items_in_vending_machine/<int:vm_id>', view_func=get_stock_by_vm, methods=['GET'])
app.add_url_rule('/get_vending_machines', view_func=view_vm, methods=['GET'])

if __name__ == '__main__':
    app.run()
