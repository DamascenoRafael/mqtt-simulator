from pathlib import Path
from simulator import Simulator

base_folder = Path(__file__).resolve().parent.parent
settings_file = base_folder / 'config/settings.json'

simulator = Simulator(settings_file)

simulator.run()
