import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
import sys
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from random import randrange
types = [
    'fire',
    'water',
    'grass',
    'electric',
    'psychic',
    'ice',
    'dragon',
    'dark',
    'fairy',
    'normal',
    'fighting',
    'flying',
    'poison',
    'ground',
    'rock',
    'bug',
    'ghost',
    'steel'
]
weaknesses = {
    'fire': ['water', 'ground', 'rock'],
    'water': ['electric', 'grass'],
    'grass': ['fire', 'ice', 'poison', 'flying', 'bug'],
    'electric': ['ground'],
    'psychic': ['bug', 'ghost', 'dark'],
    'ice': ['fire', 'fighting', 'rock', 'steel'],
    'dragon': ['ice', 'dragon', 'fairy'],
    'dark': ['fighting', 'bug', 'fairy'],
    'fairy': ['poison', 'steel'],
    'normal': ['fighting'],
    'fighting': ['flying', 'psychic', 'fairy'],
    'flying': ['electric', 'ice', 'rock'],
    'poison': ['ground', 'psychic'],
    'ground': ['water', 'grass', 'ice'],
    'rock': ['water', 'grass', 'fighting', 'ground', 'steel'],
    'bug': ['fire', 'flying', 'rock'],
    'ghost': ['ghost', 'dark'],
    'steel': ['fire', 'fighting', 'ground']
}
resistances = {
    'fire': ['fire', 'grass', 'ice', 'bug', 'steel', 'fairy'],
    'water': ['fire', 'water', 'ice', 'steel'],
    'grass': ['water', 'electric', 'grass', 'ground'],
    'electric': ['electric', 'flying', 'steel'],
    'psychic': ['fighting', 'psychic'],
    'ice': ['ice'],
    'dragon': ['fire', 'water', 'electric', 'grass'],
    'dark': ['ghost', 'dark'],
    'fairy': ['fighting', 'bug', 'dark'],
    'normal': [],
    'fighting': ['bug', 'rock', 'dark'],
    'flying': ['grass', 'fighting', 'bug'],
    'poison': ['grass', 'fighting', 'poison', 'bug', 'fairy'],
    'ground': ['poison', 'rock'],
    'rock': ['normal', 'fire', 'poison', 'flying'],
    'bug': ['grass', 'fighting', 'ground'],
    'ghost': ['poison', 'bug'],
    'steel': ['normal', 'grass', 'ice', 'flying', 'psychic', 'bug', 'rock', 'dragon', 'steel', 'fairy']
}
immunities = {
    'fire': [],
    'water': [],
    'grass': [],
    'electric': ['electric'],
    'psychic': [],
    'ice': [],
    'dragon': [],
    'dark': ['psychic'],
    'fairy': [],
    'normal': ['ghost'],
    'fighting': [],
    'flying': ['ground'],
    'poison': [],
    'ground': ['electric'],
    'rock': [],
    'bug': [],
    'ghost': ['normal', 'fighting'],
    'steel': ['poison']
}
def get_most_common_weakness(types):
    weakness_count = {}
    for pokemon_type in types:
        if pokemon_type in weaknesses:
            for weakness in weaknesses[pokemon_type]:
                if weakness in weakness_count:
                    weakness_count[weakness] += 1
                else:
                    weakness_count[weakness] = 1
            for resistance in resistances[pokemon_type]:
                if resistance in weakness_count:
                    weakness_count[resistance] -= 0.5
            for immunity in immunities[pokemon_type]:
                if immunity in weakness_count:
                    weakness_count[immunity] -= 1.5
    if weakness_count:
        most_common_weakness = max(weakness_count, key=weakness_count.get)
        return most_common_weakness
    else:
        return "No weaknesses found"    
def generate_teams(n):
    teams = []
    for _ in range(n):
        team = [types[randrange(0, len(types))] for _ in range(3)]
        teams.append(team)
    return teams
# Print cli args
teams_num = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 2
teams = generate_teams(teams_num)
vulnerabilities = [get_most_common_weakness(team) for team in teams]
def get_label(index): return f'pokemon{index}_type'
pokemon_types = {get_label(i+1): [team[i] for team in teams] for i in range(3)}
data = {
    **pokemon_types,
    'vulnerability': vulnerabilities
} 
# Criar DataFrame
df = pd.DataFrame(data)
# Converter tipos em números (encoder)
type_mapping = {'fire': 0, 'water': 1, 'grass': 2, 'electric': 3, 'psychic': 4, 'ice': 5, 'dragon': 6, 'dark': 7, 'fairy': 8, 'normal': 9, 'fighting': 10, 'flying': 11, 'poison': 12, 'ground': 13, 'rock': 14, 'bug': 15, 'ghost': 16, 'steel': 17}
df = df.map(lambda x: type_mapping[x] if x in type_mapping else x)
i = df.to_csv()
open('data.csv', 'w').write(i)
# Separar características e alvo
X = df.drop('vulnerability', axis=1)
y = df['vulnerability']

# Dividir os dados em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Criar e treinar o modelo
# model = DecisionTreeClassifier()
scaler = StandardScaler()
# scaler = MinMaxScaler()

# Ajustar e transformar os dados de treino
X_train_scaled = scaler.fit_transform(X_train)
# Transformar os dados de teste
X_test_scaled = scaler.transform(X_test)

model = RandomForestClassifier(random_state=42)
model.fit(X_train_scaled, y_train)

# Fazer previsões
y_pred = model.predict(X_test_scaled)

# Avaliar o modelo
accuracy = accuracy_score(y_test, y_pred)
print(f'Acurácia do modelo: {accuracy*100:.2f}%')
