import pandas as pd
from datetime import datetime

SITES = "./data/sites.csv"
MATERIEL = "./data/materiel.csv"
ASSOCIATIONS = "./data/associations.csv"
RESERVATIONS = "./data/reservations.csv"


df_sites = pd.read_csv(SITES)
df_materiel = pd.read_csv(MATERIEL)
df_associations = pd.read_csv(ASSOCIATIONS)
df_reservations = pd.read_csv(RESERVATIONS)

print("\n=== Materiel ===")



doublons = df_materiel[df_materiel.duplicated()]
print("\nDoublons stricts :", len(doublons))
print(doublons.head(3))
print("-------------")

annee_achat_vide = df_materiel[df_materiel["annee_achat"].isna()]
print("\nAnnées achats vide :", len(annee_achat_vide))
print(annee_achat_vide.head(3))
print("-------------")

annee_achat_impossible = datetime.now().year

annee_achat_impossible = df_materiel[
    df_materiel["annee_achat"] > annee_achat_impossible
]
print("\nAnnee d'achat impossible :", len(annee_achat_impossible))
print(annee_achat_impossible.head(3))
print("-------------")

valeur_achat_vide = df_materiel[df_materiel["valeur_achat"].isna()]
print("\nValeur d'achat vide :", len(valeur_achat_vide))
print(valeur_achat_vide.head(3))
print("-------------")

categorie_en_majuscule = df_materiel[
    df_materiel["categorie"].str.isupper()
]
print("\nCatégorie en majuscule :", len(categorie_en_majuscule))
print(categorie_en_majuscule.head(3))
print("-------------")

espaces_parasites = df_materiel[df_materiel["categorie"] != df_materiel["categorie"].str.strip()]
print("\nEspaces parasites :", len(espaces_parasites))
print(espaces_parasites.head(3))
print("-------------")

valeur_achat_avec_virgule = df_materiel[df_materiel["valeur_achat"].astype(str)
                                        .str.contains(",", na=False)
]
print("\nValeur d'achat contenant une virgule :", len(valeur_achat_avec_virgule))
print(valeur_achat_avec_virgule.head(3))
print("-------------")


print("\n=== Associations ===")


code_postal_vide = df_associations[df_associations["code_postal"].isna()| 
                                   (df_associations["code_postal"].astype(str).str.strip() == "")]

print("\nCode postal vide :", len(code_postal_vide))
print(code_postal_vide.head(3))
print("-------------")


type_association_inconnu = df_associations[
    df_associations["type_association"].str.lower() == "inconnu"
]
print("\nType association = inconnu :", len(type_association_inconnu))
print(type_association_inconnu.head(3))
print("-------------")


date_jjmmaaaa = df_associations[
    df_associations["date_convention"]
    .astype(str)
    .str.contains(r"^\d{2}/\d{2}/\d{4}$", regex=True, na=False)
]
print("\nDate convention au format JJ/MM/AAAA :", len(date_jjmmaaaa))
print(date_jjmmaaaa.head(3))
print("-------------")

print("\n=== Reservations ===")

doublons = df_reservations[df_reservations.duplicated()]
print("\nDoublons stricts :", len(doublons))
print(doublons.head(3))
print("-------------")


materiel_inexistant = df_reservations[~df_reservations["id_materiel"]
                                      .isin(df_materiel["id_materiel"])]

print("\nMatériel inexistant :", len(materiel_inexistant))
print(materiel_inexistant.head(3))
print("-------------")



retour_avant_debut = df_reservations[df_reservations["date_retour_reelle"] < df_reservations["date_debut"]]
print("\nRetour avant début :", len(retour_avant_debut))
print(retour_avant_debut.head(3))
print("-------------")


quantite_zero = df_reservations[
    df_reservations["quantite"] == 0
]
print("\nQuantité égale à zéro :", len(quantite_zero))
print(quantite_zero.head(3))
print("-------------")


print("\n=== Prêts en cours ===")
prets_en_cours_avant = df_reservations[
    df_reservations["date_retour_reelle"].isna()
]
print("Prêts en cours (cas métier normal) :", len(prets_en_cours_avant))
print("-------------")


masque_doublons_materiel = df_materiel.duplicated()
masque_annee_achat_vide = df_materiel["annee_achat"].isna()
masque_annee_achat_future = (
    df_materiel["annee_achat"] > datetime.now().year
)
masque_valeur_achat_vide = df_materiel["valeur_achat"].isna()
masque_categorie_majuscule = (
    df_materiel["categorie"].str.isupper().fillna(False)
)
masque_categorie_espaces = (
    df_materiel["categorie"]
    != df_materiel["categorie"].str.strip()
)
masque_valeur_achat_virgule = (
    df_materiel["valeur_achat"]
    .astype(str)
    .str.contains(",", na=False)
)

masque_code_postal_vide = (
    df_associations["code_postal"].isna()
    | (df_associations["code_postal"].astype(str).str.strip() == "")
)
masque_type_inconnu = (
    df_associations["type_association"].str.lower() == "inconnu"
)
masque_date_jjmmaaaa = (
    df_associations["date_convention"]
    .astype(str)
    .str.match(r"^\d{2}/\d{2}/\d{4}$", na=False)
)

