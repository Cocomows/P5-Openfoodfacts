#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
import os
import mysql.connector

def clear_and_print(txtmenu, txtchoice=False):
    os.system('cls||clear')
    print(txtmenu)
    if txtchoice:
        print(txtchoice)
    return

def select_category():

    txt_menu2 = ("Selectionnez votre catégorie d'aliment à l'aide du numéro, Q pour quitter, "+
                 "M pour revenir au menu principal:\n")

    conn = mysql.connector.connect(host="localhost", user="cocomo", password="password",
                                   database="openfoodfacts")
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM category""")
    rows = cursor.fetchall()
    for row in rows:
        txt_menu2 += ('{0} : {1} - {2}\n'.format(row[0], row[1], row[2]))

    conn.close()

    clear_and_print(txt_menu2)

    user_choice = input(">>")


    while user_choice != 'q' and user_choice != 'm':
        try:
            choice_int = int(user_choice)-1

            if 0 <= choice_int < len(rows):
                try:
                    text_choice = ("Vous avez choisi la catégorie numéro "+str(rows[choice_int][0])+
                                   " : "+str(rows[choice_int][1]))
                    clear_and_print(txt_menu2, text_choice)
                except IndexError:
                    clear_and_print(txt_menu2, "Erreur : Le nombre n'est pas dans la liste")
            else:
                clear_and_print(txt_menu2, "Le nombre choisi n'est pas dans la liste")

        except ValueError:
            clear_and_print(txt_menu2, 'Choix non reconnu')

        user_choice = input(">>")
    return user_choice

def menu_principal():

    txt_menu1 = ("Selectionnez votre choix à l'aide du numéro, Q pour quitter:\n"+
                 "1 - Quel aliment souhaitez-vous remplacer ?\n"+
                 "2 - Retrouver mes aliments substitués.\n")

    clear_and_print(txt_menu1)
    user_choice = input(">>")

    while user_choice != 'q':

        if user_choice == '1':
            #~ Demander la catégorie
            user_choice = select_category()
            clear_and_print(txt_menu1)

        elif user_choice == '2':
            #~ Retrouver les aliments substitués
            clear_and_print(txt_menu1, 'Choix 2')

        else:
            clear_and_print(txt_menu1, 'Choix non reconnu')

        if user_choice != 'q':

            user_choice = input(">>")


def main(args):

    menu_principal()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
