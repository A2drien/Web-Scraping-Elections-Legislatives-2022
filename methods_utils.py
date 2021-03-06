import requests
from bs4 import BeautifulSoup


URL = "https://www.resultats-elections.interieur.gouv.fr/legislatives-2022/index.html"

NOM_FICHIER = "data.csv"                            #Nom du fichier où sauvegarder les données
CLASSE_TABLE_RESULTATS = "tableau-resultats-listes-ER"      #Nom de la classe du tableau web à scrapper
CLASSE_TABLE_EXCEPTION_DEP_99 = "table table-bordered"
CLASSE_DIVISION = "offset2 span8"

IDX_NOM_PRENOM = 0                                  #Index de la colonne où trouver le nom et prénom du candidat
IDX_NB_VOIX = 2                                     #Index de la colonne où trouver le nombre de voix qu'à obtenu un candidat

LABEL_CIRCONSCRIPTION = "Num_Circo"                 #Label utilisé dans le code et dans le .csv pour le nombre de circonscriptions
LABEL_NOM = "Nom"                                   #Label utilisé dans le code et dans le .csv pour le nom du candidat
LABEL_PRENOM = "Prenom"                             #Label utilisé dans le code et dans le .csv pour le prénom du candidat
LABEL_NB_VOIX = "Nb_Voix"                           #Label utilisé dans le code et dans le .csv pour le nombre de voix qu'à obtenu un candidat

SEPARATEUR = ";"                                    #Symbole utilisé pour délimiter les colonne dans le .csv

EXCEPTION_DEP_75 = "https://www.resultats-elections.interieur.gouv.fr/legislatives-2022/075/index.html"
EXCEPTION_DEP_99 = "https://www.resultats-elections.interieur.gouv.fr/legislatives-2022/099/index.html"


def get_reponse_url(url: str) -> BeautifulSoup:
    """Retourne le code HTML de la page demandée"""

    return BeautifulSoup(requests.get(url).text, "html.parser")


def traitement_prenom_nom(prenom_nom: str) -> tuple[str, str]:
    """
    Prend le nom/prénom ent paramètre et retourne le nom et le prénom
    Ex: 'M. Jean BON LE GRAND' renverra : 'Jean', 'BON LE GRAND'
    """

    liste_prenom_nom = prenom_nom.split()[1:]       #On enlève le M./Mme

    #Tout ce qui est en majuscule va dans nom, le reste dans prenom
    nom = " ".join([mot for mot in liste_prenom_nom if mot.isupper() or mot == '-'])
    prenom = " ".join([mot for mot in liste_prenom_nom if not mot.isupper() and mot != '-'])

    return prenom, nom


def get_circonscription(url_circonscription: str) -> str:
    """Prend une URL en paramètre et retourne la circonscription au format xxx-yy"""
    
    format = url_circonscription[-10:-5]
    num_departement = format[:3]
    num_circonscription = format[3:]

    #Bug connu : le département 99 de l'URL est remplacé par 999
    if num_departement == "099": num_departement = "999"

    return num_departement + "-" + num_circonscription


def conversion_nombre(nombre: int) -> str:
    """Retourne un chiffre en format XX au de lieu de X"""

    if nombre < 10: return "0" + str(nombre)
    else: return str(nombre)