#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
import os
#~ import mysql.connector
from bdd import *

def clear_and_print(txtmenu, txtchoice=False):
    os.system('cls||clear')
    print(txtmenu)
    if txtchoice:
        print(txtchoice)
    return

def pretty_print_product(product):
    str_product = """
Produit             : {}
Marque              : {}
Description         : {}
Nutriscore          : {}
En vente chez       : {}
Lien openfoodfacts  : {}
    """
    if not product[6]:
        store = "Information non disponible"
    else:
        store = product[6]
    print(str_product.format(product[1], product[3], product[5], NUTRISCORE[product[4]],
                             store, product[7]))


def display_alternative_product(choice_int, category_id, page):

    product_info = get_product(category_id, page, choice_int)
    nutriscore_int = product_info[4]
    clear_and_print("Vous avez choisi le produit suivant :")
    pretty_print_product(product_info)
    if nutriscore_int != 0:
        print("Ce produit a un nutriscore de {}\n".format(NUTRISCORE[nutriscore_int]))
        if nutriscore_int == get_best_score_category(category_id):
            print("Félicitations, votre produit possède déjà le meilleur score de sa catégorie !")
            if(get_alternative(product_info[0])):
                print("Un autre produit de la même catégorie"+
                      "avec un score identique pourrait être :")
                pretty_print_product(get_alternative(product_info[0]))
            else:
                print("Il n'y a pas d'autre produit dans cette catégorie avec un score identique")
        else:
            print("Voici une alternative à votre produit avec un meilleur nutriscore : ")
            pretty_print_product(get_alternative(product_info[0]))

    else:
        print("Le nutriscore du produit que vous avez sélectionné n'est pas renseigné.\n")
        print("Voici un produit de la même catégorie avec le meilleur nutriscore possible :")
        pretty_print_product(get_alternative(product_info[0]))

    return

def filldatabase_menu(text_choice, category_txt, category_id):
    text_choice += ("\nIl n'y a pas de produits pour cette catégorie, voulez-vous requêter"+
                    " le site openfoodfacts pour les produits de la catégorie "+
                    category_txt+
                    " ?\n[O]ui pour requêter le site ou [N]on pour revenir au menu précédent")
    clear_and_print(text_choice)
    user_choice = input(">>")
    while True:
        if user_choice.lower() == 'q' or user_choice.lower() == 'm':
            break
        elif user_choice.lower() == 'n':
            return 'm'
        elif user_choice.lower() == 'o':
            clear_and_print("Addition à la base de données des produits de la catégorie : "+
                            str(category_id))
            insert_db(category_id)
            return 'm'
        else:
            clear_and_print(text_choice)
            print("Choix non reconnu")
        user_choice = input(">>")
    return user_choice

def display_next_page(page, total_pages, text_choice, category_id):
    if page+1 <= total_pages:
        page += 1
        clear_and_print(text_choice)
        print_products_page(category_id, page)
    else:
        clear_and_print(text_choice)
        print_products_page(category_id, page)
        print("Dernière page atteinte")
    return page

def display_previous_page(page, total_pages, text_choice, category_id):
    if page-1 > 0:
        page -= 1
        clear_and_print(text_choice)
        print_products_page(category_id, page)
    else:
        clear_and_print(text_choice)
        print_products_page(category_id, page)
        print("Première page atteinte")
    return page

def display_pages(text_choice, category_id):
    page = 1
    total_pages = get_number_pages(category_id)
    if total_pages > 1:
        text_choice += ("\nNavigation avec (B)ack et (N)ext pour la pagination")

    clear_and_print(text_choice)
    print_products_page(category_id, page)

    user_choice = input(">>")
    while True:
        if user_choice.lower() == 'q' or user_choice.lower() == 'm':
            break
        elif user_choice.lower() == 'n':
            #~ Display next page
            page = display_next_page(page, total_pages, text_choice, category_id)

        elif user_choice.lower() == 'b':
            #~ Display previous page
            page = display_previous_page(page, total_pages, text_choice, category_id)

        else:
            try:
                choice_int = int(user_choice)
                if 0 < choice_int <= ROWS_PER_PAGE:
                    #~ Correct choice, handle the chosen category
                    display_alternative_product(choice_int, category_id, page)
                else:
                    clear_and_print(text_choice)
                    print_products_page(category_id, page)
                    print("Le nombre choisi n'est pas dans la liste")

            except ValueError:
                clear_and_print(text_choice)
                print_products_page(category_id, page)
                print("Choix non reconnu, veuillez entrer un nombre, ou Q pour quitter, "+
                      "M pour revenir au menu principal")

        user_choice = input(">>")
    return user_choice

def select_product(categories, choice_int):

    #~ Display the menu to select a product and handle the choice
    category_id = categories[choice_int][0]
    category_txt = categories[choice_int][1]
    text_choice = "Vous avez choisi la catégorie numéro {} : {}".format(str(category_id),
                                                                        category_txt)

    #~ Check number of products in selected category

    if get_number_products(category_id) == 0:
        #~ Ask if user wants to request products
        user_choice = filldatabase_menu(text_choice, category_txt, category_id)
        return user_choice
    else:
        #~ There are products, we display them with pages
        user_choice = display_pages(text_choice, category_id)
        return user_choice

def select_category():

    #~ Display the menu to select a category and handle the choice
    txt_menu_cat = ("Selectionnez votre catégorie d'aliment à l'aide du numéro, Q pour quitter, "+
                    "M pour revenir au menu principal:\n")
    #~ Add categories to menu
    txt_menu_cat += str_categories()
    #~ Get list with categories
    categories = get_categories()
    clear_and_print(txt_menu_cat)
    user_choice = input(">>")

    while True:
        if user_choice.lower() == 'q' or user_choice.lower() == 'm':
            break
        try:
            choice_int = int(user_choice)-1
            if 0 <= choice_int < len(categories):
                #~ Correct choice, handle the chosen category
                user_choice = select_product(categories, choice_int)
                if user_choice.lower() == 'm':
                    clear_and_print(txt_menu_cat)
                elif user_choice.lower() == 'q':
                    #~ If user quit in submenu
                    break

            else:
                clear_and_print(txt_menu_cat, "Le nombre choisi n'est pas dans la liste")

        except ValueError:
            clear_and_print(txt_menu_cat, "Choix non reconnu, veuillez entrer un nombre, "+
                            "ou Q pour quitter, M pour revenir au menu principal")

        user_choice = input(">>")
    return user_choice

def menu_principal():

    txt_menu1 = ("Selectionnez votre choix à l'aide du numéro, Q pour quitter:\n"+
                 "1 - Quel aliment souhaitez-vous remplacer ?\n"+
                 "2 - Retrouver mes aliments substitués.\n")

    clear_and_print(txt_menu1)
    user_choice = input(">>")

    while True:
        if user_choice == '1':
            #~ Demander la catégorie
            user_choice = select_category()
            if user_choice.lower() == 'm':
                clear_and_print(txt_menu1)
            elif user_choice.lower() == 'q':
                #~ If user quit in submenu
                break
        elif user_choice == '2':
            #~ Retrouver les aliments substitués
            clear_and_print(txt_menu1, 'Choix 2')
        elif user_choice.lower() == 'q':
            break
        else:
            clear_and_print(txt_menu1, 'Choix non reconnu')
        user_choice = input(">>")

def main(args):

    menu_principal()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
