## ANALIZA PODATKOV - KNJIGE

Avtor: Zala Gregorc   

Vsi kdaj pa kdaj radi preberemo kakšno dobro knjigo, še posebej ob morju na plaži. Da bi izvedeli, katere knjige so trenutno najbolj priljubljene, kateri avtorji ponujajo največ knjig, kaj zanimivega o njih ter kateri naslovi so najbolj priljubljena izbira med avtorji, sem pripravila analizo knjig.

V tem projektu bom analizirala knjige, ki jih ponuja ena izmed bolj priljubljenih spletnih knjigaren, [Beletrina](https://beletrina.si). 

# UPORABA PROGRAMA

Prvi korak je pridobivanje podatkov oziroma neobdelanih (HTML) zapisov, v katerih se skrivajo željeni podatki. Kodo za ta korak najdete v datotekah prevedi_in_shrani_glavne_strani.py in prevedi_in_shrani.py. Najprej zaženemo datotekah prevedi_in_shrani_glavne_strani.py, ki nam shrani glavne spletne strani, iz katerih naprej poiščemo dopolnitve URL-jev. Ta koda naloži prvih osem strani s knjigami pod rubrikama "Romani" in "Poezija". V drugi skripti pa iz dobljenih podatkov funkcija izlušči dopolnilne URL-je, ki nas povežejo s spletnimi stranmi posameznih knjig, ki so na voljo na teh osmih straneh posamezne rubrike.

Drugi korak je iz tega nepreglednega HTML zapisa izluščiti podatke, ki jih bomo potrebovali za analizo. To naredimo s pomočjo skripte obdelaj_podatke.py, kjer najdete kodo, ki prečisti naše podatke s pomočjo regularnih izrazov ter jih shrani v CSV datoteko oziroma tabelo. Tudi tukaj je potrebno le zagnati skripto.

Zadnji korak je analiza dobljenih podatkov. Rezultate te analize najdete v Jupyter zvezku projekt.ipynb.

# AKTIVACIJA VIRTUALNEGA OKOLJA 

Aktivacija virtualnega okolja:

"""
source venv/bin/activate
"""

# KLJUČNE KNJIŽNICE UPORABLJENE V PYTHON SKRIPTI

Program je v celoti napisan v jeziku python (tudi Jupyter zvezki), pri čemer sem uporabila naslednje knjižnice:

 - knjižnico request; za pošiljanje HTTP zahtevkov in prejemanje odgovorov s spletnih strežnikov 
 - knjižnico os, ki omogoča interakcijo z operacijskim sistemom, torej preveri obstoj datotek ali map in jih po potrebi ustvari ali spremeni (v ta namen sem jo jaz uporabila) 
 - knjižnico re; za delo z regularnimi izrazi
 - knjižnica csv; za branje in pisanje datotek v formatu csv (shranjevanje podatkov v obliki tabele)
 - knjižnica pandas; za branje in pisanje raznih podatkovnih struktur ter branje CSV datotek, uporablja se za analizo
 - knjižnica matplotlib; za izdelavo grafičnih prikazov podatkov

Kako naložiti potrebe knjižnice (za okolje iOS):

"""
pip3 install requests
pip3 install jupyter
pip3 install pandas
pip3 install matplotlib
"""
Za sisteme Windows uporabite ukaz 'pip install ime_knjižnice'.