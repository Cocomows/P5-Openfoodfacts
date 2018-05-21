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

def select_product(categories, choice_int):

    #~ Display the menu to select a product and handle the choice
    category_id = categories[choice_int][0]
    page = 1
    total_pages = get_number_pages(category_id)

    text_choice = ("Vous avez choisi la catégorie numéro "+str(category_id)+
                   " : "+str(categories[choice_int][1]))
    if total_pages > 1:
        text_choice += ("\nNavigation avec (B)ack et (N)ext pour la pagination")

    clear_and_print(text_choice)
    print_products_page(category_id, page)

    user_choice = input(">>")
    while user_choice.lower() != 'q' and user_choice.lower() != 'm':
        if user_choice.lower() == 'n':
            #~ Display next page
            if page+1 <= total_pages:
                page += 1
                clear_and_print(text_choice)
                print_products_page(category_id, page)
            else:
                clear_and_print(text_choice)
                print_products_page(category_id, page)
                print("Dernière page atteinte")

        elif user_choice.lower() == 'b':
            #~ Display previous page
            if page-1 > 0:
                page -= 1
                clear_and_print(text_choice)
                print_products_page(category_id, page)
            else:
                clear_and_print(text_choice)
                print_products_page(category_id, page)
                print("Première page atteinte")


        try:
            choice_int = int(user_choice)

            if 0 < choice_int < ROWS_PER_PAGE:
                #~ Correct choice, handle the chosen category
                print("choix :"+str(choice_int))
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

def select_category():

    #~ Display the menu to select a category and handle the choice
    txt_menu_cat = ("Selectionnez votre catégorie d'aliment à l'aide du numéro, Q pour quitter, "+
                    "M pour revenir au menu principal:\n")
    txt_menu_cat += str_categories()
    categories = get_categories()
    clear_and_print(txt_menu_cat)
    user_choice = input(">>")

    while user_choice.lower() != 'q' and user_choice.lower() != 'm':
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

    while user_choice.lower() != 'q':

        if user_choice.lower() != 'q':
            if user_choice == '1':
                #~ Demander la catégorie
                user_choice = select_category()

            elif user_choice == '2':
                #~ Retrouver les aliments substitués
                clear_and_print(txt_menu1, 'Choix 2')

            else:
                clear_and_print(txt_menu1, 'Choix non reconnu')

            if user_choice.lower() != 'q':
                #~ If user didn't quit in submenu
                user_choice = input(">>")


def main(args):

    menu_principal()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
