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
        return f"Nepremicnine(lokacija='{self.lokacija}', tip='{self.tip}', kvadratura={self.kvadratura} m², cena={self.cena:.2f} €)"

    def pretvori_v_slovar(self):
        '''
        Vrne slovar, ki vsebuje podatke nepremičnine. Kasneje ga bomo zapisali v csv.
        '''
        return {"lokacija": self.lokacija, "tip nepremičnine": self.tip, "kvadratura": self.kvadratura, "cena": self.cena}
    
    
    
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



def vsi_oglasi_nepremicnin(path):
    '''
    Funkcija pobere vse podatke iz naših html datotek.
    '''
    # seznam, ki hrani vse nepremicnine
    nepremicnine = []
    for i in range(1, 16):
        if i == 1:
            while os.path.exists(path + ".html"):
                with open(path + ".html", "r", encoding='utf-8') as file_in:
                    vsebina = file_in.read()
                    najdene_nepremicnine = izlusci_oglase(vsebina)  
        else:       
            # postopek ponavljamo dokler imamo datoteke
            while os.path.exists(path + '/' + str(i) + '.html'):
                with open(path + '/' + str(i) + '.html', "r", encoding='utf-8') as file_in:
                    vsebina = file_in.read()
                    najdene_nepremicnine = izlusci_oglase(vsebina)
        nepremicnine.extend(najdene_nepremicnine)
    return nepremicnine




