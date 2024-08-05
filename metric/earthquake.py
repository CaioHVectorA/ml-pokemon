from pokemon import Pokemon, get_pokemon_by_name, Measure
def measure_earthquake(poke: Pokemon) -> Measure:
    measure: int = 3
    if (poke.type1 == 'flying' or poke.type2 == 'flying' or poke.abilities.find('levitate') != -1):
        return Measure.HARD_COUNTER
    measure /= poke.against_ground
    bulk = (poke.defense * poke.hp) / 100 # bulk is a measure of how much damage a pokemon can take in ~ 30 - 200
    measure *= max(0.5, bulk / 100)
    return Measure(max(1, min(5, round(measure, 0))))
