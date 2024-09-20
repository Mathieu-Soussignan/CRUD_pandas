import pandas as pd
import bcrypt
import seaborn as sns
import matplotlib.pyplot as plt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) 

def create_user(users):
    username = input ("Entrez un nom d'utilisateur:")
    password = input ("Entrez un mot de passe:")
    email = input ("Entrez votre email:")
    hashed_password = hash_password(password)
    new_user = pd.DataFrame({
        'username': [username],
        'password': [hashed_password],
        'email': [email]
    })
    users = pd.concat([users, new_user], ignore_index=True)
    print(f"Utilisateur {username} créé avec succès.")
    return users