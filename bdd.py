#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector 

conn = mysql.connector.connect(host="localhost",user="cocomo",password="password", database="openfoodfacts")
cursor = conn.cursor()



cursor.execute("""SELECT * FROM category""")
rows = cursor.fetchall()
for row in rows:
    print('{0} : {1} - {2}'.format(row[0], row[1], row[2]))


cursor.execute("""SELECT product_id, product_name, nutriscore FROM product WHERE product_id = %s""", ("1", ))
rows = cursor.fetchall()
for row in rows:
    print('{0} : {1} - {2}'.format(row[0], row[1], row[2]))



conn.close()
