import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from pokemon import Pokemon

def get_bulky_def(pokemon: Pokemon):
    return float(pokemon.hp) * float(pokemon.defense) / 100

def get_bulky_spdef(pokemon: Pokemon):
    return float(pokemon.hp) * float(pokemon.sp_defense) / 100

def get_bulky(pokemon: Pokemon):
    return (get_bulky_def(pokemon) + get_bulky_spdef(pokemon)) / 2