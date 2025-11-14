# Tietokannan asennus
Tietokanta käynnistetään lokaalisti docker-konttiin, josta sovellus aksessoi sitä. 

## Asenna koneellesi docker     
1. Fuksiläppäri: https://version.helsinki.fi/cubbli/cubbli-help/-/wikis/Docker
2. Ubuntu: https://docs.docker.com/engine/install/ubuntu/    
3. Mac: https://docs.docker.com/desktop/setup/install/mac-install/
4. Windows: https://docs.docker.com/desktop/setup/install/windows-install/  

## Lisää koneellesi .env-tiedosto 
Kopioi tämä sisältö: 
````   
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/neliapila
TEST_ENV=true
SECRET_KEY=satunnainen_merkkijono
```` 

## Käynnistä docker 
1. Avaa terminaali projektin juuressa
2. Suorita seuraava komento: `docker compose up`    (jos tämä ei toimi kokeile `docker-compose up`) 
3. Vaihtoehtoisesti voit käynnistää tietokannan niin, että docker pyörii taustalla (detached mode): 
`docker compose up -d`          

## Pysäytä kontti (data säilyy)
1. `docker compose down`      

## Aja alas koko tietokanta ja kaikki data
1. `docker compose down -v`     

# Suora yhteys kantaan 
1. Asenna koneellesi client, joka tukee postgres:iä: https://dbeaver.io/download/     
2. Avaa DBeaver     
3. 
    -  POSTGRES_USER: postgres
    -  POSTGRES_PASSWORD: postgres
    -  POSTGRES_DB: neliapila
      port:5432

      ![DBeaver](images/dbeaver.png)       