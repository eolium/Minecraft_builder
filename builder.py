#!/usr/bin/python3
from sys import argv
import os
import shutil
import json

# On tente d'importer la librairie requests (on l'installe si nécessaire)
try:
    from requests import get
except:
    os.system("pip install requests")
    os.system("pip install --break-system-packages requests")
    from requests import get

def bad_argument():
    print("""Création de serveur minecraft. Usages possibles :
./builder install
builder create {server_name} {server_type} {server_version}

- server_name : nom du serveur
- server_type : type de serveur (vanilla, forge, paper, create, ...)
                si le type n'est pas pris en charge, une erreur est générée
- server_version : version du serveur, sans espace (format classique quoi)
""")
    exit()


def download_jar(server_name, server_type, server_version):
    print("Recherche du type de serveur en cours...")

    api = "https://mcutils.com/api/server-jars"

    types = get(api).json()
    found = False
    for e in types:
        if e["key"] == server_type:
            api = e["url"]
            found = True
            break

    if found:
        print("Type de serveur trouvé")
    else:
        print("Le type de serveur n'a pas été trouvé")
        print("Fin du programme")
        exit()


    print("Recherche d'une version disponible")

    versions = get(api).json()
    found = False
    for e in versions:
        if e["version"] == server_version:
            api = e["url"]
            found = True
            break

    if found:
        print("Version trouvé")
    else:
        print("La version n'a pas été trouvée")
        print("Fin du programme")
        exit()


    print("Téléchargement du fichier jar d'installation...")

    download = get(api).json()["downloadUrl"]

    # Techniquement une faille par prompt injection, donc À N'UTILISER QU'EN LIGNE DE COMMANDE !!
    os.system(f"wget {download} -O version_jars/{server_type}_{server_version}.jar")

    print("Fichier d'installation téléchargé")

if len(argv) == 1:
    bad_argument()

# Ici len >= 2

cmd = argv[1]

if cmd == "create":
    if len(argv) < 5: bad_argument()

    server_name = argv[2]
    server_version = argv[4]
    server_type = argv[3]

    jar_path = f"version_jars/{server_type}_{server_version}.jar"

    if os.path.exists(server_name):
        shutil.rmtree(server_name)

    if not os.path.exists(jar_path):
        print("Aucun installateur local trouvé, téléchargement...")
        download_jar(server_name, server_type, server_version)

    print("Installation du serveur...")

    os.mkdir(server_name)

    shutil.copyfile(jar_path, f"{server_name}/server.jar")

    os.system(f"echo 'eula=true' > {server_name}/eula.txt")

    if os.system(f"cd {server_name} && java --installServer /server.jar"):
        if os.system(f"cd {server_name} && java -Xmx7G -Xms1G -jar server.jar nogui"):
            print("Je ne sais pas quelle commande utiliser pour lancer le serveur...")
            exit()



if cmd == "start":
    server_name = argv[2]
    os.system(f"cd {server_name} && java -Xmx7G -Xms1G -jar server.jar nogui")