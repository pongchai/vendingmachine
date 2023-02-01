[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=pongchai_vendingmachine&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=pongchai_vendingmachine)
[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-white.svg)](https://sonarcloud.io/summary/new_code?id=pongchai_vendingmachine)

# Vending Machine API

This API allows for creation, deletion, and management of vending machines around MUIC and the items. It uses Flask and
SQLAlchemy to handle to routes and database management.

## Setup

1. Clone the repository to your local machine
2. Install the required packages by running `pip3 install -r requirement.txt`.
3. Setup SQLite Database and Execute SQL command found in SQLSetup.sql
4. Run the app with `python3 app.py`.

### Endpoints

### Vending Machine Endpoints

- POST /vending-machines : creates a new vending machine.
- DELETE /vending-machines/id> : deletes a vending machine by its ID.
- GET /get_vending_machines : retrieves a list of all vending machines.

### Item Endpoints

- POST /create_item/id : creates a new item and assigns it to a vending machine by its ID.
- PUT /add_item_stock/id/item_id : adds stock for a specific item in a specific vending machine.
- PUT /edit_item_stock/id/item_id : edit stock for a specific item in a specific vending machine.
- PUT /remove_item_from_stock/id/item_id : remove an item from stock for a specific vending machine.
- GET /view_items_in_vending_machine/id : retrieve list of items in a specific vending machine.

### Note

- Replace <int:id>, <int:vm_id> and <int:item_id> with the actual id in the url when making requests
- If any Vending Machine or Item is not found, API will return 404 with the message "Vending Machine not found" or "Item
  not found" respectively.
