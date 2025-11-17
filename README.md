# Ohtun miniprojekti, syksy 2025 (team Neliapila)

## Ohjelman käynnistäminen

Sovellus käynnistetään Poetry-virtuaaliympäristössä komennolla
````
python src/index.py
````
Tietokanta käynnistetään projektin juuressa (erillisessä terminaalissa) komennolla 
````
docker compose up
````
Huomaa, että ennen kuin käynnistät sovelluksen ensimmäisen kerran, tulee suorittaa komento, joka luo sovelluksen käyttämän tietokantataulun:
````
python src/db_helper.py
````
Huomaa, että jos tietokantaskeeman taulujen ja entiteettien rakenne muuttuu, tietokanta kannattaa tuhota ja luoda se uudestaan:
```` 
docker compose down -v
docker compose up
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


## Linkit backlogeihin
Backlogit: https://docs.google.com/spreadsheets/d/1YLn6Z2UjyHvtpES_IHdXTMnKivLhKFq_CAAXcKCP_Vc/edit?usp=sharing

## Definition of done
- Toteutetun koodin testikattavuus on kohtuullinen (~80 %).
- Asiakas voi aina nähdä koodin ja testien tilanteen CI-palvelusta. Testit menevät läpi CI:ssä.
- Hyväksymiskriteerit täyttyvät. Asiakas hyväksyy toteutetun koodin.
- Koodin tulee olla mahdollisimman ylläpidettävää, eli
  - nimeäminen on tehty järkevästi ja yhdenmukaisesti Pythonin tyylikäytänteiden mukaisesti
  - arkkitehtuuri on selkeää ja perusteltua
  - koodin tyyli on yhtenäistä, ja sitä valvotaan Pylintin avulla.
- Dokumentaatiota on päivitetty tarpeen mukaan.


## Versionhallintakäytännöt
- Hae uusin main 
  - `git checkout main` 
  - `git pull`
- Luo taskista uusi branch 
  - `git checkout -b omanimi/taskin-nimi`
  - `git add oma_muutos.py`
  - `git commit -m "oma commit"`
  - git push --set-upstream origin omanimitaskin-nimi
- Mahdollisimman usein kannattaa hakea uusin main
   - `git fetch origin`
   - `git merge origin/main`
   - resolvaa mahdolliset konfliktit
   - `git push`
- Githubissa luo uusi Pull Request 
   - lisää muut tiimiläiset katselmoijiksi 
   - linkkaa PR Discordiin muille tiedoksi
   - varmista, että CI-testit menevät läpi 
   - Mergeä mainiin 
   - tuhoa branch githubista 


## Asennusohjeet

### Tietokanta 
[README_db](documentation/README_db.md) 
