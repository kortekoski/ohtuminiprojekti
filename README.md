# Ohtun miniprojekti, syksy 2025 (team Neliapila)
[![GHA workflow_badge](https://github.com/kortekoski/ohtuminiprojekti/actions/workflows/ci.yaml/badge.svg)](https://github.com/kortekoski/ohtuminiprojekti/actions)
## Ohjelman käynnistäminen

Sovellus käynnistetään Poetry-virtuaaliympäristössä komennolla
````
python src/index.py
````
Tietokanta käynnistetään projektin juuressa (erillisessä terminaalissa) komennolla 
````
docker compose up
````
Huomaa, että jos tietokantaskeeman taulujen ja entiteettien rakenne muuttuu, tietokanta kannattaa tuhota ja luoda se uudestaan. Tietokantaan ajetaan automaattisesti migraatiot kansiosta `migrations` aakkosjärjestyksessä, kun se ensimmäistä kertaa luodaan.
```` 
docker compose down -v
docker compose up
```` 

## Testaaminen 
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
Kaikki testit suoritetaan komennolla:
````
sh ./src/scripts/run-tests.sh
````


## Tyylit ja formatointi

Pylint komennolla:
```` 
poetry run pylint .
````
Formatointi blackilla:
```` 
poetry run black .
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
- Hae uusin `dev`
  - `git fetch`
  - `git checkout dev`
  - `git pull`
- Luo taskista uusi branch 
  - `git checkout -b omanimi/taskin-nimi`
  - `git add oma_muutos.py`
  - `git commit -m "oma commit"`
  - `git push --set-upstream origin omanimitaskin-nimi`
- Mahdollisimman usein kannattaa hakea uusin dev (ja aina ennen PR:n luomista)
   - `git fetch origin`
   - `git merge origin/dev`
   - resolvaa mahdolliset konfliktit
   - `git push`
- Githubissa luo uusi Pull Request 
   - Lisää muut tiimiläiset katselmoijiksi 
   - Linkkaa PR Discordiin muille tiedoksi
   - Varmista, että CI-testit menevät läpi 
   - Mergeä deviin
   - Tuhoa branch githubista 

### Sprint release 
- Sprintin lopuksi luodaan toimivasta `dev` branchista release `main`-haaraan     
- Lisätään version tag: git tag -a v1.0.0 -m "Release 1.0.0"     
- Luo PR dev -> main      
- Koko tiimi katselmoi     


## Asennusohjeet

### Tietokanta 
[README_db](documentation/README_db.md) 
