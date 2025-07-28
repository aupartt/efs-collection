import json
from pathlib import Path
from api_carto_client.models.sampling_location_entity import SamplingLocationEntity

LOCATIONS_FILE = Path("data/locations.jsonl")


if __name__ == "__main__":
    #check_api()

    postal_code = set()

    with LOCATIONS_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            location = SamplingLocationEntity.from_dict(json.loads(line))
            postal_code.add(location.post_code)

    print(postal_code)




