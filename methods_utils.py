import requests
from bs4 import BeautifulSoup


URL = "https://www.resultats-elections.interieur.gouv.fr/legislatives-2022/index.html"
NOM_FICHIER = "file.csv"
CLASSE_TABLEAU = "tableau-resultats-listes-ER"

IDX_NOM_PRENOM = 0
IDX_NB_VOIX = 2

LABEL_CIRCONSCRIPTION = "Num_Circo"
LABEL_NOM = "Nom"
LABEL_PRENOM = "Prenom"
LABEL_NB_VOIX = "Nb_Voix"


def get_reponse_url(url: str) -> BeautifulSoup:
    """Retourne le code HTML de la page demandée"""

    return BeautifulSoup(requests.get(url).text, "html.parser")



def traitement_prenom_nom(prenom_nom :str) -> tuple[str, str]:
    """
    Prend le nom/prénom ent paramètre et retourne le nom et le prénom
    Ex : 'M. Jean BON LE GRAND' renverra : 'Jean', 'BON LE GRAND'
    """

    liste_prenom_nom = prenom_nom.split()[1:]                                   #On enlève le M./Mme
    prenom = liste_prenom_nom[0]                                                #Le "1er" élément est le prénom
    nom = " ".join(liste_prenom_nom[1:])                                        #Le reste est le nom
    return nom, prenom


def traitement_circonscription(url: str) -> str:
    
    return ""