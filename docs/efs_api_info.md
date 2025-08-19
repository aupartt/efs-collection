
## Pré-requis

* [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Génération du package client en Python

(pour référence, car le package client est déjà inclus dans le dépôt git)

```sh
pip install openapi-python-client
openapi-python-client generate --url  https://oudonner.api.efs.sante.fr/carto-api/v3/swagger.json
```

## Récupération de tous les lieux de collecte

A exécuter une seule fois pour récupérer tous les lieux de collecte de Bretagne, tous les fichiers seront stockés dans le répertoire `data` :

```sh
cd collecte-info
uv run get_lieux_collecte.py
```

## Extraction de la liste des codes postaux

Après exécution de l'étape précédente :

```sh
uv run get_codes_postaux.py
```

Le script retourne un ensemble de chaînes de caractères.


# Utilisation de l'API collecte

## Nomenclature

| Anglais | Français | Description |
|---|---|---|
| Region | Région | 13 régions contenant un libellé, un acronyme à 4 lettres, un monogramme d'une seule lettre et un code à 3 chiffres stocké sous forme de string |
| Group | Groupement | Groupement de lieux de collectes, par exemple une commune, une entreprise ou un lycée |
| Location | Lieu de prélèvement | On peut avoir plusieurs lieux pour un même groupement (ex. Thorigné-Fouillard car la collecte a eu lieu dans différentes salles) |

## Recherche de lieux de prélèvement

La recherche de lieux utilise l'endpoint `/samplinglocations/`.

1. Lister toutes les régions

https://oudonner.api.efs.sante.fr/carto-api/v3/samplinglocation/getregions

2. Lister tous les _groupements_ d'une région

Exemple pour la Bretagne : 

https://oudonner.api.efs.sante.fr/carto-api/v3/samplinglocation/getgroupements?RegionCode=016

3. Lister tous les _lieux de collecte_ d'un groupement

Exemple pour Rennes-INSA :

https://oudonner.api.efs.sante.fr/carto-api/v3/samplinglocation/searchbygrouplocationcode?GroupCode=F70318

## Recherche d'une collecte

La recherche de collectes utilise l'endpoint `/samplingcollections/`.

C'est _a priori impossible_ par groupement ou par lieu de collecte, il faut chercher :
* par code postal
* par ville
* par coordonnées géographiques (autour d'un point ou dans un carré)

Exemple pour le code postal 35000 :

https://oudonner.api.efs.sante.fr/carto-api/v3/samplingcollection/searchbypostcode?PostCode=35000&UserLatitude=48&UserLongitude=-2

L'API retourne :
* Une liste des **lieux de collecte** fixes dans le champ `samplingLocationEntities_SF`
* Une liste de collectes mobiles dans le champ `samplingLocationCollections`

Pour chaque collecte mobile, on retrouve :
* Le lieu de collecte
* Une liste de collectes ayant chacune des métadonnes, notamment :
  * Un ID unique
  * La date et les créneaux horaires de collecte
  * Un lien direct d'inscription
  * Le nombre de places pour chaque type de prélèvement

Si une collecte est sur plusieurs dates, les collectes des jours suivants apparaissent dans la liste `children` de la collecte correspondant au premier jour. Exemple pour les collectes de Liffré :

https://oudonner.api.efs.sante.fr/carto-api/v3/samplingcollection/searchbycityname?CityName=liffr%C3%A9&UserLatitude=48&UserLongitude=-2
