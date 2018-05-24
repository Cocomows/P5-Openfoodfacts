#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
Module used to offer a command line interface to navigate the application
P5 Openfoodfacts.
Displays products for a given Openfoodfacts category and offers an alternative product with
a better nutriscore when user selects a product
"""
import os
from bdd import *

def clear_and_print(txtmenu, txtchoice=False):
    """
    Clears command line interface and prints given choice, with an optional second str to add
    """
    os.system('cls||clear')
    print(txtmenu)
    if txtchoice:
        print(txtchoice)
    return

def str_product(product):
    """
    Returns a string of a product with informations displayed in a readable way
    Param : product : list returned from database with all informations
    """

    str_res = """
    Produit             : {}
    Marque              : {}
    Description         : {}
    Nutriscore          : {}
    En vente chez       : {}
    Lien openfoodfacts  : {}"""
    if not product[6]:
        store = "Information non disponible"
    else:
        store = product[6]
    return(str_res.format(product[1], product[3], product[5], NUTRISCORE[product[4]],
                          store, product[7]))

def save_option(txtproduit, product_id):
    """
    Menu to allow user to save a product
    """
    txt_sauv = "\n\nSouhaitez vous sauvegarder le résultat ?\n"
    txt_sauv += "[O]ui ou [N]on pour revenir au menu précédent."
    clear_and_print(txtproduit, txt_sauv)
    user_choice = input(">>")
    while True:
        if user_choice.lower() == 'q':
            return 'q'
        elif user_choice.lower() == 'n':
            return 'm'
        elif user_choice.lower() == 'o':
            save_product(product_id)
            clear_and_print(txtproduit)
            print("\n\nLe produit a bien été sauvegardé.\n"+
                  "Appuyez sur Entrée pour revenir au menu précédent.")

            user_choice = input(">>")
            return 'm'
        else:
            clear_and_print(txtproduit, txt_sauv)
            print("Choix non reconnu")
        user_choice = input(">>")
    return user_choice

def display_alternative_product(choice_int, category_id, page):
    """
    For a product selected from the product menu, displays an alternative and calls save_option
    """
    product_info = get_product(category_id, page, choice_int)
    nutriscore_int = product_info[4]
    txtproduit = "Vous avez choisi le produit suivant :\n"

    txtproduit += str_product(product_info)
    if nutriscore_int != 0:
        txtproduit += ("Ce produit a un nutriscore de {}.\n".format(NUTRISCORE[nutriscore_int]))
        if nutriscore_int == get_best_score_category(category_id):
            txtproduit += ("\nFélicitations, votre produit possède déjà le"+
                           " meilleur score de sa catégorie !\n")
            if get_alternative(product_info[0]):
                txtproduit += ("\nUn autre produit de la même catégorie "+
                               "avec un score identique pourrait être :\n")
                txtproduit += (str_product(get_alternative(product_info[0])))
            else:
                txtproduit += ("\nIl n'y a pas d'autre produit dans cette catégorie"+
                               " avec un score identique")
                return save_option(txtproduit, product_info[0])

        else:
            txtproduit += ("\nVoici une alternative à votre produit"+
                           " avec un meilleur nutriscore :\n")
            txtproduit += (str_product(get_alternative(product_info[0])))

    else:
        txtproduit += ("Le nutriscore du produit que vous avez sélectionné n'est pas renseigné.\n")
        txtproduit += ("Voici un produit de la même catégorie"+
                       " avec le meilleur nutriscore possible :\n")
        txtproduit += (str_product(get_alternative(product_info[0])))

    return save_option(txtproduit, get_alternative(product_info[0])[0])

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
    """
    Displays next page from a category
    """
    if page+1 <= total_pages:
        page += 1
        clear_and_print(text_choice)
        print_products_page(category_id, page)
    else:
        clear_and_print(text_choice)
        print_products_page(category_id, page)
        print("Dernière page atteinte")
    return page

def display_previous_page(page, text_choice, category_id):
    """
    Displays previous page from a category
    """
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
    """
    Handles page navigation in a category
    """
    page = 1
    total_pages = get_number_pages(category_id)
    if total_pages > 1:
        text_choice += ("\nSélectionnez un des produits avec le nombre correspondant."+
                        "\nNavigation avec [B]ack et [N]ext pour la pagination"+
                        "\nQ pour quitter, M pour revenir au menu précédent.")

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
            page = display_previous_page(page, text_choice, category_id)

        else:
            try:
                choice_int = int(user_choice)
                if 0 < choice_int <= ROWS_PER_PAGE:
                    #~ Correct choice, handle the chosen category
                    user_choice = display_alternative_product(choice_int, category_id, page)
                    if user_choice.lower() == 'q':
                        break
                    else:
                        clear_and_print(text_choice)
                        print_products_page(category_id, page)
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
    """
    Display menu to select a product, with page navigation or option to fill database if
    the category is empty
    """
    #~ Display the menu to select a product and handle the choice
    category_id = categories[choice_int][0]
    category_txt = categories[choice_int][1]
    text_choice = "Vous avez choisi la catégorie numéro {} : {}".format(str(category_id),
                                                                        category_txt)

    #~ Check number of products in selected category
    if get_number_products(category_id) == 0:
        #~ Ask if user wants to request products
        return filldatabase_menu(text_choice, category_txt, category_id)
    else:
        #~ There are products, we display them with pages
        return display_pages(text_choice, category_id)

def select_category():
    """
    Display the menu to select a category and handle the choice
    """

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

def main_menu():
    """
    Display the main menu and handles the choice
    """

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
            str_saved = "Voici la liste des aliments sauvegardés :\n\n"
            str_saved += get_str_saved()
            clear_and_print(txt_menu1, str_saved)
        elif user_choice.lower() == 'q':
            break
        else:
            clear_and_print(txt_menu1, 'Choix non reconnu')
        user_choice = input(">>")

def main():
    main_menu()
    return 0

if __name__ == '__main__':
    main()
