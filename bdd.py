#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module used to handle interactions with the database and display functions
in the openfoodfact project
"""
import sys
import math
import mysql.connector
import requests

ROWS_PER_PAGE = 40

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
    Prints a given page of products for a given category
    """
    number_of_rows = get_number_products(category_id)
    total_pages = get_number_pages(category_id)
    products = get_products_page(category_id, page)

    if len(products) == 0:
        print("Aucun résultat")
    else:
        display_str = '\nAffichage des résultats {} à {} sur {} (Page {} sur {}):'
        print(display_str.format((((page-1)*ROWS_PER_PAGE)+1),
                                 (((page-1)*ROWS_PER_PAGE)+len(products)),
                                 number_of_rows, page, total_pages))

        format_string = '{0:>3} |{1:<110}| {2}'
        print(format_string.format("Num", "Produit - Marque", "Lien Openfoodfacts"))
        print('='*170)

        #~ Using enumerate to get index of the loop displayed as choice
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

def get_category_url(category_id):
    """
    Request url from the database for a given category
    """
    conn = mysql.connector.connect(**CONNECTION_PARAMETERS)
    cursor = conn.cursor()
    cursor.execute("""SELECT link_openfoodfacts FROM category WHERE category_id = %s""",
                   (category_id,))
    (url,) = cursor.fetchone()
    conn.close()
    return url

def request_json(category_id):
    """
    This function requests json of products on openfoodfacts for a given category
    and returns a list of data
    """
    url_category = get_category_url(category_id)
    json_categorie = requests.get(url_category+"1.json").json()

    #~ Number of pages calculated with count of products / product displayed per page
    nb_pages = int(math.ceil(json_categorie["count"] / json_categorie["page_size"]))

    data = []
    current_product = 0

    for page in range(0, nb_pages):
        json_categorie = requests.get(url_category+str(page+1)+".json").json()

        #~ print("-Requesting products of page "+str(page+1)+" out of "+str(nb_pages))
        #~ print_progress(page+1, nb_pages, decimals = 0)
        for product in json_categorie["products"]:
            print_progress(current_product, json_categorie["count"], decimals=0)
            try:
                str_nutr_grade = product["nutrition_grade_fr"]
                nutriscore = list(NUTRISCORE.keys())[
                    list(NUTRISCORE.values()).index(str_nutr_grade.upper())]
            except KeyError:
                str_nutr_grade = "N/A"
                nutriscore = 0
            try:
                if product["stores"] == "":
                    stores = None
                else:
                    stores = product["stores"]
            except KeyError:
                stores = None

            try:
                desc = product["generic_name"]
            except KeyError:
                desc = ""
                try:
                    desc = product["ingredients_text"]
                except KeyError:
                    desc = ""


            link = "https://fr.openfoodfacts.org/produit/"+str(product["code"])

            data.append((
                product["product_name"],
                category_id,
                nutriscore,
                desc,
                stores,
                link,
                False,
                product["brands"]
            ))

            current_product += 1
    return data

def insert_db(category_id):
    """
    Inserts into database the result of json query of the openfoodfacts site
    """
    data = request_json(category_id)

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

def get_product(category_id, page, index):
    """
    Request a single product for a given category at the given page
    returns a list with the following information :
    product_id, product_name, category_id, product_brand, nutriscore, description,
    store, link_openfoodfacts, saved
    """
    conn = mysql.connector.connect(**CONNECTION_PARAMETERS)
    cursor = conn.cursor()

    #~ Get results
    cursor.execute("""SELECT * FROM product WHERE category_id = %s
                    ORDER BY product_id ASC
                    LIMIT 1 OFFSET %s""", (category_id, (index-1+(page-1)*ROWS_PER_PAGE)))
    row = cursor.fetchone()

    conn.close()
    return row

def get_best_score_category(category_id):
    """
    Returns the best available nutriscore for a given category
    """
    conn = mysql.connector.connect(**CONNECTION_PARAMETERS)
    cursor = conn.cursor()
    cursor.execute("""SELECT MIN(nutriscore) FROM product
                      WHERE category_id = %s AND nutriscore !=  0 """, (category_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0]

def get_alternative(product_id):
    """
    Request a single product with a nutriscore better than the given one
    returns a list with the following information :
    product_id, product_name, category_id, product_brand, nutriscore, description,
    store, link_openfoodfacts, saved
    returns None if no alternative available
    """
    conn = mysql.connector.connect(**CONNECTION_PARAMETERS)
    cursor = conn.cursor()
    cursor.execute("""SELECT nutriscore, category_id FROM product
                      WHERE product_id =  %s """, (product_id,))
    row = cursor.fetchone()
    category_id = row[1]
    best_score = get_best_score_category(category_id)

    #~ Try to get a better product with a store
    cursor.execute("""SELECT * FROM product
                      WHERE nutriscore = %s
                      AND category_id = %s
                      AND product_id != %s
                      AND store IS NOT NULL
                      ORDER BY product_id ASC
                      LIMIT 1""",
                   (best_score, category_id, product_id))
    result = cursor.fetchone()
    #~ if no result, get a product without a store:
    if not result:
        cursor.execute("""SELECT * FROM product
                          WHERE nutriscore = %s
                          AND category_id = %s
                          AND product_id != %s
                          ORDER BY product_id ASC
                          LIMIT 1""",
                       (best_score, category_id, product_id))
        result = cursor.fetchone()
    conn.close()

    return result

def get_saved_products():
    """
    Request saved products from the database and returns a list of products
    """
    conn = mysql.connector.connect(**CONNECTION_PARAMETERS)
    cursor = conn.cursor()
    cursor.execute("""SELECT category_name, product_name, product_brand, nutriscore,
                      product.link_openfoodfacts, store
                      FROM product  INNER JOIN category
                      ON category.category_id = product.category_id
                      WHERE saved = true
                      ORDER BY category.category_id""")
    saved_products = cursor.fetchall()
    conn.close()
    return saved_products

def get_str_saved():
    """
    Returns string with all saved products formatted
    """
    format_string = '{0:30} | {1:50} | {2:^10} | {3:50} | {4}  \n'
    res = format_string.format('Catégorie', 'Produit - Marque', 'Nutriscore', 'Lien', 'Magasin')
    res += '='*170
    res += '\n'
    for product in get_saved_products():

        if not product[5]:
            store = "Information non disponible"
        else:
            store = product[5]

        res += (format_string.format(product[0], product[1]+' - '+product[2],
                                     NUTRISCORE[product[3]], product[4], store))
    return res

def save_product(product_id):
    """
    Change saved column on table product in database for given product_id
    """
    conn = mysql.connector.connect(**CONNECTION_PARAMETERS)
    cursor = conn.cursor()
    cursor.execute("""UPDATE product
                      SET saved = TRUE
                      WHERE product_id = %s """,
                   (product_id,))
    conn.commit()
    conn.close()
    return

def clear_products():
    """
    Clears the database of all products. Used for maintenance only.
    """
    conn = mysql.connector.connect(**CONNECTION_PARAMETERS)
    cursor = conn.cursor()
    print("Clearing table product")
    try:
        cursor.execute("""TRUNCATE TABLE product""")
        cursor.execute("""ALTER TABLE product AUTO_INCREMENT = 1""")
    except mysql.connector.Error as err:
        print("Failed clearing table: {}".format(err))

    conn.commit()
    conn.close()
    print("Table cleared")

def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

