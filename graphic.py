from multiprocessing import Pool
import subprocess
import matplotlib.pyplot as plt
from tqdm import tqdm
NUMBER_OF_IRATIONS = 300
# def run_script(_):
#     result_10 = subprocess.run(['python', 'main.py', '10'], capture_output=True, text=True)
#     result_100 = subprocess.run(['python', 'main.py', '100'], capture_output=True, text=True)
#     result_1000 = subprocess.run(['python', 'main.py', '1000'], capture_output=True, text=True)
#     printed_value_10 = result_10.stdout.strip()
#     printed_value_100 = result_100.stdout.strip()
#     printed_value_1000 = result_1000.stdout.strip()
#     return float(printed_value.replace('Acurácia do modelo: ', '').replace('%', '').strip())
def run_script(_):
    result = subprocess.run(['python', 'main.py', '500'], capture_output=True, text=True)
    printed_value = result.stdout.strip()
    return float(printed_value.replace('Acurácia do modelo: ', '').replace('%', '').strip())
def run_script_hundred(_):
    result = subprocess.run(['python', 'main.py', '100'], capture_output=True, text=True)
    printed_value = result.stdout.strip()
    return float(printed_value.replace('Acurácia do modelo: ', '').replace('%', '').strip())
def run_script_thousand(_):
    result = subprocess.run(['python', 'main.py', '1000'], capture_output=True, text=True)
    printed_value = result.stdout.strip()
    return float(printed_value.replace('Acurácia do modelo: ', '').replace('%', '').strip())
def run_script_hundred_thousand(_):
    result = subprocess.run(['python', 'main.py', '100000'], capture_output=True, text=True)
    printed_value = result.stdout.strip()
    return float(printed_value.replace('Acurácia do modelo: ', '').replace('%', '').strip())
if __name__ == "__main__":
    with Pool() as pool:
        results = list(tqdm(pool.imap(run_script, range(int(NUMBER_OF_IRATIONS/3))), total=int(NUMBER_OF_IRATIONS/3), desc="Loading graphic 500"))
        # results_hundred = list(tqdm(pool.imap(run_script_hundred, range(int(NUMBER_OF_IRATIONS/3))), total=int(NUMBER_OF_IRATIONS/3), desc="Loading graphic 100"))
        results_thousand = list(tqdm(pool.imap(run_script_thousand, range(int(NUMBER_OF_IRATIONS/3))), total=int(NUMBER_OF_IRATIONS/3), desc="Loading graphic 1000"))
        results_ten_thousand = list(tqdm(pool.imap(run_script_hundred_thousand, range(int(NUMBER_OF_IRATIONS/3))), total=int(NUMBER_OF_IRATIONS/3), desc="Loading graphic 100000"))
    # Plot the results
    plt.figure(figsize=(10, 5))
    plt.title('Model Accuracy')
    plt.xlabel('Iteration')
    plt.ylabel('Accuracy (%)')
    plt.plot(results, color='blue', label='500')
    # plt.plot(results_hundred, color='red', label='100')
    plt.plot(results_thousand, color='green', label='1000')
    plt.plot(results_ten_thousand, color='yellow', label='100000')
    plt.legend()
    plt.show()