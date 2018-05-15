#! /usr/bin/env python3
# coding: utf-8

import requests
import json, math


current_page = "1"

url_categorie = "https://fr.openfoodfacts.org/categorie/lentilles-preparees/"

r = requests.get(url_categorie+current_page+".json")

#~ json_categorie = json.loads(r.text)

json_categorie =r.json()
        

product_count = json_categorie["count"]

nb_pages = int(math.ceil(product_count / json_categorie["page_size"]))

print("There are "+str(nb_pages)+" pages")

#~ for product in json_categorie["products"]:
    #~ print (product["product_name"])

for page in range(0, nb_pages):
    r = requests.get(url_categorie+str(page+1)+".json")
    json_categorie = json.loads(r.text)
    print ("\n -Displaying products of page "+str(page+1))
    
    for product in json_categorie["products"]:
        try:
            str_nutr_grade = product["nutrition_grade_fr"]
        except KeyError:
            str_nutr_grade = "N/A"
        print (product["product_name"]+" with a score of "+str_nutr_grade.upper())
