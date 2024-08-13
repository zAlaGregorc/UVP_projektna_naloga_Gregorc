import requests # ENOSTAVNEJŠA OD URLLIB; pošlje zahteve (z requests) na spletni strežnik, ki vsebuje spletno stran na url
import re # za uporabo regularnih izrazov
import os 

# Najprej definirajmo nekaj spremenljivk, ki jih bomo potrebovali v nadaljevanju.
# url glavne spletne strani - v mojem primeru nepremičnine.net
url = "https://www.nepremicnine.net"
# Imeni map, kamor bomo shranili naše podatke; zapišemo v obliki seznama nepremicnine.
nepremicnine = ["stanovanje", "hiša"]
# Imena datotek, kamor shranimo naše podatke; enako kot imena map zapišemo kot seznam lokacije.
lokacije = ["Ljubljana_mesto", "Ljubljana_okolica", "posavje", "koroška"]

def prevedi_v_niz(link):
    """
    Funkcija sprejme niz in poskusi vrniti vsebino te spletne strani kot niz, če je to mogoče.
    Sicer nam o napaki poroča.
    """
    # Try sproži oziroma pokaže napako, če je ta prisotna.
    try:
        # vsebino spletne strani (HTML) shranimo v spremenljivko besedilo
        vsebina = requests.get(link).text
    # Če pride do napake pri pošiljanju zahtevka ali pridobivanju vsebine (npr. spletna stran ne obstaja), 
    # nam to sporoči - "Prišlo je do napake!". 
    except requests.exceptions.RequestException:
        print("Prišlo je do napake!")
        return None
    # Če ni prišlo do napake funkcija vrne vsebino spletne strani.
    return vsebina

def shrani_v_datoteko(besedilo, mapa, datoteka):
    """ 
    Funkcija shrani vsebino (besedilo) v željeno datoteko "datoteka", ki se nahaja v mapi "mapa" 
    (v resnici poda pot do datoteke). Funkcija vrne False, če pride do napake.
    """
    try:
        # Ustvarimo mapo, če ta še ne obstaja. Drugi argument prepreči, da bi prišlo do napake v primeru ko mapa že obstaja.
        os.makedirs(mapa, exist_ok=True)
        # path nam pove, kje lahko našo datoteko najdemo ("polno pot do datoteke")
        path = os.path.join(mapa, datoteka)
        # odpremo datoteko za pisanje, kamor zapišemo vsebino / besedilo
        with open(path, 'w', encoding='utf-8') as izhodna:
            izhodna.write(besedilo)
        return None
    # Če funkcija naleti na problem oziroma napako, to pove.
    except OSError:
        print(f"Napaka pri shranjevanju")
        return False

