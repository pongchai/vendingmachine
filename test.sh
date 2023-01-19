#!/bin/bash

curl -X POST -H "Content-Type: application/json" -d '{"name": "Vending Machine 1", "location": "A343"}' http://localhost:5000/create_vm
