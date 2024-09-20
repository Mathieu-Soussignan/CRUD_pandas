import pytest
import pandas as pd 
# from src import *
import os 
from werkzeug.security import generate_password_hash

# Fonction à tester : 
# creation_utilisateurs():

def test_creation_utilisateurs(monkeypatch):

    # Sauvegarde de l'ancien CSV
    if os.path.isfile('users.csv'):
        os.rename('users.csv', 'users_backup.csv')

    # similer l'entrée de l'utilisateur
    # iter() créer un itération à partir d'une liste de 3 valeurs. Cela permet de parcourir les valeurs une par une
    # Automatisation du test sans intervention manuelle
    user_inputs = iter(['test_user', 'test_password', 'test@exemple.com'])
    
    # monkeypatch.setattr() aide à définir/supprimer en toute sécurité un attribut, un élément de dictionnaire ou une variable d'environnement
    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))
    
    # appel de la fonction
    df = creation_utilisateurs()
    
    # verification des données dans le dataframe 
    # user_name = input("Veuillez entrer votre nom d'utilisateur : ")
    # user_password = input("Veuillez entrer votre mot de passe : ")
    # user_mail = input("Veuillez entrer votre email : ")
    assert df.shape == ( 1 , 3 )
    assert df['nom_utilisateur'][0] == 'test_user'
    assert df['mo_de_passe'][0] == 'test_password'
    assert df['adresse_mail'][0] == 'test@exemple.com'
    
    # verification du csv
    # file_exists = os.path.isfile('users.csv')
    assert os.path.isfile('users.csv')
    saved_df = pd.read_csv('users.csv')
    assert saved_df.shape == ( 1 , 3 )
    assert saved_df['nom_utilisateur'][0] == 'test_user'
    assert saved_df['mo_de_passe'][0] == 'test_password'
    assert saved_df['adresse_mail'][0] == 'test@exemple.com'
    
    # Supprime du csv crée
    os.remove('users.csv')
    if os.path.isfile('users_backup.csv'):
        os.rename('users_backup.csv', 'users.csv')
        
    
    test_creation_utilisateurs()
    