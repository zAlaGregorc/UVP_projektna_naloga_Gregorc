import requests
 # ENOSTAVNEJŠA OD URLLIB; pošlje zahteve (z requests) na spletni strežnik, ki vsebuje spletno stran na url
import re # za uporabo regularnih izrazov
import os 

print("Skripta se je začela izvajati.")

def prevedi_v_niz(url):
    """
    Funkcija sprejme niz in poskusi vrniti vsebino te spletne strani kot niz, če je to mogoče.
    Sicer nam o napaki poroča.
    """
    # Try sproži oziroma pokaže napako, če je ta prisotna.
    try:
        # vsebino spletne strani (HTML) shranimo v spremenljivko besedilo
        vsebina = requests.get(url).text
    # Če pride do napake pri pošiljanju zahtevka ali pridobivanju vsebine (npr. spletna stran ne obstaja), 
    # nam to sporoči - "Prišlo je do napake!". 
    except requests.exceptions.RequestException:
        print("Prišlo je do napake!")
        return None
    # Če ni prišlo do napake funkcija vrne vsebino spletne strani.
    print("Vsebina je prevedena")
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

def shrani_stran_v_datoteko(url, nepremicnine, lokacije):
    """
    Ta funkcija nalaga strani za dolocene nepremicnine  iz katerih bomo dobili podatke 
    """
    for nepremicnina in nepremicnine:
        for lokacija in lokacije:
            # prenesli bomo le 15 strani podatkov, zato for zanko zapišemo v razponu od 1 do 15 
            for i in range(1, 16):
                if i == 1:
                    novi_url = url + "/oglasi-prodaja/" + lokacija + "/" + nepremicnina + "/"
                else:
                    novi_url = url + "/oglasi-prodaja/" + lokacija + "/" + nepremicnina + "/" + f"{i}" + "/"
                print(f"Pridobivam: {novi_url}")
                besedilo = prevedi_v_niz(novi_url)
                if besedilo:
                    shrani_v_datoteko(besedilo, f"podatki/{lokacija}/{nepremicnina}", f"{nepremicnina}_{i}.html")
                else:
                    print(f"Strani ni bilo mogoče prenesti: {novi_url}")

print("Skripta je končana.")

# Definirajmo nekaj spremenljivk, ki jih bomo potrebovali.
# url glavne spletne strani - v mojem primeru nepremičnine.net
url = "https://www.nepremicnine.net"
# Imeni map, kamor bomo shranili naše podatke; zapišemo v obliki seznama nepremicnine.
nepremicnine = ["stanovanje", "hisa"]
# Imena datotek, kamor shranimo naše podatke; enako kot imena map zapišemo kot seznam lokacije.
lokacije = ["ljubljana-mesto", "ljubljana-okolica", "posavje", "koroska"]
   
shrani_stran_v_datoteko(url, nepremicnine, lokacije)
 
# /Users/zalag/Desktop/UVP_projektna_naloga_Gregorc/prevedi_in_shrani_podatke.py