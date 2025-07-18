import json
from pathlib import Path
from api_carto_client import Client
from api_carto_client.models.ping import Ping
from api_carto_client.models.sampling_region_entity import SamplingRegionEntity
from api_carto_client.models.sampling_group_entity import SamplingGroupEntity
from api_carto_client.api.ping import get_carto_api_v3_ping as api_ping
from api_carto_client.api.sampling_location import get_carto_api_v3_samplinglocation_getregions as api_get_regions
from api_carto_client.api.sampling_location import get_carto_api_v3_samplinglocation_getgroupements as api_get_groupements
from api_carto_client.api.sampling_location import get_carto_api_v3_samplinglocation_searchbygrouplocationcode as api_search_location

FICHIER_GROUPEMENTS = "data/groupements.json"
PREFIXE_LIEUX = "data/groupement_"

def with_api_client(func):
    def wrapper(*args, **kwargs):
        client = Client(base_url="https://oudonner.api.efs.sante.fr/")
        with client as cli:
            return func(client, *args, **kwargs)
    return wrapper


@with_api_client
def check_api(client: Client):
    ping_resp: ping = api_ping.sync(client=client)
    if ping_resp.version != "v3":
        raise Exception(f"Le serveur exécute l'API en {ping_resp.version}, mais seule la v3 est supportée")

@with_api_client
def get_region(client: Client, nom: str) -> SamplingRegionEntity:
    """Retourne une région définie par son nom"""
    regions: list[SamplingRegionEntity] = api_get_regions.sync(client=client)

    for region in regions:
        if region.libelle == nom:
            print(region)
            return region

    return None

@with_api_client
def get_groupements(client: Client, region: SamplingRegionEntity):
    """Retourne tous les groupements d'une région"""
    groupements: list[SamplingGroupEntity] = api_get_groupements.sync(client=client, region_code=region.code)
    return groupements
    
@with_api_client
def get_lieux_prelevement(client: Client, groupement: SamplingGroupEntity):
    """Retourne tous les lieux de prélèvement d'un groupement"""
    res: sampling_location_result = api_search_location.sync(client=client, group_code=groupement.gr_code)
    return res.sampling_location_entities


if __name__ == "__main__":
    #check_api()

    groupements: list[SamplingGroupEntity] = []

    fichier_groupements = Path(FICHIER_GROUPEMENTS)
    if fichier_groupements.is_file():
        print("Chargement des groupements depuis le fichier")
        with fichier_groupements.open("r", encoding="utf-8") as fp:
            for line in fp:
                groupement = SamplingGroupEntity.from_dict(json.loads(line))
                groupements.append(groupement)

    else:
        print("Chargement des groupements depuis l'API")

        region_bretagne: SamplingRegionEntity = get_region(nom="Bretagne")
        if region_bretagne is None:
            print("Impossible de télécharger l'identifiant de la région Bretagne")

        with fichier_groupements.open("w", encoding="utf-8") as fp:
            groupements = get_groupements(region=region_bretagne)
            for groupement in groupements:
                fp.write(json.dumps(groupement.to_dict(), indent=None))
                fp.write("\n")

    print(f"Groupements en Bretagne: {len(groupements)}")

    for groupement in groupements:
        fichier_lieux = Path(f"{PREFIXE_LIEUX}_{groupement.gr_code}.json")
        if fichier_lieux.is_file() and fichier_lieux.stat().st_size > 0:
            pass
        else:
            print(f"Téléchargement des lieux de {groupement.gr_code}")

            with fichier_lieux.open("w", encoding="utf-8") as fp:
                lieux = get_lieux_prelevement(groupement=groupement)

                for lieu in lieux:
                    if lieu.post_code[0:2] not in ["22","29","35","56"]:
                        print(f"Code postal inattendu dans le groupement {groupement.gr_lib}: '{lieu.post_code}'")
                    else:
                        fp.write(json.dumps(lieu.to_dict(), indent=None))
                        fp.write("\n")





