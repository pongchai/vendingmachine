#!/bin/bash


# Command for testing the API

# Create VM
curl -X POST -H "Content-Type: application/json" -d '{"name": "Vending Machine 1", "location": "A343"}' http://localhost:5000/create_vm
# Delete VM ID 1
curl -X DELETE http://localhost:5000/delete_vm/1
# Create Item in VM id 1
curl -X POST -H "Content-Type: application/json" -d '{"name": "Chips", "price": 2.5, "quantity": 10}' http://localhost:5000/create_item/1
# Add Item to stock
curl -X PUT -H "Content-Type: application/json" -d '{"quantity": 5}' http://localhost:5000/add_item_to_stock/1/1
# Edit Item stock
curl -X PUT -H "Content-Type: application/json" -d '{"quantity": 5}' http://localhost:5000/edit_item_stock/1/1
# Get All Vending Machine
curl -X GET http://localhost:5000/get_vending_machines
# Get All Stock Information By Vending Machine ID
curl -X GET http://localhost:5000/view_items_in_vending_machine/1
