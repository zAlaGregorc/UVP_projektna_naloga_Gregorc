import requests # ENOSTAVNEJŠA OD URLLIB
import re
import os

def prevedi_v_niz(url):
    try:
        besedilo = requests.get(url).text
    except requests.exceptions.RequestException:
        print("Prišlo je do napake!")
        return None
    return besedilo

def shrani_besedilo(besedilo, datoteka):
    
    return None

# KOPIRANI IZ ZAPISKOV!!
def vse_pojavitve(besedilo: str, iskani_niz: str):
    konec_pojavitve = 0
    while True:
        try:
            zacetek_pojavitve = besedilo.index(iskani_niz, konec_pojavitve)
            konec_pojavitve = min(zacetek_pojavitve + len(iskani_niz), len(besedilo))
            yield zacetek_pojavitve, konec_pojavitve
        except ValueError:
            break