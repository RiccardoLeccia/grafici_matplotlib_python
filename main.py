import os
import pandas as pd
import shutil
import tkinter as tk
import matplotlib.pyplot as plt

def lettura_file(percorso_file):
    data = []
    with open(percorso_file, "r") as f:
        righe = f.readlines()[4:]
        for riga in righe:
            valori = []
            for elemento in riga.split():
                try:
                    if "." in elemento or "e" in elemento.lower():
                        numero = float(elemento)
                        valori.append(numero)
                    else:
                        valori.append(int(elemento))
                except ValueError:
                    valori.append(elemento)
            data.append(valori)

    num_colonne = max(len(riga) for riga in data) if data else 0
    colonne = [[] for _ in range(num_colonne)]
    for riga in data:
        for i, valore in enumerate(riga):
            colonne[i].append(valore)
    
    return colonne

def config():
    with open("config.txt", "r") as f:
        TITOLO = f.readline().strip()
        WIDTH = int(f.readline().strip())
        HEIGHT = int(f.readline().strip())
        COLORE = f.readline().strip()
    return TITOLO, WIDTH, HEIGHT, COLORE

def crea_grafici_max(max_values, quote):
    max_v = []
    quotes_list = []
    cartella_grafici = "grafici/valori_massimi_quote"
    for file in file_list:
        if file in max_values and file in quote and quote[file]:  
            max_v.append(list(max_values[file])[1:]) 
            quotes_list.append(quote[file])
    print(f"Valori massimi: {max_v}")
    print(f"Quote: {quotes_list}")

    if os.path.exists(cartella_grafici):
        shutil.rmtree(cartella_grafici)
    os.makedirs(cartella_grafici, exist_ok=True)

    for i, file in enumerate(file_list):
        if i >= len(max_v) or i >= len(quotes_list):
            print(f"Skip file {file}: dati insufficienti")
            continue  

        if len(max_v[i]) == len(quotes_list[i]):  
            plt.figure(figsize=(10, 6))
            plt.plot(max_v[i], quotes_list[i], color=conf[3], linewidth=0.5)
            plt.xlabel("Valori massimi")
            plt.ylabel("Quote")
            plt.title(f"Valori massimi e Quote - {file}")
            plt.grid(True)
            plt.savefig(f"{cartella_grafici}/grafico_valori_massimi_x_quote_{file}.png", dpi=300)
            plt.close()
        else:
            print(f"Errore: Lunghezze diverse per {file} - Max: {len(max_v[i])}, Quote: {len(quotes_list[i])}")



def continua(entry_list):
    global counter, quote
    quote[current_file] = [entry.get() for entry in entry_list if entry.get().strip()]  
    counter += 1
    richiesta_quote()

def clear_window():
    for widget in finestra.winfo_children():
        widget.destroy()

def disegna_grafici_per_file(cartella_data, cartella_grafici, conf):
    if os.path.exists(cartella_grafici):
        shutil.rmtree(cartella_grafici)
    os.makedirs(cartella_grafici, exist_ok=True)
    
    for file in os.listdir(cartella_data):
        percorso = os.path.join(cartella_data, file)
        if os.path.isfile(percorso):
            colonne = lettura_file(percorso)

            nome_file = os.path.splitext(file)[0]
            cartella_file = os.path.join(cartella_grafici, nome_file)
            os.makedirs(cartella_file, exist_ok=True)

            for i in range(1, len(colonne)):
                y = colonne[i]
                plt.figure(figsize=(10, 6))
                lunghezza_min = min(len(colonne[0]), len(y))
                plt.plot(colonne[0][:lunghezza_min], y[:lunghezza_min], label=f"Colonna {i}", color=conf[3], linewidth=0.5)
                
                plt.xlabel("Valori X")
                plt.ylabel("Valori Y")
                plt.title(f"Grafico per {nome_file} - Colonna {i}")
                plt.legend()
                plt.grid(True)
                plt.savefig(f"{cartella_file}/grafico_colonna_{i}.png", dpi=300)
                plt.close()

def richiesta_quote():
    global counter, current_file, quote, file_list
    
    if counter >= len(file_list):
        if all(quote.values()):  
            finestra.destroy()
            crea_grafici_max(max_values, quote)
        else:
            print("Errore: Non tutte le quote sono state inserite")
        return
    
    current_file = file_list[counter]
    colonne_count = len(data[current_file])
    quote[current_file] = []
    
    clear_window()
    
    label = tk.Label(finestra, text=f"Inserire le quote per il file: {current_file}")
    label.pack()
    
    entry_list = []
    for i in range(colonne_count - 1):
        entry = tk.Entry(finestra, width=20)
        entry.pack()
        entry_list.append(entry)
    
    button = tk.Button(finestra, text="Invia", command=lambda: continua(entry_list))
    button.pack()

avanza, counter = False, 0
conf = config()
quote = {}
max_values = {}
data = {}
file_list = []

for file in os.listdir("data/"):
    percorso = os.path.join("data/", file)
    if os.path.isfile(percorso):
        colonne = lettura_file(percorso)
        if colonne:
            max_len = max(len(col) for col in colonne)
            colonne = [col + [None] * (max_len - len(col)) for col in colonne]

            df = pd.DataFrame({f"Colonna {i}": col for i, col in enumerate(colonne)})
            max_values[file] = df.max()
            data[file] = colonne
            file_list.append(file)

disegna_grafici_per_file("data/", "grafici/", conf)

finestra = tk.Tk()
finestra.title(conf[0])
finestra.geometry(f"{conf[1]}x{conf[2]}")
finestra.resizable(False, False)

richiesta_quote()

finestra.mainloop()