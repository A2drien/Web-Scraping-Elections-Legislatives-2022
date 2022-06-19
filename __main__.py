import re
import requests
from urllib.parse import urljoin
import pandas as pd
from bs4 import BeautifulSoup, ResultSet, Tag
from methods_utils import *


def get_liste_url_departement() -> list[str]:
    """Retourne la liste des URLs de tous les départements"""

    soup = BeautifulSoup(requests.get(URL).content, "html.parser")
    select_tag: Tag = soup.find("select")  #type: ignore
    options: ResultSet[Tag] = select_tag.find_all("option")

    return [urljoin(URL, "./" + (str(option["value"]))) for option in options][1:]


def get_liste_url_circonscription(url_departement: str) -> list[str]:
    """Retourne la liste des URLs de toutes les circonscriptions du département"""

    #Si le département actuel est le 75, alors procéder à la sélection "à la main"
    if url_departement == EXCEPTION_DEP_75:
        liste_circo = [f"https://www.resultats-elections.interieur.gouv.fr/legislatives-2022/075/075{conversion_nombre(i)}.html" for i in range(1,19)] 
        return liste_circo

    
    soup = get_reponse_url(url_departement)

    #Si le département est celui des francais de l'étranger, alors procéder à un 
    if url_departement == EXCEPTION_DEP_99:
        select_tags: ResultSet[Tag] = soup.find("table", {"class": CLASSE_TABLE_EXCEPTION_DEP_99}) #type: ignore
        liste_circo = [urljoin(url_departement, link.get('href')) for link in select_tags.find_all('a')]  #type: ignore
    
    select_tags: ResultSet[Tag] = soup.find_all("div", {"class": CLASSE_DIVISION})
    liste_circo = [urljoin(url_departement, link.get('href')) for link in select_tags[1].find_all('a')]

    return liste_circo


def get_resultats(url_circonscription: str)-> list[dict[str, str]]:
    """Retourne les résultats sous forme de liste de dictionnaire"""
    
    liste_donnes_candidats = []
    soup = get_reponse_url(url_circonscription)

    try:
        select_tags: ResultSet[Tag] = soup.find_all("table",{"class": CLASSE_TABLE_RESULTATS})
        select_tag: Tag = select_tags[-2].find("tbody") #type: ignore

        lignes: ResultSet[Tag] = select_tag.find_all("tr")

        for ligne in lignes:
            donnes_candidat = {}
            donnees_brutes: ResultSet[Tag] = ligne.find_all("td")
            
            donnes_candidat[LABEL_PRENOM], donnes_candidat[LABEL_NOM] = traitement_prenom_nom(donnees_brutes[IDX_NOM_PRENOM].text)
            donnes_candidat[LABEL_NB_VOIX] = "".join(donnees_brutes[IDX_NB_VOIX].text.split())
            donnes_candidat[LABEL_CIRCONSCRIPTION] = get_circonscription(url_circonscription)
            
            liste_donnes_candidats.append(donnes_candidat)

        return liste_donnes_candidats

    except:
        print(f"Résultats manquants pour la circonscription {get_circonscription(url_circonscription)}")
        return [{}]


def sauvegarder(resultats: list[dict]) -> None:
    """Sauvegarde les données dans un fichier csv"""

    df = pd.DataFrame(resultats, columns=[LABEL_CIRCONSCRIPTION, LABEL_NOM, LABEL_PRENOM, LABEL_NB_VOIX])
    df.to_csv(NOM_FICHIER, index=False, encoding='utf-8', sep=SEPARATEUR)


if __name__ == '__main__':
    resultats = []
    for departement in get_liste_url_departement():
        for circonscription in get_liste_url_circonscription(departement):
            print(circonscription)
            resultats += get_resultats(circonscription)

    sauvegarder(resultats)