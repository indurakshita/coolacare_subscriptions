import time
from termcolor import colored
from decouple import config
from .base import *

def animate(message):
    chars = "/—\|"
    for char in chars:
        print('\r' + message + ' ' + colored(char, 'yellow'), end='', flush=True)
        time.sleep(0.1)
    print('\r' + message + ' ' + colored('Done!', 'green'))

# Load the project variable from the .env file
project = config('project', default='prod')

# Determine which settings to import based on the project variable
if project == 'dev':
    print(colored("Running development...", 'green'))
    from .dev import *
else:
    print(colored("Running production...", 'green'))
    from .prod import *

# Example animation
animate("Starting servers")


