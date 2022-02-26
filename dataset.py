import csv
import datetime
import os
import shutil
import typing

import requests

from models.moer import MOER

DATASET_URL = 'https://raw.githubusercontent.com/WattTime/software_modeling/master/MOERS.csv'
DATASET_DIR = 'data'
FILE_NAME = 'MOERS.csv'
DATASET_FILEPATH = f'{DATASET_DIR}/{FILE_NAME}'


def download_dataset():
    """
    Downloads the dataset if DNE or uses the one on disk
    :return: None
    """

    if os.path.exists(DATASET_FILEPATH):
        return

    if os.path.exists(DATASET_DIR):
        try:
            shutil.rmtree(DATASET_DIR)
        except NotADirectoryError:
            os.remove(DATASET_DIR)

    os.mkdir(DATASET_DIR)

    if not os.path.exists(DATASET_FILEPATH):
        response = requests.get(DATASET_URL)
        response.raise_for_status()

        with open(DATASET_FILEPATH, 'w') as f:
            f.write(response.content.decode())


def more_moer(
        start_dt: typing.Optional[datetime.datetime] = None,
        end_dt: typing.Optional[datetime.datetime] = None,
        header_rows: int = 0,
) -> typing.List[MOER]:
    """
    Generator function that yields the next set(hour) of MOERs
    :param start_dt: ignores MOERs before this time
    :param end_dt: ignores MOERs after this time
    :param header_rows: optional number of rows to skip
    :return: list of MOERs
    """
    with open(DATASET_FILEPATH, 'r') as f:
        # skip headers
        for _ in range(0, header_rows):
            f.readline()

        fieldnames = ['timestamp', 'moer']
        reader = csv.DictReader(f, fieldnames=fieldnames)

        def should_add_moer(m: MOER):
            if not any((start_dt, end_dt)):
                return True

            if start_dt <= m.timestamp <= end_dt:
                return True

            return False

        hour_of_moers = []
        for item in reader:
            next_moer = MOER(**item)

            if len(hour_of_moers) < 12:
                if should_add_moer(next_moer):
                    hour_of_moers.append(next_moer)
            else:
                yield hour_of_moers
                hour_of_moers = []

        yield hour_of_moers
