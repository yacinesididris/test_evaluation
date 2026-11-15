import pandas as pd
import numpy as np
import csv

CHEMIN_ASSOCIATIONS = "data/associations.csv"
CHEMIN_MATERIEL = "data/materiel.csv"
CHEMIN_RESERVATIONS = "data/reservations.csv"
CHEMIN_SITES = "data/sites.csv"

from datetime import datetime



def lire_csv(chemin) :
    with open(chemin, "r", encoding="utf-8") as fichier:
        lecteur = csv.DictReader(fichier)
        donnees = list(lecteur)
        return donnees

# Variables

associations = lire_csv(CHEMIN_ASSOCIATIONS)
materiel = lire_csv(CHEMIN_MATERIEL)
reservations = lire_csv(CHEMIN_RESERVATIONS)
sites = lire_csv(CHEMIN_SITES)
annee_actuelle = datetime.now().year


#fonctions

def compter_par(lignes, colonne):
    resultat = {}

    for ligne in lignes:
        valeur = ligne[colonne]
        resultat[valeur] = resultat.get(valeur, 0) + 1
    return resultat


def total_par(lignes, colonne_groupe, colonne_valeur):

    resultat = {}

    for ligne in lignes:
        groupe = ligne[colonne_groupe]
        valeur = int(ligne[colonne_valeur])
        resultat[groupe] = resultat.get(groupe, 0) + valeur

    return resultat



class Site:
    def __init__(self, code_site, nom, commune, annee_ouverture, surface_m2):
        self.code_site = code_site
        self.nom = nom
        self.commune = commune
        self.annee_ouverture = int(annee_ouverture)
        self.surface_m2 = int(surface_m2)

    def anciennete(self, annee_reference):
        if annee_reference < self.annee_ouverture:
            raise ValueError("Année de référence invalide")

        return annee_reference - self.annee_ouverture

    def __str__(self):
        return f"{self.code_site} - {self.nom} ({self.commune}), {self.surface_m2} m2"

#fonctions supplémentaires

def reservations_en_cours(reservations):
    liste_reservations = []

    for ligne in reservations:
        if not ligne["date_retour_reelle"]:
            liste_reservations.append(ligne)

    return liste_reservations

def nombre_ligne_par_fichier():
    print(f"Associations : {len(associations)} lignes")
    print(f"Matériel : {len(materiel)} lignes")
    print(f"Réservations : {len(reservations)} lignes")
    print(f"Sites : {len(sites)} lignes")


def creation_objet_de_classe_site():
    sites_objets = []

    for ligne in sites:
        site = Site(
            ligne["code_site"],
            ligne["nom"],
            ligne["commune"],
            ligne["annee_ouverture"],
            ligne["surface_m2"]
        )
        sites_objets.append(site)
    return sites_objets



def main():
    # Le nombre de lignes de chacun des quatre fichiers
    nombre_ligne_par_fichier()
    print("")
    print("-"*30)
    print("")
    # Les cinq objets Site avec leur ancienneté calculée pour 2026
    sites_objets = creation_objet_de_classe_site()
    for site in sites_objets:
        print(f"{site} - Ancienneté : {site.anciennete(annee_actuelle)} ans")
    print("")
    print("-"*30)
    print("")
    print(f"Nombre de réservations par code_site : ")
    # Le nombre de réservations par code_site, trié du plus grand au plus petit
    reservations_non_triées = compter_par(reservations, "code_site")
    reservations_par_site = sorted(reservations_non_triées.items(),
                                       key=lambda x: x[1],
                                       reverse=True)
    
    for site, nb in reservations_par_site:
        print(f"{site} : {nb}")

    print("")
    print("-"*30)
    print("")

    # La quantité totale réservée par code_site, triée du plus grand au plus petit
    print("Quantité totale réservée par code_site :")
    quantites_par_site = total_par(reservations, "code_site", "quantite")
    quantites_par_site = sorted(quantites_par_site.items(),
                                key=lambda x: x[1],
                                reverse=True)
    for site, quantite in quantites_par_site:
        print(f"{site} : {quantite}")

    print("")
    print("-"*30)
    print("")

    print(f"Nombre de matériel par état : ")
    # Le nombre de matériels par etat
    materiel_par_etat = compter_par(materiel, "etat")
    for etat, nb in materiel_par_etat.items():
        print(f"{etat} : {nb}")
    
    print("")
    print("-"*30)
    print("")

    # Le nombre de valeurs distinctes de categorie dans materiel.csv
    categories = {ligne["categorie"] for ligne in materiel}
    print(f"Nombre de catégories distinctes : {len(categories)}")

    print("")
    print("-"*30)
    print("")

    # Le nombre de réservations en cours
    print(f"Nombre de réservations en cours : {len(reservations_en_cours(reservations))}")

if __name__ == "__main__":
    main()