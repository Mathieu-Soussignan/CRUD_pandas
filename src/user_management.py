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


def modifier_utilisateur():
    if not os.path.isfile(csv_file_path):
        # Si le fichier n'existe pas je sors directement de la fonction
        print("Le fichier 'users.csv' n'existe pas.")
        return
    
    # Je lis le csv
    users_df = pd.read_csv(csv_file_path)
    
    user_name = input("Veuillez entrer le nom d'utilisateur à modifier : ")
    
    if user_name in users_df["nom_utilisateur"].values:
        print("Utilisateur trouvé.")
        
        new_user_name = input("Entrez le nouveau nom d'utilisateur (laisser vide pour ne pas modifier) : ")
        new_password = input("Entrez le nouveau mot de passe (laisser vide pour ne pas modifier) : ")
        new_email = input("Entrez la nouvelle adresse email (laisser vide pour ne pas modifierne) : ")

        
        if new_user_name:
            users_df.loc[users_df["nom_utilisateur"] == user_name, "nom_utilisateur"] = new_user_name
        if new_email:
            users_df.loc[users_df["nom_utilisateur"] == user_name, "adresse_mail"] = new_email
        if new_password:
            # Je hash le nouveau mot de passe
            users_df.loc[users_df["nom_utilisateur"] == user_name, "mot_de_passe"] = generate_password_hash(new_password)
        
        
        users_df.to_csv(csv_file_path, index=False)
        print("Informations de l'utilisateur mises à jour.")
    else:
        print("Utilisateur non trouvé.")


def supprimer_utilisateur():
    # Si le fichier n'existe pas je sors directement de la fonction
    if not os.path.isfile(csv_file_path):
        print("Le fichier 'users.csv' n'existe pas.")
        return
    # Je lis le csv
    users_df = pd.read_csv(csv_file_path)
    
    user_name = input("Veuillez entrer le nom d'utilisateur à supprimer : ")
    
    # Si le nom_d'utilisateur existe pas dans la valeur de la colonne
    if user_name in users_df["nom_utilisateur"].values:
        # Je renvoie True si le nom d'utilisateur ne correspond pas au nom d'utilisateur que je veux supprimer
        users_df = users_df[users_df["nom_utilisateur"] != user_name]
        users_df.to_csv(csv_file_path, index=False)
        print("Utilisateur supprimé.")
    else:
        print("Utilisateur non trouvé.")