#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
import os

def select_category():
    os.system('cls||clear')
    txt_menu2 = ("Selectionnez votre choix à l'aide du numéro, Q pour quitter, "+
                        "M pour revenir au menu principal:\n"+"1 - Cat1\n2 - Cat2\n")
    print(txt_menu2)
    user_choice = input(">>")

    while user_choice != 'q' and user_choice != 'm':
        if user_choice == '1':
            #~ Cat 1
            os.system('cls||clear')
            print(txt_menu2)
            print('Catégorie 1')
        elif user_choice == '2':
            #~ Retrouver les aliments substitués
            os.system('cls||clear')
            print(txt_menu2)
            print('Catégorie 2')
        else:
            os.system('cls||clear')
            print(txt_menu2)
            print('Choix non reconnu')

        user_choice = input(">>")
    return user_choice

def menu_principal():
    txt_menu1 = ("Selectionnez votre choix à l'aide du numéro, Q pour quitter:\n"+
                 "1 - Quel aliment souhaitez-vous remplacer ?\n"+
                 "2 - Retrouver mes aliments substitués.\n")
    
    os.system('cls||clear')    
    print(txt_menu1)
    user_choice = input(">>")

    while user_choice != 'q':

        if user_choice == '1':
            #~ Demander la catégorie
            user_choice = select_category()
            os.system('cls||clear')    
            print(txt_menu1)
            
        elif user_choice == '2':
            #~ Retrouver les aliments substitués
            os.system('cls||clear')    
            print(txt_menu1)
            print('Choix 2')
            
        else:
            os.system('cls||clear')    
            print(txt_menu1)
            print('Choix non reconnu')

        if user_choice != 'q':

            user_choice = user_choice = input(">>")


def main(args):

    menu_principal()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
