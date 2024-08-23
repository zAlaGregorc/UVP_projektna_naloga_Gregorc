import re
import os
import csv # za branje in pisanje CSV datotek

class Knjige():
    """ 
    Razred Knjige predstavlja eno knjigo, ki se prodaja. Z atributi naslov knjige, avtor knjige, 
    število strani (dolžina) in opis pisatelja.
    """

    def __init__(self, naslov, avtor, dolzina, o_pisatelju):
        # Nastavimo začetne vrednosti za podatke.
        self.naslov = naslov
        self.avtor = avtor
        self.dolzina = dolzina
        self.o_pisatelju = o_pisatelju
        self.zvrst = None

    def __str__(self):
        """
        Vrnemo niz, ki opisuje eno knjigo.
        """
        return f"Knjiga z naslovom {self.naslov},\n avtor: {self.avtor},\n dolžina: {self.dolzina} strani in\n o_pisatelju: {self.o_pisatelju}."
    
    def __repr__(self):
        """
        Funkcija vrne opis knjige (objekta), ki je primeren za razhroščevanje, shranjevanje 
        in ponovno ustvarjanje objekta.
        """
        return f"Nepremicnine(lokacija='{self.naslov}', tip='{self.avtor}', kvadratura={self.dolzina}, o_pisatelju={self.o_pisatelju})"

    def pretvori_v_slovar(self):
        """
        Vrne slovar, ki vsebuje podatke knjige. Kasneje ga bomo zapisali v csv.
        """
        return {"naslov": self.naslov, "avtor": self.avtor, "dolzina": self.dolzina, "zvrst": self.zvrst, "o_pisatelju": self.o_pisatelju}

print("Razred je narejen.")  


    
def izlusci_podatke(html):
    """
    Funkcija izlušči vse podatke, ki jih potrebujemo, iz html zapisa.
    """
    # 1. NASLOV
    # Za vsak podatek posebej najprej napišemo vzorec z regularnimi izrazi, po katerem najdemo podatek v html-ju.
    naslov_vzorec = r"<div class=\"title-02\">\s*(.*?)\s+<\/div>"
    # Te vzorce poiščemo v html-ju.
    naslov = re.search(naslov_vzorec, html, flags=re.DOTALL)
    naslov = naslov.group(1) if naslov else None

    
    # 2. AVTOR
    avtor_vzorec = r"class=\"link-underline\">(.+?)<\/a>"
    avtor = re.search(avtor_vzorec, html, flags=re.DOTALL)
    avtor = avtor.group(1) if avtor else None
    
    
    # 3. ŠTEVILO STRANI
    dolzina_vzorec = r"<dt>Št\. strani<\/dt>\s*<dd>(\d+)<\/dd>"
    dolzina = re.search(dolzina_vzorec, html, flags=re.DOTALL)
    dolzina = dolzina.group(1) if dolzina else None
    
    # 4. VSEBINA KNJIGE
    o_pisatelju_vzorec = r'<div class="w-full md:w-1\/2 xl:w-8\/12">\s*<p>(.*?)<\/p>\s*?'
    o_pisatelju = re.search(o_pisatelju_vzorec, html, flags=re.DOTALL)
    o_pisatelju = o_pisatelju.group(1).replace('"', '').replace('&ndash', '-').strip() if o_pisatelju else None
    
    return Knjige(naslov, avtor, dolzina, o_pisatelju)



def pridobi_podatke_iz_datoteke(datoteka):
    """
    Funkcija prebere in izpiše podatke iz ene same html datoteke.
    """
    with open(datoteka, "r", encoding='utf-8') as f:
        vsebina = f.read()
        podatki = izlusci_podatke(vsebina)
        return [podatki] if podatki else []
    


def vsi_podatki_o_knjigah(mapa):
    """
    Funkcija pridobi vse podatke iz vseh html datotek v mapi.
    """
    knjige = []
    for datoteka in os.listdir(mapa):
        if datoteka.endswith(".html"):
            pot_do_datoteke = os.path.join(mapa, datoteka)
            try:
                knjige.extend(pridobi_podatke_iz_datoteke(pot_do_datoteke))
            except FileNotFoundError:
                print(f"Datoteka {pot_do_datoteke} ni najdena.")
            except Exception as e:
                print(f"Napaka pri obdelavi datoteke {pot_do_datoteke}: {e}")
    return knjige

            

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
    


def pripravi_podatke_za_csv():
    vsi_podatki = []
    zvrsti = ["roman", "poezija"]
    for zvrst in zvrsti:
        knjige = vsi_podatki_o_knjigah(f"podatki/{zvrst}/knjige")
        for knjiga in knjige:
            knjiga.zvrst = zvrst
            podatki_knjige = knjiga.pretvori_v_slovar() 
            vsi_podatki.append(podatki_knjige)
    return vsi_podatki
    
    
vsi_podatki = pripravi_podatke_za_csv()            
fieldnames = ["naslov", "avtor", "dolzina", "zvrst", "o_pisatelju"]
write_csv(fieldnames, vsi_podatki, "koncni_podatki", "podatki_o_knjigi.csv")
