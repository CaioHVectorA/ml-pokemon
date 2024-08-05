from typing import List, Optional, TypedDict
import requests
import pandas as pd
from enum import Enum

class Measure(Enum):
    # see measure.md
    FATAL = 1
    WEAK = 2
    NORMAL = 3
    STRONG = 4
    HARD_COUNTER = 5
    
class _Move(TypedDict):
    name: str
    url: str

class _Mfe(TypedDict):
    move: _Move


class Pokemon:
    moves: List[_Mfe] = []
    def __init__(self, abilities: List[str], against_bug: float, against_dark: float, against_dragon: float, against_electric: float, against_fairy: float, against_fight: float, against_fire: float, against_flying: float, against_ghost: float, against_grass: float, against_ground: float, against_ice: float, against_normal: float, against_poison: float, against_psychic: float, against_rock: float, against_steel: float, against_water: float, attack: int, base_egg_steps: int, base_happiness: int, base_total: int, capture_rate: int, classification: str, defense: int, experience_growth: str, height_m: float, hp: int, japanese_name: str, name: str, percentage_male: float, pokedex_number: int, sp_attack: int, sp_defense: int, speed: int, type1: str, type2: Optional[str], weight_kg: float, generation: int, is_legendary: bool):
        self.abilities = abilities
        self.against_bug = against_bug
        self.against_dark = against_dark
        self.against_dragon = against_dragon
        self.against_electric = against_electric
        self.against_fairy = against_fairy
        self.against_fight = against_fight
        self.against_fire = against_fire
        self.against_flying = against_flying
        self.against_ghost = against_ghost
        self.against_grass = against_grass
        self.against_ground = against_ground
        self.against_ice = against_ice
        self.against_normal = against_normal
        self.against_poison = against_poison
        self.against_psychic = against_psychic
        self.against_rock = against_rock
        self.against_steel = against_steel
        self.against_water = against_water
        self.attack = attack
        self.base_egg_steps = base_egg_steps
        self.base_happiness = base_happiness
        self.base_total = base_total
        self.capture_rate = capture_rate
        self.classification = classification
        self.defense = defense
        self.experience_growth = experience_growth
        self.height_m = height_m
        self.hp = hp
        self.japanese_name = japanese_name
        self.name = name
        self.percentage_male = percentage_male
        self.pokedex_number = pokedex_number
        self.sp_attack = sp_attack
        self.sp_defense = sp_defense
        self.speed = speed
        self.type1 = type1
        self.type2 = type2
        self.weight_kg = weight_kg
        self.generation = generation
        self.is_legendary = is_legendary

def get_pokemon_by_index(index: int) -> Pokemon:
    pokemon = pd.read_csv('./data/pokemon.csv')
    data = pokemon.loc[index].astype(str)
    data['moves'] = requests.api.get(f"https://pokeapi.co/api/v2/pokemon/{data['name'].lower()}").json()['moves']
    return data

def get_pokemon_by_name(name: str) -> Pokemon:
    data = requests.api.get(f"https://pokeapi.co/api/v2/pokemon/{name}").json()
    res = get_pokemon_by_index(data['id'] - 1)
    return res