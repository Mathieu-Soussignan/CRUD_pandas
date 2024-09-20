from src.user_management import UserManagementSystem
import seaborn as sns
import matplotlib.pyplot as plt

def main_menu(system, user):
    while True:
        print("\n--- Menu Principal ---")
        print("1. Liste des utilisateurs")
        print("2. Créer un utilisateur")
        print("3. Mettre à jour un utilisateur")
        print("4. Supprimer un utilisateur")
        print("5. Visualiser les statistiques")
        print("6. Déconnexion")
        
        choice = input("Choisissez une option : ")
        
        if choice == "1":
            print(system.list_users())
        elif choice == "2":
            create_user_menu(system)
        elif choice == "3":
            update_user_menu(system)
        elif choice == "4":
            delete_user_menu(system)
        elif choice == "5":
            visualize_user_stats(system)
        elif choice == "6":
            print("Déconnexion...")
            break
        else:
            print("Option invalide. Veuillez réessayer.")

def create_user_menu(system):
    print("\n--- Création d'un nouvel utilisateur ---")
    username = input("Nom d'utilisateur : ")
    email = input("Adresse e-mail : ")
    password = input("Mot de passe : ")
    is_admin = input("Est-ce un administrateur? (o/n) : ").lower() == "o"
    system.create_user(username, email, password, is_admin)

def update_user_menu(system):
    print("\n--- Mise à jour d'un utilisateur ---")
    username = input("Nom d'utilisateur à mettre à jour : ")
    new_email = input("Nouvelle adresse e-mail (laisser vide pour ne pas changer) : ")
    new_password = input("Nouveau mot de passe (laisser vide pour ne pas changer) : ")
    system.update_user(username, new_email if new_email else None, new_password if new_password else None)

def delete_user_menu(system):
    print("\n--- Suppression d'un utilisateur ---")
    username = input("Nom d'utilisateur à supprimer : ")
    system.delete_user(username)

def visualize_user_stats(system):
    user_counts = system.users['is_admin'].value_counts()
    sns.barplot(x=user_counts.index.map({True: 'Admin', False: 'User'}), y=user_counts.values)
    plt.title('Distribution des types d\'utilisateurs')
    plt.xlabel('Type d\'utilisateur')
    plt.ylabel('Nombre')
    plt.show()

def main():
    system = UserManagementSystem()
    system.ensure_admin_exists()
    
    while True:
        username = input("Nom d'utilisateur : ")
        password = input("Mot de passe : ")
        
        user = system.authenticate_user(username, password)
        if user is not None:
            print(f"Bienvenue, {username}!")
            main_menu(system, user)
        else:
            print("Authentification échouée. Veuillez réessayer.")

if __name__ == "__main__":
    main()