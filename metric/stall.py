import helper.get_bulky
import helper.has_recovery
import helper.get_moves
from pokemon import Pokemon, Measure, get_pokemon_by_name
import helper
def stall(poke: Pokemon) -> Measure:
    # returns 1 to 5 a potential of a poke to pass stall
    measure: int = 2
    # Is the pokemon strong against toxic or chip damage?
    if (poke.type1 == 'steel' or poke.type2 == 'poison' or poke.type1 == 'poison' or poke.type2 == 'steel' or poke.abilities.__contains__("Magic Guard") or poke.abilities.__contains__("Natural Cure") or poke.abilities.__contains__("Regenerator") or poke.abilities.__contains__("Poison Heal") or poke.abilities.__contains__("Shed Skin") or poke.abilities.__contains__("Magic Bounce")):
        measure += 2
    # Is the pokemon strong enough to act as a wallbreaker
    if (int(poke.attack) < 120 or int(poke.sp_attack) < 120):
        measure -= 1
    else:
        measure += 1
    # Is the pokemon bulky enough to take hits?
    print(helper.get_bulky.get_bulky(poke))
    if (helper.get_bulky.get_bulky(poke) > 60):
        if (helper.has_recovery.has_recovery(poke.moves)):
            measure += 2
        measure += 1
    else:
        measure -= 1
    # Can the pokemon trap with a good move like magma storm?
    if (helper.get_moves.get_moves(poke).__contains__("magma-storm") or helper.get_moves.get_moves(poke).__contains__("whirlpool") or helper.get_moves.get_moves(poke).__contains__("wrap") or helper.get_moves.get_moves(poke).__contains__("fire Spin") or helper.get_moves.get_moves(poke).__contains__("sand tomb") or helper.get_moves.get_moves(poke).__contains__("infestation")):
        # And its have taunt?
        if (helper.get_moves.get_moves(poke).__contains__("taunt")):
            measure += 2
        measure += 0.5
    return Measure(max(1, min(5, round(measure, 0))))


