# Thonny logifailide analüüs

## Töörežiimid ##

### graafikud ###
Selle abil on võimalik näha üldist analüüsi kontrolltöö logifaili kohta kasutajaliideses.
Kasutajale kuvatakse järgnev informatsioon.
* Üldinfo - Kuvatakse töö lahendamise algus- ja lõppaeg ning kestus. Samuti veateadete arv, käivitamiste kordade arv, veateadetega järgnenud käivitamiste kordade arv ning rohkem kui **n** tähemärki pikkade tekstilõikude kleepimiste arv, kus **n** on kasutaja poolt valitud minimaalse kleebitud teksti pikkus. Vaikeväärtus minimaalse kleebitud pikkuse jaoks on 0.
* Erroritüübid - Sektrodiagramm, kus tuuakse välja erinevad veateated, mis kasutajal esinesid, ning nende esinemiste kordade arv.
* Käivitamised - Sündmusegraafik, kus on näha ajajoonel käivitamised, millele järgnes veateade ehk programmi töös oli midagi valesti, ja käivitamised, millele ei järgnenud veateadet ehk programmitöö oli edukas.
* Kleebitud tekstid - Tabel, kus kuvatakse vähemalt **n** pikkusega kleebitud tekstid koos ajatemplitega.
* Veateated - Tabel, kus kuvatakse kasutajal esinenud veateated koos ajatemplitega ning tüübiga.

### CSV-failid ###
Selle abil on võimalik saada üldine analüüsi informatsioon ühe logifaili kohta.
Kasutajale salvestatkse järgnevad CSV-failid samasse kausta, kus asus vaadeldav logifail.
* *logifailinimi*\_pasting.csv - CSV-fail, kus on informatsioon teksti kleepimiste kohta.
* *logifailinimi*\_errors.csv - CSV-fail, kus on informatsioon veateadete kohta.
* *logifailinimi*\_runnings.csv - CSV-fail, kus on informatsioon programmi käivitamiste kohta.
