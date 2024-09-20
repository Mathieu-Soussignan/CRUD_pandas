from werkzeug.security import generate_password_hash
import pandas as pd
import os


def creation_utilisateurs():
    user_name = input("Veuillez entrer votre nom d'utilisateur : ")
    user_password = input("Veuillez entrer votre mot de passe : ")
    user_mail = input("Veuillez entrer votre email : ")

    # Hash du mot de passe stocker dans une variable
    user_password_hash = generate_password_hash(user_password)

    # Création du dictionnaire, pour stocker les clé + valeurs, ça serait intérressant pour le csv après
    user_data = {
        'nom_utilisateur': [user_name],
        'mot_de_passe': [user_password_hash],
        'adresse_mail': [user_mail]
    }
    
    # puis création de la DataFrame
    users_df = pd.DataFrame(user_data)
    
    
    # On verifie si le fichier 'users.csv' existe 
    file_exists = os.path.isfile('users.csv')
    # 2 Structures conditionnelles
    
    if file_exists: # Renvoie True si 'users.csv" existe

        # Si le fichier existe, j'ajoute avec le mode 'a' = append
        users_df.to_csv("users.csv", mode="a", header=False, index=False)
    else: 
        # SI le fichier n'existe pas, j'ajoute avec le mode 'w' = ecriture
        users_df.to_csv("users.csv", mode= "w", header=True, index=False)

    # La fonction retourne la DataFrame


creation_utilisateurs()

