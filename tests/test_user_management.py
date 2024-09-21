
import pytest
import os
import pandas as pd
import bcrypt
from src.user_management import UserManagementSystem

# Fixtures
@pytest.fixture
def user_management_system(tmp_path):
    # Créer un fichier CSV temporaire pour les tests
    csv_file = tmp_path / "users.csv"
    return UserManagementSystem(csv_file=str(csv_file))

# Testez pour être certain que le répertoire de données existe
def test_ensure_data_directory(user_management_system, tmp_path):
    assert os.path.exists(tmp_path), "Le fichier CSV existe."

# Testez le chargement des utilisateurs lorsque le fichier n'existe pas
def test_load_users_new_file(user_management_system):
    users = user_management_system.load_users()
    assert isinstance(users, pd.DataFrame), "renvoit un DataFrame lors de la création du fichier."
    assert users.empty, "Verifie si le fichier csv est vide"

# Tester le chargement des utilisateurs avec des données existantes
def test_load_users_existing_file(user_management_system):
    user_management_system.users = pd.DataFrame({
        'username': ['test_user'],
        'email': ['test_user@example.com'],
        'password_hash': ['hashed_password'],
        'is_admin': [False]
    })
    user_management_system.save_users()

    users = user_management_system.load_users()
    assert len(users) == 1, "Test su un utilisateur est dans le fichier csv ."
    assert users.iloc[0]['username'] == 'test_user'

# Testez la creation d'un utilisateur
def test_create_user(user_management_system):
    user_management_system.create_user('new_user', 'new_user@example.com', 'password123')
    users = user_management_system.load_users()
    assert 'new_user' in users['username'].values, "Un nouvel utilisateur devrait être créer."

# Testez l'authentification d'un utilisateur
def test_authenticate_user(user_management_system):
    user_management_system.create_user('auth_user', 'auth_user@example.com', 'securepassword')
    user = user_management_system.authenticate_user('auth_user', 'securepassword')
    assert user is not None, "Verifie si l'authentification réussit."
    assert user['username'] == 'auth_user'

# Testez la mise à jour de l'email et du password d'un utilisateur
def test_update_user(user_management_system):
    user_management_system.create_user('update_user', 'update_user@example.com', 'initialpassword')
    user_management_system.update_user('update_user', new_email='newemail@example.com', new_password='newpassword')

    user = user_management_system.authenticate_user('update_user', 'newpassword')
    assert user is not None, "Verifie que l'utilisateur s'authentifie avec le mot de passe mis à jour."
    assert user['email'] == 'newemail@example.com', "L'email est mis à jour"

# testez la suppression d'utilisteur
def test_delete_user(user_management_system):
    user_management_system.create_user('delete_user', 'delete_user@example.com', 'password123')
    user_management_system.delete_user('delete_user')
    
    users = user_management_system.load_users()
    assert 'delete_user' not in users['username'].values, "Verifie que l'utilisateur est supprimé"

# Testez pour êtrte certain qu'un administrateur existe
def test_ensure_admin_exists(user_management_system, monkeypatch):
    # Simuler la saisie de l'utilisateur pour créer un administrateur
    inputs = iter(['admin_user', 'admin@example.com', 'adminpassword'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    user_management_system.ensure_admin_exists()
    
    users = user_management_system.load_users()
    assert users['is_admin'].any()
    assert 'admin_user' in users['username'].values, "verifie que l'admin peut être crée"

# Tester l'exécution automatisée de pytest
def run_all_tests():
    pytest.main()

if __name__ == "__main__":
    run_all_tests()
