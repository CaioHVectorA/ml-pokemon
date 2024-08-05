from typing import List
from pokemon import Pokemon


def get_moves(pokemon: Pokemon) -> List[str]:
    moves = []
    for move in pokemon.moves:
        moves.append(move['move']['name'])
    return moves