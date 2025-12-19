# Miniprojektiraportti

Tässä raportissa käydään läpi ohjelmistotuotannon miniprojektia, johon ovat osallistuneet Mika Kortekoski, Saara-Maija Pakarinen, Jeremias Setälä ja Teemu Vierros. Aluksi eritellään esiin tulleita ongelmia sprinteittäin – ongelmiin laaditut kehitystoimenpiteet on eritelty retrospektiivien muistiinpanoissa. Tämän jälkeen käsitellään sitä, miten projekti on sujunut, mitä on opittu ja mitä olisi vielä haluttu oppia.

---

## Ongelmat

### Sprintti 1
- Kommunikaatiota kaivattiin lisää sekä Discordissa että fyysisesti. Toisten tekemisistä oli vaikea pysyä perillä.
- Hyväksymiskriteerit kirjattiin ylös vasta työn aloittamisen jälkeen. Ne eivät siis varsinaisesti ohjanneet työntekoa, vaikka niin olisi tarkoitus.
- Yhteisen repositorion käyttöön ei ollut tarkkoja pelisääntöjä. Koodia pushattiin myös suoraan mainiin ilman pull requestia.
- Koodi oli paikoin laadutonta. Pylint antoi koodille luokattoman arvosanan.
- Testien ajaminen koettiin hankalaksi, koska se vaati aina usean komentorivikomennon ajamista sekä testiaineiston luomista.

### Sprintti 2
- Sprintin aikana koodiin tehtiin laajahkoa refaktorointia koodin laadunparannuksen vuoksi (jaottelu kansioihin, kerrosarkkitehtuurin noudattaminen, taikanumerot enumeraatioiksi, testidata omaan tiedostoonsa), minkä seurauksena päädyttiin laatimaan arkkitehtuurikaavio, jotta muutokset ja rakenne olisivat koko tiimille selviä.
- Edellisen sprintin päätteeksi sovittiin, että käytetään omia brancheja eikä pusketa koodia suoraan mainiin.
- Edellisen sprintin päätteeksi sovittiin, että toisen tiimiläisen pitäisi aina hyväksyä pull request ennen koodin mergeämistä main-haaraan. Tämä käytäntö lisäsi kuitenkin odottelua – prosessiin syntyi siis konkreettinen esimerkki leanissa määritellystä hukasta.
- Hukkaa havaittiin myös toisaalla: edellisen sprintin aikana tehty rajapinta todettiin turhaksi varastoiduksi koodiksi ja poistettiin projektista. Ongelman yhteydessä keskusteltiin laajemmin siitä, että tehdyn työn tulisi keskittyä juuri haluttujen toiminnallisuuksien tuottamiseen.
- Yksi toiminnallisuus hajosi juuri ennen katselmointia, koska sitä yritettiin viilata paremmaksi viime hetkellä. Päätettiin, että demoa varten tehdään release toimivasta koodista.

### Sprintti 3
- Commitit hajottivat main-haaran liian usein, jonka vuoksi otettiin käyttöön erillinen dev-haara. Dev-haarasta luotiin vakaa release sprintin keskellä ja myös demoa varten. 
- Robot testit eivät vastanneet riittävän tarkasti user storyjen määrittämiä lupauksia toiminnallisuuksista. Ongelma korostui, kun erikseen kirjoitetuista hyväksymiskriteereistä siirryttiin robot testeihin. Sovittiin, että siirrytään kirjoittamaan hyväksymiskriteerit siten, että robot testin nimi on suoraan hyväksymiskriteeri. 
- Koodin laadussa ja rakenteessa nousi esiin esimerkiksi nimeämisiin liittyviä ongelmia.

### Sprintti 4
- Koodissa havaittiin toisteisuutta ja sitä pyrittiin vähentämään koko sprintin ajan.
- Myös nimeämisiä pyrittiin parantamaan koko sprintin ajan. 
- Pohdittiin, että mikäli projekti olisi jatkunut pitempään, päivittäinen lyhyt läpikäynti eli daily tiimin kesken olisi parantanut kommunikaatiota vieläkin enemmän. 

