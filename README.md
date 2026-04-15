# Art Gallery Management System

A full-stack, command-line application designed to manage an art gallery's inventory, visitor logs, and customer orders. Built with Python and MySQL, this system demonstrates relational database management, role-based access control, and binary file handling.

## Features
* **Role-Based Access:** Distinct terminal interfaces for Admins, Visitors, and Customers.
* **Inventory Management (Admin):** Full CRUD capabilities to add, edit, delete, and update the status of artworks.
* **Binary File Storage:** Converts local image files into base64 encoded strings for secure storage as BLOBs within the MySQL database, enabling image retrieval directly from the terminal.
* **Customer Portal:** Allows users to register accounts, view available inventory, and place orders. 

## Tech Stack
* **Language:** Python 3
* **Database:** MySQL
* **Libraries:** `mysql-connector-python`, `Pillow` (PIL), `pandas`, `tabulate`

## System Architecture
The application utilizes a relational database (`artgallary`) consisting of three primary tables:
1. `artwork`: Stores inventory details, pricing, and binary image data.
2. `visitor`: Logs guest access and timestamps.
3. `orders`: Tracks customer purchases, billing details, and transaction histories.
