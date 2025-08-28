
## Prerequisites

* [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Generating the client package in Python

(for reference, as the client package is already included in the git repository)

```sh
pip install openapi-python-client
openapi-python-client generate --url  https://oudonner.api.efs.sante.fr/carto-api/v3/swagger.json
```

## Retrieving all collection locations

Run this once to retrieve all collection locations in Brittany. All files will be stored in the `data` directory:

```sh
cd collecte-info
uv run get_lieux_collecte.py

## Extracting the list of postal codes

After executing the previous step:

```sh
uv run get_codes_postaux.py
```

The script returns a set of character strings.


# Using the collection API

## Nomenclature

| English  | French              | Description                                                                                                                         |
| -------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Region   | Région              | 13 regions containing a label, a 4-letter acronym, a single-letter monogram, and a 3-digit code stored as a string                  |
| Group    | Groupement          | Grouping of collection points, for example a municipality, a company, or a high school                                              |
| Location | Lieu de prélèvement | There may be several locations for the same group (e.g., Thorigné-Fouillard, because the collection took place in different rooms). |

## Searching for sampling locations

The location search uses the `/samplinglocations/` endpoint.

1. List all regions

https://oudonner.api.efs.sante.fr/carto-api/v3/samplinglocation/getregions

2. List all the _groups_ in a region

Example for Brittany:

https://oudonner.api.efs.sante.fr/carto-api/v3/samplinglocation/getgroupements?RegionCode=016

3. List all the collection points for a group

Example for Rennes-INSA:

https://oudonner.api.efs.sante.fr/carto-api/v3/samplinglocation/searchbygrouplocationcode?GroupCode=F70318

## Searching for a collection

The search for collections uses the endpoint `/samplingcollections/`.

It is _impossible_ to search by group or collection location; you must search:
* by postal code
* by city
* by geographic coordinates (around a point or within a square)

Example for postal code 35000:

https://oudonner.api.efs.sante.fr/carto-api/v3/samplingcollection/searchbypostcode?PostCode=35000&UserLatitude=48&UserLongitude=-2

The API returns:
* A list of fixed **collection locations** in the `samplingLocationEntities_SF` field
* A list of mobile collections in the `samplingLocationCollections` field

For each mobile collection, the following information is provided:
* The collection location
* A list of collections, each with metadata, including:
  * A unique ID
  * The date and time slots for collection
  * A direct registration link
  * The number of places for each type of sample

If a collection takes place on several dates, the collections for the following days appear in the `children` list of the collection corresponding to the first day. Example for collections in Liffré:

https://oudonner.api.efs.sante.fr/carto-api/v3/samplingcollection/searchbycityname?CityName=liffr%C3%A9&UserLatitude=48&UserLongitude=-2
