import pytest
import os
import pandas as pd
from src.user_management import UserManagementSystem

# Créer un setup pour initialiser un système de gestion d'utilisateurs de test
@pytest.fixture
def user_system():
    # Utiliser un fichier CSV temporaire pour les tests
    test_csv = 'data/test_users.csv'
    # S'assurer qu'on commence avec un fichier vide
    if os.path.exists(test_csv):
        os.remove(test_csv)
    system = UserManagementSystem(csv_file=test_csv)
    yield system
    # Nettoyage : supprimer le fichier de test après les tests
    if os.path.exists(test_csv):
        os.remove(test_csv)

def test_create_user(user_system):
    # Créer un utilisateur
    user_system.create_user("testuser", "test@example.com", "password123", is_admin=False)
    # Vérifier que l'utilisateur est bien créé
    assert "testuser" in user_system.users['username'].values
    assert user_system.users.loc[user_system.users['username'] == "testuser", 'email'].values[0] == "test@example.com"

def test_update_user(user_system):
    # Créer un utilisateur pour tester la mise à jour
    user_system.create_user("updateuser", "old@example.com", "oldpassword", is_admin=False)
    user_system.update_user("updateuser", new_email="new@example.com", new_password="newpassword")
    
    # Vérifier que les informations sont mises à jour
    assert user_system.users.loc[user_system.users['username'] == "updateuser", 'email'].values[0] == "new@example.com"

def test_delete_user(user_system):
    # Créer un utilisateur pour le supprimer ensuite
    user_system.create_user("deleteuser", "delete@example.com", "password123", is_admin=False)
    user_system.delete_user("deleteuser")
    
    # Vérifier que l'utilisateur a bien été supprimé
    assert "deleteuser" not in user_system.users['username'].values
