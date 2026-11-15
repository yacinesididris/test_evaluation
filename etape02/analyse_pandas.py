import pandas as pd


SITES = "./data/sites.csv"
MATERIEL = "./data/materiel.csv"
ASSOCIATIONS = "./data/associations.csv"
RESERVATIONS = "./data/reservations.csv"


df_sites = pd.read_csv(SITES)
df_materiel = pd.read_csv(MATERIEL)

# Comme il y'a plusieurs ponctuations différentes (. et ,) pandas convertit la colonne en str. On corrige ca
df_materiel["valeur_achat"] = pd.to_numeric(df_materiel["valeur_achat"].str.replace(",", "."), errors="coerce")

# On supprime également les doublons dans df_materiel

df_materiel = df_materiel.drop_duplicates(subset="id_materiel")

df_associations = pd.read_csv(ASSOCIATIONS)
df_reservations = pd.read_csv(RESERVATIONS)


df_reservations["date_debut"] = pd.to_datetime(df_reservations["date_debut"])
df_reservations["date_retour_reelle"] = pd.to_datetime(df_reservations["date_retour_reelle"])
df_reservations["date_fin_prevue"] = pd.to_datetime(df_reservations["date_fin_prevue"])

#   Affichez pour df_materiel et df_reservations : la forme (shape), le résultat de info(), et le nombre de valeurs manquantes par colonne.

print("\n=== Formes des DATAFRAMES ===")

print("\nForme du dataframe materiel : ", df_materiel.shape)
print("Forme du dataframe reservations : ", df_reservations.shape)


print("\n=== INFO MATERIEL ===")
df_materiel.info()

print("\n=== INFO RESERVATIONS ===")
df_reservations.info()


print("\n=== VALEURS MANQUANTES MATERIEL ===")
print(df_materiel.isna().sum())

print("\n=== VALEURS MANQUANTES RESERVATIONS ===")
print(df_reservations.isna().sum())


# les 10 matériels les plus chers (reference, designation, categorie, valeur_achat), triés par valeur décroissante
df_top_10 = df_materiel.sort_values("valeur_achat", ascending=False).head(10)
df_top_10[["reference", "designation", "categorie", "valeur_achat"]]

print("\n=== Les 10 matériels les plus chers ===")
print("\n", df_top_10)

# le nombre de matériels par categorie, trié du plus fréquent au moins fréquent

nb_par_categorie = (
    df_materiel["categorie"]
    .value_counts()
    .reset_index()
)

nb_par_categorie.columns = ["categorie", "nombre_materiels"]

print("\n=== Nombre de matériels par categorie ===")
print(nb_par_categorie)

# le nombre de réservations et la quantité totale par code_site, en une seule opération groupby, triés par nombre de réservations décroissant.

reservation_et_quantite_totale = (df_reservations.groupby("code_site")
            .agg(nombre_reservations=("code_site", "count"),
                 quantite_totale=("quantite", "sum")
                 )
            .sort_values("nombre_reservations", ascending=False)
            )

print("\n=== Nombre de réservations et quantité totale par code_site ===")
print("\n", reservation_et_quantite_totale)

# Construisez df_complet en fusionnant df_reservations avec df_materiel sur id_materiel, 
# puis avec df_associations sur id_association, en jointure left depuis les réservations. 
# Affichez le nombre de lignes de df_complet et le nombre de lignes sans matériel correspondant.

df_complet = (
    df_reservations
    .merge(df_materiel, on="id_materiel", how="left")
    .merge(df_associations, on="id_association", how="left")
)

print("\n=== DATAFRAME df_complet ===")
print("\n Nombre de lignes : ", len(df_complet))
print("Nombre de lignes sans matériel correspondant : ", df_complet["reference"].isna().sum())


# À partir de df_complet, produisez le top 10 des matériels les 
# plus réservés (id_materiel, designation, nombre de réservations) et 
# exportez-le dans sorties/top10_materiel.csv, sans index, en UTF-8.

df_complet_top_10 = (df_complet.groupby(["id_materiel", "designation"])
                                .size()
                                .reset_index(name="nombre_reservations")
                                .sort_values("nombre_reservations", ascending=False)
                                .head(10)
)

df_complet_top_10.to_csv("sorties/top10_materiel.csv", index=False, encoding="utf-8")

print(df_complet_top_10.shape)