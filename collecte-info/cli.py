import argparse
import asyncio

from collecte.tasks.collections import update_collections
from collecte.tasks.groups import update_groups
from collecte.tasks.locations import update_locations
from collecte.tasks.schedules import update_schedules

parser = argparse.ArgumentParser("Collecte info CLI")
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


async def main(params: argparse.Namespace):
    if params.groups:
        await update_groups()
    if params.locations:
        await update_locations()
    if params.collections:
        await update_collections()
    if params.schedules:
        await update_schedules()


if __name__ == "__main__":
    args = parser.parse_args()

    asyncio.run(main(args))
