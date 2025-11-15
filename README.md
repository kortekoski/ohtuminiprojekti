## Ohtun miniprojekti, syksy 2025 (team Neliapila)

### Ohjelman käynnistäminen

Sovellus käynnistetään Poetry-virtuaaliympäristössä komennolla
````
python src/index.py
````
Tietokanta käynnistetään projektin juuressa (erillisessä terminaalissa) komennolla 
````
docker compose up
````
Huomaa että ennen kuin käynnistät sovelluksen ensimmäisen kerran, tulee suorittaa komento, joka luo sovelluksen käyttämän tietokantataulun:
````
python src/db_helper.py
````
Yksikkötestit suoritetaan komennolla:
````
pytest src/tests
````
Robot-testit suoritetaan komennolla:
````
robot src/story_tests
````
Coverage-kattavuus suoritetaan komennolla: 
```` 
coverage run --branch -m pytest; coverage html
```` 


### Linkit backlogeihin
Backlogit: https://docs.google.com/spreadsheets/d/1YLn6Z2UjyHvtpES_IHdXTMnKivLhKFq_CAAXcKCP_Vc/edit?usp=sharing

### Definition of done
- Toteutetun koodin testikattavuus on kohtuullinen (~80 %).
- Asiakas voi aina nähdä koodin ja testien tilanteen CI-palvelusta. Testit menevät läpi CI:ssä.
- Hyväksymiskriteerit täyttyvät. Asiakas hyväksyy toteutetun koodin.
- Koodin tulee olla mahdollisimman ylläpidettävää, eli
  - nimeäminen on tehty järkevästi ja yhdenmukaisesti Pythonin tyylikäytänteiden mukaisesti
  - arkkitehtuuri on selkeää ja perusteltua
  - koodin tyyli on yhtenäistä, ja sitä valvotaan Pylintin avulla.
- Dokumentaatiota on päivitetty tarpeen mukaan.

## Asennusohjeet

### Tietokanta 
[README_db](documentation/README_db.md) 
