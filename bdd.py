#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module used to handle interactions with the database and display functions
in the openfoodfact project
"""
import math
import mysql.connector
import requests

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

def print_products_page(category_id, page):
    """
    Print products of a given category
    """
    number_of_rows = get_number_products(category_id)
    total_pages = get_number_pages(category_id)
    products = get_products_page(category_id, page)

    if len(products) == 0:
        print("Aucun résultat")
        #~ Add option to fill database with results from site
    else:
        display_str = '\nDisplaying results {} to {} out of {} (Page {} out of {}):'
        print(display_str.format(products[0][0], (products[0][0]+len(products)-1),
                                 number_of_rows, page, total_pages))

        format_string = '{0:>3} |{1:<110}| {2}'
        print(format_string.format("Num", "Produit - Marque", "Lien Openfoodfacts"))
        print('='*170)


        for index, product in enumerate(products, start=1):
            product_fullname = str(product[1])+" - "+str(product[2])
            print(format_string.format(index, product_fullname, product[4]))

    return

def get_products_page(category_id, page):
    """
    Request products for a given category at the given page
    returns a list of products with the following information :
    product_id, product_name, product_brand, nutriscore,link_openfoodfacts
    """
    conn = mysql.connector.connect(**CONNECTION_PARAMETERS)
    cursor = conn.cursor()

    offset = (page-1)*ROWS_PER_PAGE
    #~ Get results
    cursor.execute("""SELECT product_id, product_name, product_brand,
                    nutriscore,link_openfoodfacts FROM product WHERE category_id = %s
                    ORDER BY product_id ASC
                    LIMIT %s OFFSET %s""", (category_id, ROWS_PER_PAGE, offset))
    rows = cursor.fetchall()

    conn.close()
    return rows



def get_number_products(category_id):
    """
    Request all products for a given category from the database
    and returns number of rows
    """
    conn = mysql.connector.connect(**CONNECTION_PARAMETERS)
    cursor = conn.cursor()
    #~ Get total number of rows
    cursor.execute("SELECT COUNT(*) from product where category_id = %s", (category_id,))
    (number_of_rows,) = cursor.fetchone()
    conn.close()
    return number_of_rows

def get_number_pages(category_id):
    """
    Gets the number of rows for a product and return number of pages with const ROW_PER_PAGE
    """
    return int(math.ceil(get_number_products(category_id) / ROWS_PER_PAGE))

def str_categories():
    """
    Returns string with categories formatted
    """
    str_cat = ''
    for category in get_categories():
        str_cat += ('{0:02} | {1:30} | {2}\n'.format(category[0], category[1], category[2]))
    return str_cat

def get_categories():
    """
    Request categories from the database and returns a list of categories
    """
    conn = mysql.connector.connect(**CONNECTION_PARAMETERS)
    cursor = conn.cursor()

    #~ Display all available categories from the database
    cursor.execute("""SELECT * FROM category""")
    categories = cursor.fetchall()
    conn.close()
    return categories


def insert_db(url_categorie, categorie_id):
    """This function add products in database for a given category"""

    json_categorie = requests.get(url_categorie+"1.json").json()

    #~ Number of pages calculated with count of products / product displayed per page
    nb_pages = int(math.ceil(json_categorie["count"] / json_categorie["page_size"]))

    data = []


    for page in range(0, nb_pages):
        json_categorie = requests.get(url_categorie+str(page+1)+".json").json()

        print("-Requesting products of page "+str(page+1)+" out of "+str(nb_pages))

        for product in json_categorie["products"]:
            try:
                str_nutr_grade = product["nutrition_grade_fr"]
                if str_nutr_grade == 'a':
                    nutriscore = 1
                if str_nutr_grade == 'b':
                    nutriscore = 2
                if str_nutr_grade == 'c':
                    nutriscore = 3
                if str_nutr_grade == 'd':
                    nutriscore = 4
                if str_nutr_grade == 'e':
                    nutriscore = 5
            except KeyError:
                str_nutr_grade = "N/A"
                nutriscore = 0

            if product["stores"] == "":
                stores = "N/A"
            else:
                stores = product["stores"]

            link = "https://fr.openfoodfacts.org/produit/"+str(product["code"])

            data.append((
                product["product_name"],
                categorie_id,
                nutriscore,
                product["ingredients_text"],
                stores,
                link,
                None,
                product["brands"]
            ))

    conn = mysql.connector.connect(**CONNECTION_PARAMETERS)
    cursor = conn.cursor()

    stmt = """INSERT INTO product (product_name, category_id, nutriscore, description, store,
            link_openfoodfacts, saved, product_brand)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

    cursor.executemany(stmt, data)
    print("Lignes correctement insérées")

    conn.commit()
    cursor.close()
    conn.close()


def get_product(category_id, index):
    """
    Request products for a given category at the given page
    returns a list of products with the following information :
    product_id, product_name, product_brand, nutriscore,link_openfoodfacts
    """
    conn = mysql.connector.connect(**CONNECTION_PARAMETERS)
    cursor = conn.cursor()

    #~ Get results
    cursor.execute("""SELECT product_id, product_name, product_brand,
                    nutriscore,link_openfoodfacts FROM product WHERE category_id = %s
                    ORDER BY product_id ASC
                    LIMIT 1 OFFSET %s""", (category_id, index-1))
    rows = cursor.fetchall()

    conn.close()
    return rows

#~ print(get_product(1,6))

