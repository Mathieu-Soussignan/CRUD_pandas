# users = pd.DataFrame({
#     'user_name': ['admin', 'john', 'jane'],
#     'password': ['adminpass', 'johnpass', 'janepass'],
#     'email': ['admin@example.com', 'john@example.com', 'jane@example.com']
# })

# print("Liste initiale des utilisateurs :")
# print(users)

#suppression d'un utilisateur :
def delete_user():
    global users
    user_name = input("Entrez le nom de l'utilisateur que vous souhaitez supprimer:")
    if user_name in users['user_name'].values:
        users = users [users['user_name'] != user_name]
        print(f"Utilisateur {user_name} supprimé avec succès.✅")
    else:
        print(f"L'utilisateur {user_name} n'existe pas.❌")
    return users

users = delete_user()

# Afficher la liste des utilisateurs après suppression
print("Liste des utilisateurs après suppression :")
print(users)