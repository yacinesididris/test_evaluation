# Rapport de qualité des données

## Tableau récapitulatif des anomalies

| Fichier | Colonne | Description | Nombre de lignes | Part | Traitement retenu |
|---|---|---|---:|---:|---|
| materiel.csv | toutes | Lignes en doublon strict | 7 | 1.91 % | Supprimer les occurrences répétées et conserver une ligne : elles n'apportent aucune information nouvelle. |
| materiel.csv | annee_achat | Année d'achat vide | 9 | 2.45 % | Conserver la valeur manquante, car aucune année fiable ne peut être déduite. |
| materiel.csv | annee_achat | Année d'achat postérieure à l'année courante | 5 | 1.36 % | Remplacer l'année impossible par une valeur manquante et conserver le matériel, car l'année correcte est inconnue. |
| materiel.csv | valeur_achat | Valeur d'achat vide | 11 | 3.00 % | Conserver la valeur manquante plutôt que d'inventer un montant. |
| materiel.csv | categorie | Catégorie écrite intégralement en majuscules | 6 | 1.63 % | Ramener la catégorie à son libellé homogène sans changer son sens. |
| materiel.csv | categorie | Espaces parasites autour de la catégorie | 5 | 1.36 % | Supprimer les espaces en début et en fin pour uniformiser le libellé. |
| materiel.csv | valeur_achat | Valeur d'achat avec une virgule décimale | 5 | 1.36 % | Remplacer la virgule décimale par un point puis convertir en nombre. |
| associations.csv | code_postal | Code postal vide | 9 | 4.29 % | Conserver la valeur manquante, car le code postal ne peut pas être retrouvé de façon sûre. |
| associations.csv | type_association | Type d'association égal à inconnu | 7 | 3.33 % | Conserver et signaler cette valeur pour vérification, sans inventer de type. |
| associations.csv | date_convention | Date au format JJ/MM/AAAA | 6 | 2.86 % | Convertir la date en format ISO pour uniformiser la colonne. |
| reservations.csv | toutes | Lignes en doublon strict | 18 | 0.39 % | Supprimer les occurrences répétées et conserver une ligne par réservation identique. |
| reservations.csv | id_materiel | Matériel inexistant | 21 | 0.45 % | Écarter ces réservations, car elles ne peuvent pas être reliées à un matériel existant. |
| reservations.csv | date_retour_reelle | Retour antérieur à la date de début | 15 | 0.32 % | Écarter ces réservations, car leur chronologie est impossible. |
| reservations.csv | quantite | Quantité égale à zéro | 6 | 0.13 % | Écarter ces réservations, car elles ne correspondent à aucun prêt de matériel. |

## Bilan par fichier

### materiel.csv

Lignes avant nettoyage : 367. Lignes après nettoyage : 360.

### associations.csv

Lignes avant nettoyage : 210. Lignes après nettoyage : 210.

### reservations.csv

Lignes avant nettoyage : 4618. Lignes après nettoyage : 4560.

## Prêts en cours

Avant nettoyage : 72 prêts en cours. Après nettoyage : 71.
L'écart s'explique par 1 prêt(s) en cours associé(s) à un matériel inexistant, écarté(s) avec les autres réservations sans matériel correspondant.
Les dates de retour vides sont des prêts en cours normaux et ne sont pas comptées comme des anomalies.

## Points d'attention pour la direction

- L'inventaire contenait 367 lignes ; 360 matériels restent après nettoyage.
- Les doublons exacts ont été retirés afin de ne pas compter deux fois le même matériel ou la même réservation.
- Les catégories de matériel sont désormais regroupées sous 6 libellés homogènes.
- Les années ou valeurs d'achat manquantes restent vides ; aucune information n'a été inventée.
- 9 associations n'ont pas de code postal et devront être vérifiées.
- 21 réservations désignent un matériel absent de l'inventaire et ont été écartées.
- Les prêts en cours passent de 72 à 71 : un prêt concernait un matériel absent.
