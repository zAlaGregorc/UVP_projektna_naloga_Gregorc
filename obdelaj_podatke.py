import re
import os
import csv



class Nepremicnine():
    """ 
    Razred Nepremicnine predstavlja eno nepremicnino, ki se prodaja. Vsaka nepremicnina ima napisano točno 
    lokacijo, tip nepremičnine, kvadraturo in ceno, za katero se prodaja.
    """

    def __init__(self, lokacija, tip, kvadratura, cena):
        # Nastavimo začetne vrednosti za podatke, ki nas zanimajo.
        self.lokacija = lokacija
        self.tip = tip
        self.kvadratura = kvadratura
        self.cena = cena
        self.vrsta_nepremicnine = None
        self.obmocje = None 

    def __str__(self):
        """
        Vrnemo niz, ki opisuje nepremičnino.
        """
        return f"Nepremičnina - lokacija: {self.lokacija},\n tip nepremičnine: {self.tip},\n kvadratura: {self.kvadratura} m² in\n cena: {self.cena} €"
    
    def __repr__(self):
        """
        Funkcija vrne opis nepremičnine (objekta), ki je primeren za razhroščevanje, shranjevanje 
        in ponovno ustvarjanje objekta.
        """
        return f"Nepremicnine(lokacija='{self.lokacija}', tip='{self.tip}', kvadratura={self.kvadratura}, cena={self.cena:.2f})"

    def pretvori_v_slovar(self):
        '''
        Vrne slovar, ki vsebuje podatke nepremičnine. Kasneje ga bomo zapisali v csv.
        '''
        return {"lokacija": self.lokacija, "tip nepremičnine": self.tip, "kvadratura": self.kvadratura, "cena": self.cena}
    
print("Razred je narejen.")   
    
def izlusci_podatke(html):
    """
    Funkcija izlušči vse podatke iz html zapisa, ki jih potrebujemo za analizo.
    """
    # 1. LOKACIJA
    # Za vsak podatek posebej najprej napišemo vzorec z regularnimi izrazi, po katerem najdemo podatek v html-ju.
    lokacija_vzorec = r"itemprop=\"name\" title=\"(\w+)"
    # Te vzorce poiščemo v html-ju.
    lokacija = re.search(lokacija_vzorec, html, flags=re.DOTALL)
    
    # 2. TIP NEPREMIČNINE
    tip_vzorec = r"Prodaja: (.+,).+\"tipi\">(.*?)<"
    tip = re.findall(tip_vzorec, html, flags=re.DOTALL)
    
    # 3. CENA
    cena_vzorec = r">([\d\.]+,\d+\s?[€$£])<"
    cena = re.search(cena_vzorec, html, flags=re.DOTALL)
    # Zapišemo, kaj se zgodi, če cena ni podana.
    if cena != None:
        cena = cena.group()
    else:
        # če oglas nima cene, ga filtriramo
        return None
    
    # 4. KVADRATURA
    kvadratura_vzorec = r"(\d+\,\d+) m"
    kvadratura = re.search(kvadratura_vzorec, html, flags=re.DOTALL) + "m²"
    
    return Nepremicnine(lokacija, tip, kvadratura, cena)

print("Podatki so izluščeni.")

def izlusci_oglase(vsebina):
    """ 
    Ta funckija iz html datoteke potegne bloke, ki predstavljajo posamezen oglas za nepremičnino. Vrne seznam oglasov 
    oziroma podatke iz oglasov, ki jih želimo.
    """
    # Napišemo najprej vzorec po katerem najdemo blok.
    blok_vzorec = r"<div class=\"col-md-6 col-md-12 position-relative\">"
    # Te bloke (vzorce) poiščemo v našem html-ju.
    nepremicnine_neobdelano = re.findall(blok_vzorec, vsebina, flags=re.DOTALL)
    # Vse oglase (bloke) shranimo v seznam.
    nepremicnine = []
    # Napišemo for zanko, ki za vsako nepremičnino izlušči podatke, ki jih doda v seznam, če že niso v seznamu.
    for nepremicnina in nepremicnine_neobdelano:
        prebran_oglas = izlusci_podatke(nepremicnina)
        if prebran_oglas != None:
            nepremicnine.append(prebran_oglas)
    return nepremicnine


def pridobi_podatke_iz_datoteke(datoteka):
    """
    Funkcija prebere in izpiše podatke iz ene same html datoteke.
    """
    with open(datoteka, "r", encoding='utf-8') as f:
        vsebina = f.read()
        najdene_nepremicnine = izlusci_oglase(vsebina)
        return najdene_nepremicnine

def vsi_oglasi_nepremicnin(mapa):
    """
    Funkcija pridobi vse podatke iz vseh html datotek v mapi.
    """
    nepremicnine = []
    for datoteka in os.listdir(mapa):
        if datoteka.endswith(".html"):
            pot_do_datoteke = os.path.join(mapa, datoteka)
            try:
                nepremicnine.extend(pridobi_podatke_iz_datoteke(pot_do_datoteke))
            except FileNotFoundError:
                print(f"Datoteka {pot_do_datoteke} ni najdena.")
            except Exception as e:
                print(f"Napaka pri obdelavi datoteke {pot_do_datoteke}: {e}")
    return nepremicnine
            

def write_csv(fieldnames, rows, directory, filename):
    """
    Funkcija v csv datoteko, ki se nahaja "directory"/"filename" zapiše
    vrednosti v parametru "rows" pripadajoče ključem podanim v "fieldnames"
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return

def pripravi_podatke_za_csv():
    '''
    Funkcija
    '''
    vrsta_nepremicnin = ["stanovanje", "hisa"]
    obmocja = ["ljubljana-mesto", "ljubljana-okolica", "posavje", "koroska"]
    vsi_podatki = []
    for obmocje in obmocja:
        for vrsta_nepremicnine in vrsta_nepremicnin:
            oglasi = vsi_oglasi_nepremicnin("podatki/" + obmocje + "/" + vrsta_nepremicnine)

            for oglas in oglasi:
                oglas.vrsta_nepremicnine = vrsta_nepremicnine
                oglas.obmocje = obmocje         
                vsi_podatki.extend(oglasi)
                return vsi_podatki
vsi_podatki = pripravi_podatke_za_csv()
    
                
fieldnames = ["LOKACIJA NEPREMIČNINE", "TIP NEPREMIČNINE", "KVADRATURA NEPREMIČNINE", "CENA NEPREMIČNINE"]
write_csv(fieldnames, vsi_podatki, "koncni_podatki", "nepremicnine.csv")
