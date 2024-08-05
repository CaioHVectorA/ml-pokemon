from typing import List
def has_recovery(data: List[str]) -> bool:
# slack off, recover, soft-boiled, morning sun, synthesis, wish, rest, moonlight, milk drink, shore up
    recoverys = ['slack off', 'recover', 'soft-boiled', 'morning sun', 'synthesis', 'wish', 'rest', 'moonlight', 'milk drink', 'shore up']
    for line in data:
        for recovery in recoverys:
            if recovery in line:
                return True
    return False