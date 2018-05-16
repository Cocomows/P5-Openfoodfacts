#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import mysql.connector

ROWS_PER_PAGE = 30
NUTRISCORE = {
              0: 'N/A',
              1: 'A',
              2: 'B',
              3: 'C',
              4: 'D',
              5: 'E'
            }
CONNECTION_PARAMETERS = {
                        "host": "localhost",
                        "user": "cocomo",
                        "password": "password", 
                        "database": "openfoodfacts"
                        }

def display_products_page(category_id, page):
    conn = mysql.connector.connect(**CONNECTION_PARAMETERS)
    cursor = conn.cursor()

    #~ Get total number of rows
    number_of_rows, total_pages = get_row_and_pages(category_id)
    
    offset = (page-1)*ROWS_PER_PAGE
    #~ Get results
    cursor.execute("""SELECT product_id, product_name, product_brand,
                    nutriscore,link_openfoodfacts FROM product WHERE category_id = %s
                    ORDER BY product_id ASC LIMIT %s OFFSET %s""", (category_id, ROWS_PER_PAGE, offset))
    rows = cursor.fetchall()

    if len(rows) == 0:
        print("Aucun résultat")
    else:
        display_str = '\n\nDisplaying results {} to {} out of {} (Page {} out of {})\n'
        print(display_str.format(rows[0][0],(rows[0][0]+len(rows)-1),number_of_rows,page,total_pages))

        format_string = '{0:0>3} |{1:70}|{2:70}| {3:5} | {4}'
        print(format_string.format(" ID", "Produit", "Marque", "Score","Lien"))
        print('_'*190)

        for row in rows:
            print(format_string.format(row[0], row[1], row[2], NUTRISCORE[row[3]], row[4]))

    conn.close()
    return

def get_row_and_pages(category_id):
    conn = mysql.connector.connect(**CONNECTION_PARAMETERS)
    cursor = conn.cursor()
    #~ Get total number of rows
    cursor.execute("SELECT COUNT(*) from product where category_id = %s",(category_id,))
    (number_of_rows,)=cursor.fetchone()
    conn.close()
    total_pages = int(math.ceil(number_of_rows / ROWS_PER_PAGE))
    return number_of_rows, total_pages


def get_categories():
    conn = mysql.connector.connect(**CONNECTION_PARAMETERS)
    cursor = conn.cursor()
    
    #~ Display all available categories from the database
    cursor.execute("""SELECT * FROM category""")
    categories = cursor.fetchall()
    return categories

