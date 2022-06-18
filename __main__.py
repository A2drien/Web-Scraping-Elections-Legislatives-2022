import requests
from bs4 import BeautifulSoup, NavigableString, ResultSet, Tag
from urllib.parse import urljoin
import re

import pandas as pd

URL = "https://www.resultats-elections.interieur.gouv.fr/legislatives-2022/index.html"
NOM_FICHIER = "file.csv"


def _get_reponse_url(url: str) -> BeautifulSoup:
    """Retourne le code HTML de la page demandée"""

    return BeautifulSoup(requests.get(url).text, "html.parser")


def get_liste_url_departement() -> list[str]:
    """Retourne la liste des URLs de tous les départements"""

    soup = BeautifulSoup(requests.get(URL).content, "html.parser")
    select_tag :Tag = soup.find("select")  #type: ignore
    options :ResultSet[Tag] = select_tag.find_all("option")

    return [urljoin(URL, "./" + (str(option["value"]))) for option in options][1:]


def get_liste_url_circonscription(url_departement: str) -> list[str]:
    """Retourne la liste des URLs de toutes les circonscriptions du département"""
    
    soup = _get_reponse_url(url_departement)                                                #Les 2 derniers liens ne sont pas utiles
    liste_circo = [urljoin(url_departement, link.get('href')) for link in soup.find_all('a')]
    return liste_circo[2:-2]


def get_resultats(url_circonscription: str)-> list[dict]:
    """Retourne les résultats sous forme de liste de dictionnaire"""

    dico = {}
    
    return [{}]


def sauvegarder(resultats: list[dict]) -> None:
    """Sauvegarde les données dans un fichier csv"""

    df = pd.DataFrame(resultats, columns=[])
    df.to_csv(NOM_FICHIER, index=False, encoding='utf-8')


def resultats_sortis(url_circonscription :str) -> bool:
    return True


if __name__ == '__main__':
    resultats = []
    for departement in get_liste_url_departement():
        for circonscription in get_liste_url_circonscription(departement):
            resultats += get_resultats(circonscription)

    #sauvegarder(resultats)