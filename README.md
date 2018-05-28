# P5-Openfoodfacts

# Pre requisite 
Python 3 and MySQL must be installed on the OS.

# Environnement installation
Install the required files with:
`pip install -r requirements.txt`

Create the database with the command: 
`mysql -h localhost -u [user] openfoodfacts < path/to/openfoodfact.sql`

# How to use the application
Launch the application with : 
`python3 main.py`

Navigate the menus with the numbers, choose a category, request the Open Food Fact site to get products for this category if there are none. Then choose a product to get an alternative with a better nutriscore from Open Food Facts. You can save the alternative and access all saved alternative from the main menu later.
Use M to get to the previous menu or Q to quit at any time.
