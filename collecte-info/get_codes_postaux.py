import json
from pathlib import Path
from api_carto_client.models.sampling_location_entity import SamplingLocationEntity

PREFIXE_LIEUX = "data/groupement_"


if __name__ == "__main__":
    #check_api()

    pwd = Path.cwd()
    fichiers_lieux = pwd.glob(f"{PREFIXE_LIEUX}*.json")

    codes_postaux = set()

    for fichier_lieux in fichiers_lieux:
        with fichier_lieux.open("r", encoding="utf-8") as fp:
            for line in fp:
                lieu = SamplingLocationEntity.from_dict(json.loads(line))
                codes_postaux.add(lieu.post_code)

    print(codes_postaux)




