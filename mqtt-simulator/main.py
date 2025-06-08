import argparse
import sys
from json import JSONDecodeError
from pathlib import Path

from pydantic import ValidationError as PydanticValidationError
from simulator import Simulator
from utils.exceptions.simulator_validation_error import SimulatorValidationError
from utils.print_validation_error import print_validation_error
from utils.read_publishers import read_publishers


def default_settings() -> Path:
    base_folder = Path(__file__).resolve().parent.parent
    settings_file = base_folder / "config/settings.json"
    return settings_file


def is_valid_file(arg: str) -> Path:
    settings_file = Path(arg)
    if not settings_file.is_file():
        raise argparse.ArgumentTypeError(f"argument -f/--file: can't open '{arg}'")
    return settings_file


parser = argparse.ArgumentParser()
parser.add_argument(
    "-f",
    "--file",
    dest="settings_file",
    type=is_valid_file,
    help="settings file path",
    default=default_settings(),
    metavar="",
)
parser.add_argument(
    "-v",
    "--verbose",
    dest="is_verbose",
    action="store_true",
    help="enable verbose output",
    default=False
)
args = parser.parse_args()

try:
    publishers = read_publishers(args.settings_file, args.is_verbose)
except (JSONDecodeError, PydanticValidationError, SimulatorValidationError) as e:
    print_validation_error(e)
    sys.exit(1)

simulator = Simulator(publishers)
simulator.run()
