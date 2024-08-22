## ANALIZA PODATKOV - KNJIGE

Avtor: Zala Gregorc

Vsi kdaj pa kdaj radi preberemo kakšno dobro knjigo, še posebej ob morju na plaži. Da bi vedeli, katere knjige se trenutno najbolje prodajajo, kakšna je razlika v ceni med elektronsko knjigo in mehko vezavo, kateri avtorji ponujajo največ knjig in kateri naslovi so najbolj priljubljeni med bralci, sem pripravila analizo le-teh.

V tem projektu bom analizirala knjige, ki jih ponuja ena izmed bolj priljubljenih spletnih knjigaren, [Belentrina] (https://beletrina.si). 

# UPORABA PROGRAMA

Prvi korak je pridobivanje podatkov oziroma neobdelanih (HTML) zapisov, v katerih se skrivajo željeni podatki. Kodo za ta korak najdete v datoteki prevedi_in_shrani.py. Ta koda naloži prvih osem strani s knjigami pod rubrikama "Romani" in "Poezije". Iz dobljenih podatkov nato funkcija razbere dopolnitvene URL-je, ki nas povežejo s spletnimi stranmi posameznih knjig, ki so na voljo na teh osmih straneh.

Drugi korak je iz tega nepreglednega HTML zapisa izluščiti podatke, ki jih bomo potrebovali za analizo. To naredimo s pomočjo skripte obdelaj_podatke.py, kjer najdete kodo, ki naše podatke prečisti s pomočjo regularnih izrazov ter jih shrani v CSV datoteko oziroma tabelo. Tudi tukaj je potrebno le zagnati skripto.

Zadnji korak je analiza dobljenih podatkov, rezultate le-teh najdete v Jupyter zvezku projekt.ipynb.

# AKTIVACIJA VIRTUALNEGA OKOLJA 

Aktivacija virtualnega okolja:

"""
source venv/bin/activate
"""

# KLJUČNE KNJIŽNICE UPORABLJENE V PYTHON SKRIPTI

Program je v celoti napisan v jeziku python, pri čemer smo uporabili naslednje knjižnice:
 - knjižnico request; za pošiljanje HTTP zahtevkov in prejemanje odgovorov s spletnih strežnikov 
 - knjižnico os, ki omogoča interakcijo z operacijskim sistemom, torej preveri obstoj datotek ali map in jih po potrebi ustvari ali spremeni (v ta namen sem jo jaz uporabila) 
 - knjižnico re; za delo z regularnimi izrazi
 - knjižnica csv; za branje in pisanje datotek v formatu csv (shranjevanje podatkov v obliki tabele)

Kako naložiti potrebe knjižnice (za okolje iOS):

"""
pip3 install requests
pip3 install pandas
pip3 install matplotlib
"""