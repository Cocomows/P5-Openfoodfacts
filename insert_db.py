#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DOCSTRING
This module is used to handle interactions with the database
"""

import math
import mysql.connector
import requests


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

    conn = mysql.connector.connect(host="localhost", user="cocomo", password="password",
                                   database="openfoodfacts")
    cursor = conn.cursor()

    stmt = """INSERT INTO product (product_name, category_id, nutriscore, description, store,
            link_openfoodfacts, saved, product_brand)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

    cursor.executemany(stmt, data)
    print("Lignes correctement insérées")

    conn.commit()
    cursor.close()
    conn.close()

insert_db("https://fr.openfoodfacts.org/categorie/pates-a-tartiner-aux-noisettes/", 1)
