import argparse
import asyncio
import json

from collecte.tasks.collections import update_collections
from collecte.tasks.groups import update_groups
from collecte.tasks.locations import update_locations
from collecte.tasks.schedules import update_schedules

parser = argparse.ArgumentParser(prog="collecte-info", description="Collecte info CLI")
parser.add_argument(
    "--groups",
    "-g",
    action="store_true",
    help="Run the task to retrieve and save new groups",
)
parser.add_argument(
    "--locations",
    "-l",
    action="store_true",
    help="Run the task to retrieve and save new locations",
)
parser.add_argument(
    "--collections",
    "-c",
    action="store_true",
    help="Run the task to retrieve and save new collections",
)
parser.add_argument(
    "--schedules",
    "-s",
    action="store_true",
    help="Run the task to retrieve and save new schedules",
)
parser.add_argument(
    "--file",
    "-f",
    default=None,
    help="The path and name of the JSON file",
)
parser.add_argument(
    "--format",
    "-F",
    choices=['JSON', 'JSONL'],
    default='JSONL',
    help="Format of the JSON data [JSON, JSONL]",
)


def load_data(fila_path: str, file_type: str = "JSONL"):
    with open(fila_path) as file:
        if file_type == "JSON":
            return json.load(file)
        return [json.loads(line) for line in file.readlines()]
        

async def main(params: argparse.Namespace):
    data = None

    if params.file:
        data = load_data(params.file, params.format)
    if params.groups:
        await update_groups(data)
    elif params.locations:
        await update_locations(data)
    elif params.collections:
        await update_collections(data)
    elif params.schedules:
        await update_schedules(data)


if __name__ == "__main__":
    args = parser.parse_args()

    asyncio.run(main(args))
