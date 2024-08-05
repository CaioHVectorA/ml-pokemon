import pandas as pd

def parse_pokemon_data(pokemon_str):
    lines = pokemon_str.strip().split('\n')
    name_item = lines[0].split('@')
    name = name_item[0].strip()
    item = name_item[1].strip()
    
    ability = lines[1].split(':')[1].strip()
    
    evs_line = lines[2].split(':')[1].strip().split('/')
    evs = {ev.split()[1]: int(ev.split()[0]) for ev in evs_line}
    
    nature = lines[3].split()[0]
    
    moves = [line.strip('- ') for line in lines[4:]]
    
    return {
        "Name": name,
        "Item": item,
        "Ability": ability,
        "EVs": evs,
        "Nature": nature,
        "Moves": moves
    }

pokemon_str = """Weavile @ Choice Band
Ability: Pressure
EVs: 252 Atk / 4 SpD / 252 Spe
Jolly Nature
- Beat Up
- Knock Off
- Triple Axel
- Ice Shard"""

weavile_data = parse_pokemon_data(pokemon_str)

# Create a DataFrame
data = {
    "Name": [weavile_data["Name"]],
    "Item": [weavile_data["Item"]],
    "Ability": [weavile_data["Ability"]],
    "Nature": [weavile_data["Nature"]],
    "Moves": [', '.join(weavile_data["Moves"])],  # Joining moves into a single string
}

# Add EVs to the DataFrame
for stat, value in weavile_data["EVs"].items():
    data[f"EV_{stat}"] = [value]

df = pd.DataFrame(data)

print(df)
