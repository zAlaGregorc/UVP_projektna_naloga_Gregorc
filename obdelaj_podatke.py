import re
import os
import csv #


class Knjige():
    """ 
    Razred Knjige predstavlja eno knjigo, ki se prodaja. Vsaka knjiga ima za atribute 
    naslov knjige, avtorja knjige, število strani (dolžina), cena knjige (mehka vezava),
    cena elektronske knjige (ecena).
    """

    def __init__(self, naslov, avtor, dolzina, cena, ecena):
        # Nastavimo začetne vrednosti za podatke.
        self.lokacija = naslov
        self.tip = avtor
        self.kvadratura = dolzina
        self.cena = cena
        self.ecena = ecena
        self.zvrst = None

    def __str__(self):
        """
        Vrnemo niz, ki opisuje eno knjigo.
        """
        return f"Knjiga z naslovom {self.naslov},\n avtor: {self.avtor},\n dolžina: {self.dolzina} strani,\n cena mehke vezave: {self.cena} € in\n cena e-knjige: {self.ecena}."
    
    def __repr__(self):
        """
        Funkcija vrne opis knjige (objekta), ki je primeren za razhroščevanje, shranjevanje 
        in ponovno ustvarjanje objekta.
        """
        return f"Nepremicnine(lokacija='{self.naslov}', tip='{self.avtor}', kvadratura={self.dolzina}, cena mehke vezave={self.cena:.2f}, cena e-knjige={self.ecena:.2f})"

    def pretvori_v_slovar(self):
        """
        Vrne slovar, ki vsebuje podatke nepremičnine. Kasneje ga bomo zapisali v csv.
        """
        return {"naslov": self.naslov, "avtor": self.avtor, "dolzina": self.dolzina, "cena": self.cena, "ecena": self.ecena}
    
print("Razred je narejen.")   
    
def izlusci_podatke(html):
    """
    Funkcija izlušči vse podatke iz html zapisa, ki jih potrebujemo za analizo.
    """
    # 1. NASLOV
    # Za vsak podatek posebej najprej napišemo vzorec z regularnimi izrazi, po katerem najdemo podatek v html-ju.
    naslov_vzorec = r"<div class=\"title-02\">\s+(\w+)\s+<\/div>"
    # Te vzorce poiščemo v html-ju.
    naslov = re.search(naslov_vzorec, html, flags=re.DOTALL)
    
    
    # 2. AVTOR
    avtor_vzorec = r"class=\"link-underline\">(.+?)<\/a>"
    avtor = re.findall(avtor_vzorec, html, flags=re.DOTALL)
    
    
    # 3. ŠTEVILO STRANI
    dolzina_vzorec = r"<dt>Št\. strani<\/dt>\s*<dd>(\d+)<\/dd>"
    dolzina = re.search(dolzina_vzorec, html, flags=re.DOTALL) + "strani"
    
    
    # 4. CENA MEHKE VEZAVE IN E-KNJIGE
    cena_vzorec = r"<div class=\"title-06 \">(\d+,\d+ €)<\/div>"
    cene = re.findall(cena_vzorec, html, flags=re.DOTALL) + "€"
    # Zapišemo, kaj se zgodi, če cena ni podana.
    if cena != None:
        cena = cene[0]
        ecena = cene[1]
    else:
        # če knjiga nima cene, jo filtriramo
        return None
    
    return Knjige(naslov, avtor, dolzina, cena, ecena)

print("Podatki so izluščeni.")

#!!!!!!!!!!!!!


def pridobi_podatke_iz_datoteke(datoteka):
    """
    Funkcija prebere in izpiše podatke iz ene same html datoteke.
    """
    with open(datoteka, "r", encoding='utf-8') as f:
        vsebina = f.read()
        return izlusci_podatke(vsebina)

def vse_knjige(mapa):
    """
    Funkcija pridobi vse podatke iz vseh html datotek v mapi.
    """
    knjiga = []
    for datoteka in os.listdir(mapa):
        if datoteka.endswith(".html"):
            pot_do_datoteke = os.path.join(mapa, datoteka)
            try:
                knjige.extend(pridobi_podatke_iz_datoteke(pot_do_datoteke))
            except FileNotFoundError:
                print(f"Datoteka {pot_do_datoteke} ni najdena.")
            except Exception as e:
                print(f"Napaka pri obdelavi datoteke {pot_do_datoteke}: {e}")
    return Knjige
            

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

# def pripravi_podatke_za_csv():
#     '''
#     Funkcija
#     '''
#     vrsta_nepremicnin = ["stanovanje", "hisa"]
#     obmocja = ["ljubljana-mesto", "ljubljana-okolica", "posavje", "koroska"]
#     vsi_podatki = []
#     for knjiga in knjige:
#         knjiga.vrsta_nepremicnine = vrsta_nepremicnine
#         knjiga.obmocje = obmocje         
#         vsi_podatki.extend(oglasi)
#         return vsi_podatki
    
vsi_podatki = pripravi_podatke_za_csv()
    
                
fieldnames = ["NASLOV", "AVTOR", "ŠTEVILO STRANI", "CENA MEHKE VEZAVE", "CENA E-KNJIGE"]
write_csv(fieldnames, vsi_podatki, "koncni_podatki", "knjige.csv")
