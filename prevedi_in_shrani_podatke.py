import requests 
import os 
import re 


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
    
    
    
def izlusci_pot_do_knjig(html):
    """
    Funkcija poišče vse dopolnitve url-ja za dostop do spletnih strani knjig. Le-te shrani v seznam in ga vrne.
    """
    naslov_knjige_vzorec = r'<a href="(/knjiga/.+?)" class="'
    # Poiščemo vsa ujemanja v besedilu.
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
    Funkcija pridobi vse podatke iz vseh html datotek v mapi in vrne seznam, kamor jih shranjuje.
    """
    link_knjige = []
    for datoteka in os.listdir(mapa):
        
        if datoteka.endswith(".html"):
            # Če se datoteka konča s '.html', potem ustvari polno pot do datoteke.
            pot_do_datoteke = os.path.join(mapa, datoteka)
            
            try:
                # V seznam shrani izluščene podatke za datoteko.
                link_knjige.extend(pridobi_podatke_iz_datoteke(pot_do_datoteke))
                
            except FileNotFoundError:
                print(f"Datoteka {pot_do_datoteke} ni najdena.")
                
            except Exception as e:
                print(f"Napaka pri obdelavi datoteke {pot_do_datoteke}: {e}")
                
    return link_knjige



def shrani_stran_knjige(url, mapa, ime_datoteke):
    """
    Funkcija shrani html zapise v datoteko "ime_datoteke", katero najdemo v mapi z naslovom "mapa". 
    """
    besedilo = prevedi_v_niz(url)
    if besedilo:
        shrani_v_datoteko(besedilo, mapa, ime_datoteke)
    else:
        print(f"Strani ni bilo mogoče prenesti: {url}")



def main():
    url = "https://beletrina.si"
    zvrsti = ["roman", "poezija"]
    
    for zvrst in zvrsti:
        linki = vsi_linki_knjig(f"podatki/{zvrst}")
        for link in linki:
            novi_url = url + link
            print(f"Pridobivam: {novi_url}")
            shrani_stran_knjige(novi_url, f"podatki/{zvrst}/knjige", f"{link.split('/')[-1]}.html")


if __name__ == "__main__":
    main()
