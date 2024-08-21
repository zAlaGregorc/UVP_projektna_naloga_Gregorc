import requests # za pošiljanje zahtevkov in prejemanje odgovorov s spletnih strežnikov 
import os # za ustvarjanje ali popravljanje map/datotek
import re # za regularne izraze


def prevedi_v_niz(url):
    """
    Funkcija sprejme niz in poskusi vrniti vsebino te spletne strani kot niz, če je to mogoče,
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
    Funkcija shrani vsebino (besedilo) v željeno datoteko "datoteka", ki se nahaja v mapi "mapa" 
    (v resnici poda pot do datoteke). Funkcija vrne False, če pride do napake.
    """
    try:
        # Ustvarimo mapo, če ta še ne obstaja. Drugi argument prepreči, 
        # da bi prišlo do napake v primeru ko mapa že obstaja.
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
    
 

def izlusci_pot_do_knjig(html):
    """
    Funkcija poišče vse dopolnitve url-ja za dostop do spletnih strani knjig. Le-te shrani v seznam in ga vrne.
    """
    # napišemo vzorec po katerem najdemo del linka v html datoteki
    naslov_knjige_vzorec = r'<a href="(/knjiga/.+?)" class="'
    # poiščemo vse pojavitve
    naslov_knjige = re.findall(naslov_knjige_vzorec, html)
    return naslov_knjige



def pridobi_podatke_iz_datoteke(datoteka):
    """
    Funkcija prebere in izpiše podatke iz ene same html datoteke.
    """
    with open(datoteka, "r", encoding='utf-8') as f:
        vsebina = f.read()
        return izlusci_pot_do_knjig(vsebina)
    


def vsi_linki_knjig(mapa):
    """
    Funkcija pridobi vse podatke iz vseh html datotek v mapi.
    """
    link_knjige = []
    for datoteka in os.listdir(mapa):
        if datoteka.endswith(".html"):
            pot_do_datoteke = os.path.join(mapa, datoteka)
            try:
                link_knjige.extend(pridobi_podatke_iz_datoteke(pot_do_datoteke))
            except FileNotFoundError:
                print(f"Datoteka {pot_do_datoteke} ni najdena.")
            except Exception as e:
                print(f"Napaka pri obdelavi datoteke {pot_do_datoteke}: {e}")
    return link_knjige



def shrani_stran_knjige(url, mapa, ime_datoteke):
    """
    Funkcija shrani html zapise v datoteko "ime_datoteke", katero najdemo v mapi z imenom "mapa". 
    """
    besedilo = prevedi_v_niz(url)
    if besedilo:
        shrani_v_datoteko(besedilo, mapa, ime_datoteke)
    else:
        print(f"Strani ni bilo mogoče prenesti: {url}")



def main():
    url = "https://beletrina.si"
    linki = vsi_linki_knjig("podatki/roman")
    for link in linki:
        novi_url = url + link
        print(f"Pridobivam: {novi_url}")
        shrani_stran_knjige(novi_url, "podatki/roman/knjige", f"{link.split('/')[-1]}.html")


if __name__ == "__main__":
    main()