masque_doublons_reservations = df_reservations.duplicated()
masque_materiel_inexistant = ~df_reservations["id_materiel"].isin(
    df_materiel["id_materiel"]
)
date_debut = pd.to_datetime(df_reservations["date_debut"], errors="coerce")
date_retour = pd.to_datetime(
    df_reservations["date_retour_reelle"], errors="coerce"
)
masque_retour_avant_debut = date_retour < date_debut
masque_quantite_zero = df_reservations["quantite"] == 0

anomalies_qualite = [
    ("materiel.csv", "toutes", "Lignes en doublon strict",
     int(masque_doublons_materiel.sum()), len(df_materiel),
     "Supprimer les occurrences répétées et conserver une ligne : elles n'apportent aucune information nouvelle."),
    ("materiel.csv", "annee_achat", "Année d'achat vide",
     int(masque_annee_achat_vide.sum()), len(df_materiel),
     "Conserver la valeur manquante, car aucune année fiable ne peut être déduite."),
    ("materiel.csv", "annee_achat", "Année d'achat postérieure à l'année courante",
     int(masque_annee_achat_future.sum()), len(df_materiel),
     "Remplacer l'année impossible par une valeur manquante et conserver le matériel, car l'année correcte est inconnue."),
    ("materiel.csv", "valeur_achat", "Valeur d'achat vide",
     int(masque_valeur_achat_vide.sum()), len(df_materiel),
     "Conserver la valeur manquante plutôt que d'inventer un montant."),
    ("materiel.csv", "categorie", "Catégorie écrite intégralement en majuscules",
     int(masque_categorie_majuscule.sum()), len(df_materiel),
     "Ramener la catégorie à son libellé homogène sans changer son sens."),
    ("materiel.csv", "categorie", "Espaces parasites autour de la catégorie",
     int(masque_categorie_espaces.sum()), len(df_materiel),
     "Supprimer les espaces en début et en fin pour uniformiser le libellé."),
    ("materiel.csv", "valeur_achat", "Valeur d'achat avec une virgule décimale",
     int(masque_valeur_achat_virgule.sum()), len(df_materiel),
     "Remplacer la virgule décimale par un point puis convertir en nombre."),
    ("associations.csv", "code_postal", "Code postal vide",
     int(masque_code_postal_vide.sum()), len(df_associations),
     "Conserver la valeur manquante, car le code postal ne peut pas être retrouvé de façon sûre."),
    ("associations.csv", "type_association", "Type d'association égal à inconnu",
     int(masque_type_inconnu.sum()), len(df_associations),
     "Conserver et signaler cette valeur pour vérification, sans inventer de type."),
    ("associations.csv", "date_convention", "Date au format JJ/MM/AAAA",
     int(masque_date_jjmmaaaa.sum()), len(df_associations),
     "Convertir la date en format ISO pour uniformiser la colonne."),
    ("reservations.csv", "toutes", "Lignes en doublon strict",
     int(masque_doublons_reservations.sum()), len(df_reservations),
     "Supprimer les occurrences répétées et conserver une ligne par réservation identique."),
    ("reservations.csv", "id_materiel", "Matériel inexistant",
     int(masque_materiel_inexistant.sum()), len(df_reservations),
     "Écarter ces réservations, car elles ne peuvent pas être reliées à un matériel existant."),
    ("reservations.csv", "date_retour_reelle", "Retour antérieur à la date de début",
     int(masque_retour_avant_debut.sum()), len(df_reservations),
     "Écarter ces réservations, car leur chronologie est impossible."),
    ("reservations.csv", "quantite", "Quantité égale à zéro",
     int(masque_quantite_zero.sum()), len(df_reservations),
     "Écarter ces réservations, car elles ne correspondent à aucun prêt de matériel."),
]


df_materiel_propre = df_materiel.drop_duplicates().copy()
df_materiel_propre.loc[
    df_materiel_propre["annee_achat"] > datetime.now().year,
    "annee_achat"
] = pd.NA
df_materiel_propre["annee_achat"] = pd.to_numeric(
    df_materiel_propre["annee_achat"], errors="coerce"
).astype("Int64")
df_materiel_propre["categorie"] = (
    df_materiel_propre["categorie"].str.strip().str.capitalize()
)
df_materiel_propre["valeur_achat"] = pd.to_numeric(
    df_materiel_propre["valeur_achat"]
    .astype("string")
    .str.replace(",", ".", regex=False),
    errors="coerce"
)

df_associations_propre = df_associations.copy()
date_convention_iso = (
    df_associations_propre["date_convention"].astype("string").str.strip()
)
date_convention_aaaa_mm_jj = pd.to_datetime(
    date_convention_iso, format="%Y-%m-%d", errors="coerce"
)
date_convention_jj_mm_aaaa = pd.to_datetime(
    date_convention_iso, format="%d/%m/%Y", errors="coerce"
)
df_associations_propre["date_convention"] = (
    date_convention_aaaa_mm_jj
    .fillna(date_convention_jj_mm_aaaa)
    .dt.strftime("%Y-%m-%d")
)

