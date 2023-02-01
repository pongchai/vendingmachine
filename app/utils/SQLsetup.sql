-- execute the following for complete setup of the database
.tables
 .schema vending_machine
 CREATE TABLE vending_machine (
         id INTEGER NOT NULL,
         name VARCHAR(50),
         location VARCHAR(50),
         PRIMARY KEY (id)
 );
 .schema item
 CREATE TABLE item (
         id INTEGER NOT NULL,
         name VARCHAR(50),
         price FLOAT,
         quantity INTEGER,
         vending_machine_id INTEGER,
         FOREIGN KEY(vending_machine_id) REFERENCES vending_machine (id),
         PRIMARY KEY (id)
 );
INSERT INTO item (name, price,quantity,vending_machine_id) VALUES ('item1', 2.5, 10,1)
