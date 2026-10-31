import os
from datetime import datetime
from pathlib import Path

import requests

from ..internal import constants


class APIException(Exception):
    def __init__(self, *args) -> None:
        super().__init__(*args)


def download(day_number: int) -> None:
    now = datetime.now()
    if now < datetime(constants.YEAR, constants.MONTH, day_number):
        raise APIException(f'Too early to download day {day_number}')
    if not os.getenv('AOC_SESSION'):
        raise APIException('AOC_SESSION environment variable not found')
    try:
        filepath = Path('inputs') / f'd{day_number:0>2}.in'
        if not filepath.parent.exists():
            filepath.parent.mkdir()
        if filepath.exists():
            _print_file(filepath)
            print(f'File {filepath} exists')
        else:
            response = requests.get(
                f'{constants.URL}/day/{day_number}/input',
                headers={'User-Agent': constants.USER_AGENT},
                cookies={'session': os.getenv('AOC_SESSION')},
            )

            if not response.ok:
                print(f'Error in retrieving input: Code {response.status_code}')
                match response.status_code:
                    case 400:
                        print('Try resetting session cookie')
                    case 404:
                        print('Too soon, try again later')
                response.raise_for_status()

            _create_file(filepath, response.text)
            _print_file(filepath)
            print(f'File saved as {filepath}')
    except KeyError as e:
        print(f'Missing environment variable {e}')
        raise


def _create_file(filename, data) -> None:
    with open(filename, 'w') as f:
        f.write(data)


def _print_file(filename) -> None:
    with open(filename) as f:
        print(f.read())
