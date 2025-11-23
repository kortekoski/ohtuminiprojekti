# Retrospektiivien muistiinpanot

## Sprintti 1

Retrospektiivissä käsiteltiin ensimmäisen sprintin työskentelyprosessia Glad, Sad, Mad -tekniikkaa soveltamalla. Aluksi kukin tiimin jäsenistä kirjoitti työskentelyprosessista kolme huomiota lapuille. Tämän jälkeen lappujen huomiot esiteltiin lyhyesti ja laput sijoitettiin pöydälle sen mukaan, mitä tunnetta huomio herättää. Pöydällä oli hymynaama, surunaama ja vihainen naama. Kun laput oli esitelty, tiimin jäsenet antoivat yhdelle lapulle kolme ääntä, toiselle kaksi ja kolmannelle yhden sen mukaan, mistä he halusivat keskustella eniten. Ääniä saaneista asioista keskusteltiin, kunnes keskustelu hiipui.

Yleisesti ottaen tiimi oli tyytyväinen siihen, miten sprintti oli sujunut. Keskustelussa kiiteltiin ryhmän yleistä ilmapiiriä, hyvää kommunikaatiota ja tasaista vastuunjakoa. Yhteiset työskentelysäännöt olivat myös selkeät, joten yhteistyö sujui hyvin esimerkiksi eri branchien kanssa.

![retro 1](https://retro1.tiiny.site/retro1.png)

*Laput pöydällä alueille sijoiteltuna.*

<br>

### Kehitystoimenpiteet

Esille nousi myös muutama ”surua” herättänyt asia, joihin sovittiin kehitystoimenpiteitä:
-	**Kommunikaatio**: Discord-keskustelun ja viikottaisen ”weeklyn” lisäksi voisi harkita lyhyitä daily-tyyppisiä läpikäyntejä esimerkiksi pari kertaa viikossa.  Tämä voisi johtaa läpinäkyvämpään työskentelyyn, jolloin kaikki pysyisivät paremmin kartalla toistensa työskentelystä ja päällekkäisyyksiä vältettäisiin. Pitäisi myös työnteon aktiivisena ja nostaisi esiin mahdollisia esteitä. Sovittiin kehitystoimenpiteenä, että lauantaisin kaikki ovat läsnä Discordin voice chatissa klo 13.00. Lisäksi sovittiin, että tavataan puoli tuntia ennen seuraavaa reviewiä.
-	**Hyväksymiskriteerit**: Kriteerit pitäisi laatia heti sprintin alussa ja edellistä tarkemmin. Näin kaikki tietävät, mitä ominaisuudelta vaaditaan ja millaiset testit pitää kehittää. Tarkkuuden taso voisi olla esimerkiksi: ”Robot-testi testaa, että viite lisätään.” Kehitystoimenpiteenä hyväksymiskriteerit käydään läpi sprintin 2 suunnittelussa.
-	**Pull requestit**: Edellisen keskustelun rönsyssä todettiin, että suoraan mergeäminen mainiin ei ole siistiä. Sovittiin, että jokainen PR on hyväksyttävä Githubissa ennen mergeämistä. Lisäksi toivottiin, että koodista voisi nostaa esiin huomioita reviewissä.
-	**Testaaminen**: Nykyisellään testaus on ollut työlästä, koska se vaatii paljon komentojen syöttämistä (docker ylös, sovellus ylös, yksikkötestit, robot-testit). Kehitystoimenpiteenä toteutetaan Poetryn scripti, joka käynnistää kaiken ja ajelee testit läpi.
-	**Linttaus**: Koodi on sotkuista, eikä pylint-pisteitä heru. Sovittiin Black-formatterin käyttöönotosta commit hookina, jotta koodi vähän selkeytyy.
