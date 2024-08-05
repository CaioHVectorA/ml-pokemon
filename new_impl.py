import matplotlib.pyplot as plt 
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.multioutput import MultiOutputClassifier
# Read the dataset
df = pd.read_csv('./data/pokemon.csv')

# Print the first few rows of the dataset

features = df.columns[2:19]
target = ['type1', 'type2']
print(df.columns[36:38])
X = df[features]
y = df[target]
type_mapping = {'fire': 0, 'water': 1, 'grass': 2, 'electric': 3, 'psychic': 4, 'ice': 5, 'dragon': 6, 'dark': 7, 'fairy': 8, 'normal': 9, 'fighting': 10, 'flying': 11, 'poison': 12, 'ground': 13, 'rock': 14, 'bug': 15, 'ghost': 16, 'steel': 17}
X = X.replace(type_mapping)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# model = RandomForestClassifier(random_state=42)
# model.fit(X_train, y_train)
arvore = MultiOutputClassifier(estimator=RandomForestClassifier)
arvore.fit(X, y)

plt.figure(dpi=300)

# tree.plot_tree(arvore,
#                class_names=arvore.classes_,
#                feature_names=features,
#                max_depth=3,
#                filled=True)

# plt.show()

predict = arvore.predict(X)

print(predict)

