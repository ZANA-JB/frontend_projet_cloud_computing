"""Script de test local pour vérifier l'intégration des fichiers.
Utilise le module api.py (qui partage la session HTTP) pour :
1. se connecter à un compte existant (à remplir ci-dessous)
2. uploader un petit fichier texte de démonstration
3. lister les fichiers de l'utilisateur et afficher le résultat

Exécutez ce script dans le même environnement que l'application Flask :

    py local_test.py

Une fois le script exécuté avec succès, ouvrez le tableau de bord dans le
navigateur (`http://127.0.0.1:5000/dashboard`) et vérifiez que le fichier
apparait.

Remplacez les valeurs d'email/mot de passe par un compte valide déjà créé
sur le backend.

"""

import os
import io
import api

# paramètres de test - modifiez avec un compte existant
TEST_EMAIL = "zana@gmail.com"
TEST_PASSWORD = "zana@gmail.com"

# localisation du fichier à téléverser (on crée un fichier temporaire)
TEST_FILENAME = "fichier_de_test.txt"


def perform_test():
    print("Health API ->", api.health())
    # login
    try:
        login_resp = api.login(TEST_EMAIL, TEST_PASSWORD)
        print("login response", login_resp)
    except api.APIError as e:
        print("Erreur lors de la connexion :", e)
        return

    user = login_resp.get("user")
    if not user:
        print("Impossible de récupérer l'utilisateur après login")
        return
    user_id = user.get("id")
    print("Utilisateur connecté id=", user_id)

    # préparer un fichier temporaire
    with open(TEST_FILENAME, "w", encoding="utf-8") as f:
        f.write("Ceci est un fichier de test.\n")

    # uploader
    with open(TEST_FILENAME, "rb") as f:
        try:
            up = api.upload_file(f, user_id, name="test-upload", status="private")
            print("upload response:", up)
        except api.APIError as e:
            print("Erreur upload (APIError):", e)
            return
        except Exception as e:
            print("Erreur upload (autre):", e)
            return

    # lister les fichiers de l'utilisateur
    try:
        files = api.get_user_files(user_id)
        print("Files for user:", files)
    except api.APIError as e:
        print("Erreur get_user_files:", e)
        return
    except Exception as e:
        print("Erreur get_user_files (autre):", e)
        return

    print("Test terminé. Vérifiez le dashboard dans le navigateur.")
    # cleanup
    try:
        os.remove(TEST_FILENAME)
    except Exception:
        pass


if __name__ == "__main__":
    try:
        perform_test()
    except Exception as e:
        print("Erreur inattendue dans le script de test :", e)