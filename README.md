# Thonny logifailide analüüs

## Töörežiimid ##

Kasutajal on võimalik valida ka mõlemad töörežiimid korraga.

### Analüüs graafilises liideses ###
Selle abil on võimalik näha üldist analüüsi kontrolltöö logifaili kohta kasutajaliideses.
Kasutajale kuvatakse järgnev informatsioon.
* Üldinfo - Kuvatakse töö lahendamise algus- ja lõppaeg ning kestus. Samuti veateadete arv, käivitamiste kordade arv, veateadetega järgnenud käivitamiste kordade arv ning rohkem kui **n** tähemärki pikkade tekstilõikude kleepimiste arv, kus **n** on kasutaja poolt valitud minimaalse kleebitud teksti pikkus. Vaikeväärtus minimaalse kleebitud pikkuse jaoks on 0.
* Erroritüübid - Sektrodiagramm, kus tuuakse välja erinevad veateated, mis kasutajal esinesid, ning nende esinemiste kordade arv.
* Käivitamised - Sündmusegraafik, kus on näha ajajoonel käivitamised, millele järgnes veateade ehk programmi töös oli midagi valesti, ja käivitamised, millele ei järgnenud veateadet ehk programmitöö oli edukas.
* Kleebitud tekstid - Tabel, kus kuvatakse vähemalt **n** pikkusega kleebitud tekstid koos ajatemplitega.
* Veateated - Tabel, kus kuvatakse kasutajal esinenud veateated koos ajatemplitega ning tüübiga.

### CSV-failid ###
Selle abil on võimalik saada üldine analüüsi informatsioon ühe logifaili kohta.
Kasutajale salvestatkse järgnevad CSV-failid samasse kausta, kus asus vaadeldav logifail. *Logifailinimi* on vaadeldava logifaili nimi.
* *logifailinimi*\_pasting.csv - CSV-fail, kus on informatsioon teksti kleepimiste kohta.
* *logifailinimi*\_errors.csv - CSV-fail, kus on informatsioon veateadete kohta.
* *logifailinimi*\_runnings.csv - CSV-fail, kus on informatsioon programmi käivitamiste kohta.

## Lisaparameetrid ##

### Minimaalne kleebitud teksti pikkus: ### 
Selle abil saab kasutaja täpsustada, kui pikk peab olema välja sorteeritud kleebitud tekstide minimaalne pikkus. Vaikeväärtus on 0.


## Töö käik ##

1. Valida vähemalt üks töörežiim või soovi korral ka mõlemad.
2. Soovi korral täpsustada lisaparameetrid.
3. Valida fail klõpastes nuppu "Vali logifail (.txt)". Tegemist saab olla ainult txt-failivorminguga ning peaks valima ainult korrektse logifaili.
4. Kui valiti fail, siis genereeritakse vastavalt esimeses punktis tehtud valikule graafilisse liidesesse analüüs, CSV-failid või mõlemad.
5. Kui on soov vaadelda uut logifaili, siis piisab ainult korrata punkti 3, kui ei ole soovi töörežiimi või lisaparameetreid muuta.

## Programmi käivitamine ##

Programm on loodud kasutades Pythoni versiooni 3.7. Käivitada tuleb eesliides.py. Pythoni versioonis ei ole automaatselt sees mooduleid matplotlib, numpy ja dateutil, seega need tuleb pip abil paigaldada.
