from pathlib import Path
import environ
import os
env = environ.Env(DEBUG=(bool, False) )

def key(env_key):
    env_key = str
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

    return env(f'{env_key}')