df_reservations_propre = df_reservations.drop_duplicates().copy()
df_reservations_propre = df_reservations_propre[
    df_reservations_propre["id_materiel"].isin(
        df_materiel_propre["id_materiel"]
    )
]
date_debut_propre = pd.to_datetime(
    df_reservations_propre["date_debut"], errors="coerce"
)
date_retour_propre = pd.to_datetime(
    df_reservations_propre["date_retour_reelle"], errors="coerce"
)
df_reservations_propre = df_reservations_propre[
    date_retour_propre.isna()
    | date_debut_propre.isna()
    | (date_retour_propre >= date_debut_propre)
]
df_reservations_propre = df_reservations_propre[
    df_reservations_propre["quantite"] != 0
]

prets_en_cours_apres = df_reservations_propre[
    df_reservations_propre["date_retour_reelle"].isna()
]
prets_en_cours_sans_materiel = prets_en_cours_avant[
    ~prets_en_cours_avant["id_materiel"].isin(
        df_materiel_propre["id_materiel"]
    )
]

df_materiel_propre.to_csv(
    "./sorties/materiel_propre.csv", index=False, encoding="utf-8"
)
df_associations_propre.to_csv(
    "./sorties/associations_propre.csv", index=False, encoding="utf-8"
)
df_reservations_propre.to_csv(
    "./sorties/reservations_propre.csv", index=False, encoding="utf-8"
)

rapport = []
rapport.append("# Rapport de qualité des données\n")
rapport.append("## Tableau récapitulatif des anomalies\n")
rapport.append(
    "| Fichier | Colonne | Description | Nombre de lignes | Part | Traitement retenu |"
)
rapport.append("|---|---|---|---:|---:|---|")

for fichier, colonne, description, nombre, total, traitement in anomalies_qualite:
    part = nombre / total * 100
    rapport.append(
        f"| {fichier} | {colonne} | {description} | {nombre} "
        f"| {part:.2f} % | {traitement} |"
    )

rapport.append("\n## Bilan par fichier\n")
rapport.append(
    f"### materiel.csv\n\nLignes avant nettoyage : {len(df_materiel)}. "
    f"Lignes après nettoyage : {len(df_materiel_propre)}."
)
rapport.append(
    f"\n### associations.csv\n\nLignes avant nettoyage : {len(df_associations)}. "
    f"Lignes après nettoyage : {len(df_associations_propre)}."
)
rapport.append(
    f"\n### reservations.csv\n\nLignes avant nettoyage : {len(df_reservations)}. "
    f"Lignes après nettoyage : {len(df_reservations_propre)}."
)

rapport.append("\n## Prêts en cours\n")
rapport.append(
    f"Avant nettoyage : {len(prets_en_cours_avant)} prêts en cours. "
    f"Après nettoyage : {len(prets_en_cours_apres)}."
)
rapport.append(
    f"L'écart s'explique par {len(prets_en_cours_sans_materiel)} prêt(s) "
    "en cours associé(s) à un matériel inexistant, écarté(s) avec les autres "
    "réservations sans matériel correspondant."
)
rapport.append(
    "Les dates de retour vides sont des prêts en cours normaux et ne sont "
    "pas comptées comme des anomalies."
)

rapport.append("\n## Points d'attention pour la direction\n")
rapport.append(
    f"- L'inventaire contenait {len(df_materiel)} lignes ; "
    f"{len(df_materiel_propre)} matériels restent après nettoyage."
)
rapport.append(
    "- Les doublons exacts ont été retirés afin de ne pas compter deux fois "
    "le même matériel ou la même réservation."
)
rapport.append(
    f"- Les catégories de matériel sont désormais regroupées sous "
    f"{df_materiel_propre['categorie'].nunique()} libellés homogènes."
)
rapport.append(
    "- Les années ou valeurs d'achat manquantes restent vides ; aucune "
    "information n'a été inventée."
)
rapport.append(
    f"- {int(masque_code_postal_vide.sum())} associations n'ont pas de code "
    "postal et devront être vérifiées."
)
rapport.append(
    f"- {int(masque_materiel_inexistant.sum())} réservations désignent un "
    "matériel absent de l'inventaire et ont été écartées."
)
rapport.append(
    f"- Les prêts en cours passent de {len(prets_en_cours_avant)} à "
    f"{len(prets_en_cours_apres)} : un prêt concernait un matériel absent."
)

with open("./sorties/rapport_qualite.md", "w", encoding="utf-8") as fichier:
    fichier.write("\n".join(rapport) + "\n")

print("\n=== Fichiers nettoyés ===")
print("Materiel :", len(df_materiel_propre), "lignes")
print("Associations :", len(df_associations_propre), "lignes")
print("Reservations :", len(df_reservations_propre), "lignes")
print("Rapport généré : sorties/rapport_qualite.md")