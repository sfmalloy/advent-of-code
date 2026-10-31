import importlib
import sys
from pathlib import Path

from dotenv import load_dotenv
from requests import HTTPError

from .lib import advent
from .lib.internal import constants
from .lib.internal.api import APIException, download
from .lib.internal.cmdline import load_arguments
from .lib.internal.printer import print_table
from .lib.internal.runner import DayNotFoundException, DuplicateKeyError


def main() -> None:
    load_dotenv()
    MIN_MINOR_VERSION = 15
    if sys.version_info.minor < MIN_MINOR_VERSION:
        print(f'Min version Python 3.{MIN_MINOR_VERSION} required')
        sys.exit()
    try:
        run()
    except DayNotFoundException as err:
        print(err)
    except DuplicateKeyError as err:
        print(err)
        print(f'Found duplicate solution key {err.key}')
    except APIException as err:
        print(err)
    except HTTPError:
        pass


def run() -> None:
    # importing dynamically so "unused" import isn't removed by accident
    importlib.import_module('aoc2026.solutions')
    args = load_arguments()
    if args.day:
        if args.generate_day:
            path = Path('src/aoc2026/solutions') / f'd{args.day:0>2}.py'
            if not path.parent.exists():
                path.parent.mkdir()
            if not path.exists():
                with open(path, 'w') as f:
                    f.write(constants.solution_template(args.day))
        if args.download_input:
            res = download(args.day)
        if not args.download_input and not args.generate_day:
            file = 'test.in' if args.use_test_input else args.file
            res = advent.run(args.day, file, args.num_runs, args.hide, args.part)
            print_table([res])
    elif args.run_all:
        res = advent.run_all(args.num_runs, args.hide)
        print_table(res)
