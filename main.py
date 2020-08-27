from pathlib import Path
from simulator import Simulator

settings_file = Path('./settings.json')

simulator = Simulator(settings_file)

simulator.run()
