import requests # za pošiljanje zahtevkov in prejemanje odgovorov s spletnih strežnikov 
import os # za ustvarjanje ali popravljanje map/datotek
import re # za delo z regularnimi izraze


def prevedi_v_niz(url):
    """
    Funkcija sprejme niz in poskusi vrniti vsebino spletne strani kot niz, če je to mogoče,
    sicer nam o napaki poroča.
    """
    # Try sproži oziroma pokaže napako, če je ta prisotna.
    try:
        # vsebino spletne strani (HTML) shranimo v spremenljivko vsebina
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
    Funkcija shrani vsebino (besedilo) v novo datoteko "datoteka", ki se nahaja v mapi "mapa" 
    (v resnici poda pot do datoteke). Če datoteka že obstaja jo povozi. Funkcija vrne False, če pride do napake.
    """
    try:
        # Ustvarimo mapo, če ta še ne obstaja. Drugi argument prepreči, da bi prišlo do napake v primeru ko mapa že obstaja.
        os.makedirs(mapa, exist_ok=True)
        # Path nam pove, kje lahko našo datoteko najdemo ("polno pot do datoteke").
        path = os.path.join(mapa, datoteka)
        with open(path, 'w', encoding='utf-8') as izhodna:
            izhodna.write(besedilo)
            
        return None
    
    except OSError:
        print(f"Napaka pri shranjevanju")
        
        return False
    
    
    
def vse_glavne_strani(osnovni_url, zvrsti):
    '''
    Funkcija v zanki nalaga nadaljne strani v določeni zvrsti.
    '''
    # V zanki "povemo", koliko strani bomo naložili.
    for i in range(1, 9):
        text = prevedi_v_niz(osnovni_url + "/" + zvrsti + "/stran-" + str(i) + "/")
        # primer mape: podatki/roman, primer datoteke: 1.html
        if text:
            shrani_v_datoteko(text, "podatki/" + zvrsti, str(i) + ".html")



def shrani_spletne_strani():
    '''
    Funkcija shrani podatke iz spleta in jih shrani v ustrezno datoteko na disku.
    '''
    url = "https://beletrina.si"
    zvrsti = ["roman", "poezija"]
    for zvrst in zvrsti:
        vse_glavne_strani(url, zvrst)
        
shrani_spletne_strani()