#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
import os
#~ import mysql.connector
import bdd 

def clear_and_print(txtmenu, txtchoice=False):
    os.system('cls||clear')
    print(txtmenu)
    if txtchoice:
        print(txtchoice)
    return
    
def select_product(rows, choice_int):
    text_choice = ("Vous avez choisi la catégorie numéro "+str(rows[choice_int][0])+
               " : "+str(rows[choice_int][1]))
    clear_and_print(text_choice)
    bdd.display_products_page(rows[choice_int][0], 1)
    #~ conn = mysql.connector.connect(host="localhost",user="cocomo",password="password", database="openfoodfacts")
    #~ cursor = conn.cursor()

    #~ cursor.execute("""SELECT product_id, product_name, product_brand, 
                    #~ nutriscore FROM product WHERE product_id <= %s 
                    #~ AND category_id = %s""", ("20", str(rows[choice_int][0])))
    #~ rows = cursor.fetchall()
    
    #~ for row in rows:
        #~ print('{0} : {1} - {2} nutriscore : {3}'.format(row[0], row[1], row[2], row[3]))


    #~ conn.close()
    return

def select_category():

    txt_menu_cat = ("Selectionnez votre catégorie d'aliment à l'aide du numéro, Q pour quitter, "+
                 "M pour revenir au menu principal:\n")

    categories = bdd.get_categories()
    for category in categories:
        txt_menu_cat += ('{0} : {1} - {2}\n'.format(category[0], category[1], category[2]))
    clear_and_print(txt_menu_cat)

    user_choice = input(">>")

    while user_choice != 'q' and user_choice != 'm' and user_choice != 'Q' and user_choice != 'M':
        try:
            choice_int = int(user_choice)-1

            if 0 <= choice_int < len(categories):
                #~ Correct choice, handle the chosen category
                select_product(categories, choice_int)
            else:
                clear_and_print(txt_menu_cat, "Le nombre choisi n'est pas dans la liste")

        except ValueError:
            error = ("Choix non reconnu, veuillez entrer un nombre, ou Q pour quitter, "+
                   "M pour revenir au menu principal")
            clear_and_print(txt_menu_cat, error)

        user_choice = input(">>")
    return user_choice

def menu_principal():

    txt_menu1 = ("Selectionnez votre choix à l'aide du numéro, Q pour quitter:\n"+
                 "1 - Quel aliment souhaitez-vous remplacer ?\n"+
                 "2 - Retrouver mes aliments substitués.\n")

    clear_and_print(txt_menu1)
    user_choice = input(">>")

    while user_choice != 'q' and user_choice != 'Q':

        if user_choice == '1':
            #~ Demander la catégorie
            user_choice = select_category()
            clear_and_print(txt_menu1)

        elif user_choice == '2':
            #~ Retrouver les aliments substitués
            clear_and_print(txt_menu1, 'Choix 2')

        else:
            clear_and_print(txt_menu1, 'Choix non reconnu')

        if user_choice != 'q' and user_choice != 'Q':

            user_choice = input(">>")


def main(args):

    menu_principal()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
