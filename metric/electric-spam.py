import helper.get_bulky
import helper.has_recovery
import helper.get_moves
from pokemon import Pokemon, Measure, get_pokemon_by_name
import helper
def electric_spam(poke: Pokemon) -> Measure:
    measure = 3
    # Is the pokemon immune to electric moves?
    if (poke.type1 == 'ground' or poke.type2 == 'ground' or poke.abilities.__contains__("Volt Absorb") or poke.abilities.__contains__("Motor Drive") or poke.abilities.__contains__("Lightning Rod")):
        return Measure(5)
    # The pokemon have a good spdef bulk?
    if (helper.get_bulky.get_bulky_spdef(poke) > 80):
        if (helper.has_recovery.has_recovery(poke.moves)):
            measure += 1
        measure += 1
    # The pokemon resist electric moves?