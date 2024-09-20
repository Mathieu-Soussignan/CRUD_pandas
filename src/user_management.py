from werkzeug.security import generate_password_hash
import pandas as pd
import os


# Chemin du fichier users.csv
csv_file_path = os.path.join("data", "users.csv")


def creation_utilisateurs():
    user_name = input("Veuillez entrer votre nom d'utilisateur : ")
    user_password = input("Veuillez entrer votre mot de passe : ")
    
    # Boucle pour valider l'entrée seulement si il y a un @ dedans
    while True:    
        user_mail = input("Veuillez entrer votre email : ")
        if "@" in user_mail:
            break
        else:
            print("Réssayez, le mail n'est pas valide")

    # Hash du mot de passe stocker dans une variable
    user_password_hash = generate_password_hash(user_password)
    
    # Création du dictionnaire, pour stocker les clé + valeurs, ça serait intérressant pour le csv après
    user_data = {
        "nom_utilisateur": [user_name],
        "mot_de_passe": [user_password_hash],
        "adresse_mail": [user_mail]
    }
    
    # puis création de la DataFrame
    users_df = pd.DataFrame(user_data)
    
    # On verifie si le fichier 'users.csv' existe 
    file_exists = os.path.isfile(csv_file_path)
    # 2 Structures conditionnelles
    
    if file_exists: # Renvoie True si 'users.csv" existe
        # Si le fichier existe, j'ajoute avec le mode 'a' = append
        users_df.to_csv(csv_file_path, mode="a", header=False, index=False)
    else: 
        # SI le fichier n'existe pas, j'ajoute avec le mode 'w' = ecriture
        users_df.to_csv(csv_file_path, mode= "w", header=True, index=False)


# -------------------------------------------------------------


def afficher_utilisateurs():
    if os.path.isfile(csv_file_path):
    # Si il existe je lis le fichier
        users_df = pd.read_csv(csv_file_path)
        
        if users_df.empty:
            print("Le fichier 'users.csv' est vide")
        else:
            # Les mots de passe de la colonne 'mot_de_passe' vaudront '*******'
            users_df["mot_de_passe"] = '*******'
            print(users_df)
            
    else:
        print("Le fichier 'users.csv' n'existe pas")   


# -------------------------------------------------------------
