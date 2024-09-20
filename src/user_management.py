import os
import pandas as pd
import bcrypt
from typing import Optional

class UserManagementSystem:
    def __init__(self, csv_file='data/users.csv'):
        # Initialise le système avec le fichier CSV spécifié
        self.csv_file = csv_file
        self.ensure_data_directory()
        self.users = self.load_users()

    def ensure_data_directory(self):
        os.makedirs(os.path.dirname(self.csv_file), exist_ok=True)

    def load_users(self):
        if not os.path.exists(self.csv_file):
            # Créer un DataFrame vide si le fichier n'existe pas
            df = pd.DataFrame(columns=['username', 'email', 'password_hash', 'is_admin'])
            df.to_csv(self.csv_file, index=False)
            print(f"Fichier {self.csv_file} créé.")
            return df
        
        try:
            return pd.read_csv(self.csv_file)
        except pd.errors.EmptyDataError:
            print(f"Le fichier {self.csv_file} est vide. Création d'un nouveau DataFrame.")
            return pd.DataFrame(columns=['username', 'email', 'password_hash', 'is_admin'])

    def save_users(self):
        # Sauvegarde les utilisateurs dans le fichier CSV
        self.users.to_csv(self.csv_file, index=False)

    def create_user(self, username, email, password, is_admin=False):
        # Crée un nouvel utilisateur s'il n'existe pas déjà
        if username not in self.users['username'].values:
            # Hashage du mot de passe pour la sécurité
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Ajout du nouvel utilisateur
            new_user = pd.DataFrame({
                'username': [username],
                'email': [email],
                'password_hash': [password_hash],
                'is_admin': [is_admin]
            })
            self.users = pd.concat([self.users, new_user], ignore_index=True)
            self.save_users()
            print(f"Utilisateur '{username}' créé avec succès.")
        else:
            print(f"L'utilisateur '{username}' existe déjà.")

    def authenticate_user(self, username, password):
        # Authentifie un utilisateur
        user = self.users[self.users['username'] == username]
        if not user.empty:
            stored_password_hash = self.users[self.users['username'] == username]['password_hash'].values[0]
            try:
                if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8') if isinstance(stored_password_hash, str) else stored_password_hash):
                    print(f"Authentification réussie pour '{username}'.")
                    return user.iloc[0]
            except ValueError as e:
                print(f"Erreur d'authentification : {e}")
                print(f"Mot de passe stocké pour {username} : {stored_password_hash}")
                return None
        print("Nom d'utilisateur ou mot de passe incorrect.")
        return None

    def list_users(self):
        # Retourne la liste des utilisateurs (sans les mots de passe hashés)
        return self.users[['username', 'email', 'is_admin']]
    
    def update_user(self, username: str, new_email: Optional[str] = None, new_password: Optional[str] = None):
        # Met à jour les informations de l'utilisateur
        user = self.users[self.users['username'] == username]
        if not user.empty:
            if new_email:
                user.at[0, 'email'] = new_email
            if new_password:
                user.at[0, 'password_hash'] = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            self.save_users()
            print(f"Informations de l'utilisateur '{username}' mises à jour.")
        else:
            print(f"L'utilisateur '{username}' n'existe pas.")
            
    def delete_user(self):
        user_name = input("Entrez le nom de l'utilisateur que vous souhaitez supprimer:")
        if user_name in self.users['user_name'].values:
            self.users = self.users [self.users['user_name'] != user_name]
            print(f"Utilisateur {user_name} supprimé avec succès.✅")
        else:
            print(f"L'utilisateur {user_name} n'existe pas.❌")
        return self.users

    users = delete_user()


    def ensure_admin_exists(self):
        # Vérifier s'il existe au moins un administrateur dans la liste des utilisateurs
        if not self.users['is_admin'].any():
            print("Aucun administrateur trouvé. Vous devez créer un administrateur.")
            while True:
                username = input("Nom d'utilisateur admin : ")
                email = input("Adresse e-mail admin : ")
                password = input("Mot de passe admin : ")
                if username not in self.users['username'].values:
                    self.create_user(username, email, password, is_admin=True)
                    print(f"Administrateur {username} créé avec succès.")
                    break
                else:
                    print("Erreur : Le nom d'utilisateur existe déjà. Veuillez réessayer.")

# Initialisation du système
if __name__ == "__main__":
    system = UserManagementSystem()
    system.ensure_admin_exists()
    
    print("Système de gestion d'utilisateurs initialisé.")
    print(f"Nombre d'utilisateurs : {len(system.users)}")