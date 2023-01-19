# Vending Machine API 
This API allows for creation, deletion, and management of vending machines around MUIC and the items. It uses Flask and SQLAlchemy to handle to routes and database management.

## Setup
1. Clone the repository to your local machine 
2. Install the required packages by running `pip install -r requirement.txt`.
3. Setup SQLite Database and Run SQL command found in SQLsetup.py
4. Run the app with `python3 app.py` or `python app.py`.

### Endpoints 
#### Create Vending Machine 
- Route `/create_vm`
- Method: `POST`
- Request Body: 

`{
    "name": "Vending Machine 1",
    "location": "Room A334"
}`
- Response: 
`{
  "message": "Vending Machine created successfully"  
}`

#### Delete Vending Machine 
- Route `/delete_vm/id`
- Method: `DELETE`
- Request Body: 
`{ "message" : "Vending Machine deleted successfully"
}`

#### Create Item
- Route `/create_item/vm_id`
- Method `POST`
- Request Body:
`{ "message" : "Item created successfully" }`
#### Add Item to Stock
- Route `/add_item_to_stock/vm_id/item_id`
- Method `PUT`
- Request Body:
`{"quantity" : 5}`
- Response `{ "message", "Item stock added successfully"}`
#### Edit Item Stock 
- Route `/edit_item_stock/vm_id/item_id`
- Method: `PUT`
- Request Body: `{ "quantity": 5}`
- Response `{"message": "Item stock updated successfully"}`
### Note
- Replace <int:id>, <int:vm_id> and <int:item_id> with the actual id in the url when making requests
- If any Vending Machine or Item is not found, API will return 404 with the message "Vending Machine not found" or "Item not found" respectively.

