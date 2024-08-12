import requests # ENOSTAVNEJŠA OD URLLIB
import re # za uporabo regularnih izrazov
import os 

def prevedi_v_niz(link):
    try:
        besedilo = requests.get(link).text
    except requests.exceptions.RequestException:
        print("Prišlo je do napake!")
        return None
    return besedilo

def shrani_v_datoteko(text, mapa, file):
    """ 
    Funkcija skrani podatke (text) 
    """
    # ustvarimo mapo, če ta še ne obstaja
    os.makedirs(mapa, exist_ok=True)
    # path nam pove, kje lahko našo datoteko najdemo ("pot do datoteke")
    path = os.path.join(mapa, file)
    # besedlo zapišemo v (novo) datoteko
    with open(path, 'w', encoding='utf-8') as izhodna:
        izhodna.write(text)
    return None



