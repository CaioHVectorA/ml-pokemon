import tkinter as tk
import csv

def load_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data
type_mapping = {'fire': 0, 'water': 1, 'grass': 2, 'electric': 3, 'psychic': 4, 'ice': 5, 'dragon': 6, 'dark': 7, 'fairy': 8, 'normal': 9, 'fighting': 10, 'flying': 11, 'poison': 12, 'ground': 13, 'rock': 14, 'bug': 15, 'ghost': 16, 'steel': 17}
reverted_type_mapping = {v: k for k, v in type_mapping.items()}
print(reverted_type_mapping)
def create_csv_viewer(csv_data):
    root = tk.Tk()
    root.title("CSV Viewer")

    # Create a table to display the CSV data
    for i, row in enumerate(csv_data):
        print(i, row)
        for j, value in enumerate(row):
            if (value.isdigit()): value = reverted_type_mapping[int(value)]
            label = tk.Label(root, text=value, relief=tk.RIDGE)
            label.grid(row=j, column=i, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    file_path = "./data.csv"
    csv_data = load_csv(file_path)
    create_csv_viewer(csv_data)