---

## Yhteenveto

Yleisesti projekti on sujunut ryhmän mielestä hyvin. Kommunikaatio on ollut koko projektin ajan sujuvaa ja avointa. Työskentelyprosessin ja koodin ongelmia on nostettu rohkeasti esiin, minkä lisäksi laaditut kehitystoimenpiteet on otettu oikeasti käyttöön. Ryhmässä on siis ollut vahva jatkuvan parantamisen kulttuuri, mikä on johtanut ongelmien vähentymiseen sprinttien edetessä. Lean-periaatteiden hengessä myös hukkaa on pyritty poistamaan. Käytännössä hyvin sujunut työskentely on näkynyt esimerkiksi siten, että kunkin sprintin aikana on saatu toteutettua halutut toiminnallisuudet. Lopputuloksena syntyneeseen ohjelmistoon voi olla tyytyväinen.

Aina jää kuitenkin parannettavaa. Esimerkiksi katselmointeja olisi voinut harrastaa enemmän ja yhdessä keskustellen; ne olisivat tehostaneet oppimista ja parantaneet koodin laatua. Koodia katselmoitiin pull requestien yhteydessä vain melko kursorisesti. Ryhmän kokeneempi koodari pohti myös sitä, että hän teki projektin alussa ehkä liikaa asioita itse sen sijaan, että olisi tehnyt vain parannusehdotuksia, sparrannut ja auttanut muita oppimaan. Tämä lienee ongelmana aina, kun eritasoiset tekijät ympätään yhteen työryhmään. Toisaalta tässäkin löytyi tiimille sopiva rytmi sprinttien edetessä.  

Suurin osa tiimistä koodasi ryhmässä ensimmäistä kertaa, joten opittavaa oli paljon. Projektin aikana ryhmäläiset oppivat esimerkiksi koordinoimaan töitä eri tekijöiden välillä, toimimaan yhteisen koodikannan parissa ja soveltamaan Scrumin käytänteitä. Versionhallintaa ja erilaisten työvälineiden hyödyntämistä tuli myös opeteltua ahkerasti (esim. Git, GitHub Actions ja Codecov). Ryhmäläiset oppivat lisäksi paljon monipuolisesta ohjelmistotestauksesta.

Projektin aikana olisi voitu käyttää myös enemmän ohjelmistotuotannossa yleisesti käytettyjä ohjelmistoja. Product backlogin, sprint backlogin ja burndown-käyrien hallinnointi onnistui Excelissäkin, mutta yleisesti alalla käytettyjen ohjelmistojen käyttö (esim. Jira ja Github Projects) voisi palvella paremmin kurssin oppimistavoitteita. Myös sovelluksen deployaaminen esimerkiksi Githubin kautta tai jopa yliopiston servereille aladomainiin olisi ollut hauska ja opettavainen lisä projektiin.

Kurssin laskuharjoituksista tuttujen suunnittelumallien käyttämistä olisi myös voitu edellyttää projektissa. Näin niiden oppiminen tehostuisi käytännön kautta. Projekti voisi lisäksi olla hyvä mahdollisuus harjoitella tietoturvavaatimusten täyttämistä websovelluksessa.

Turhalta ei ole tuntunut varsinaisesti muu kuin epähuomiossa tehty hukkatyö – kaiken kaikkiaan projekti on ollut erinomainen tapa opetella kurssin asioita käytännössä. Mieleen on noussut lähinnä siihen lisättäviä asioita, ei juuri poistettavaa. Projektin aihe on myös ollut mielenkiintoinen, ja siihen liittyen on ollut vaivatonta keksiä uusia toiminnallisuuksia. Teknisten ratkaisujen pohtiminen (mm. PostgreSQL-tietokannan ja BibLaTeX-formaatin käyttö) on lisäksi ollut mielekästä. Ryhmä on suoritukseensa ja oppimaansa tyytyväinen, joten tästä on hyvä jatkaa eteenpäin.
