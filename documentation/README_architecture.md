# Projektin yleisrakenne

````mermaid
flowchart TD

    A[Projektin juurikansio] --> B[documentation<br/><i>Dokumentaatio</i>]
    A --> C[migrations<br/><i>SQL tietokannan pystytykseen</i>]
    A --> D[misc<br/><i>Projektin aloitusohjeet</i>]

    %% SRC
    A --> E[src<br/><i>Koko sovelluksen koodi</i>]

    %% SRC contents
    E --> E1[entities<br/><i>Entity-luokat</i>]
    E --> E2[repositories<br/>• tietokantakyselyt<br/>• mapataa tulokset entityihin]
    E --> E3[services]
    E --> E4[static<br/>• CSS, kuvat<br/>• UI:n staattiset tiedostot]
    E --> E5[story_tests<br/>Robot Framework -testit]
    E --> E6[templates<br/>HTML UI -sivut]
    E --> E7[tests<br/>Unit- ja integraatiotestit]

    %% Services sisältö
    E3 --> S1[reference_service<br/>→ kutsuu reference_repositorya]
    E3 --> S2[validation_service<br/>→ validoi app.py:n sanomat]

    %% Tests sisältö
    E7 --> T1[repositories testit]
    E7 --> T2[services testit]
    E7 --> T3[test_reference_routes<br/>app.py reittien testit]

    %% Root files
    A --> F[app_library.py<br/><i>Robot testien helper</i>]
    A --> G[app.py<br/>• API-reitit<br/>• HTML-templatejen palveleminen]
    A --> H[config.py<br/>• Sovelluksen konfiguraatio]
    A --> I[db_helper.py<br/>• Testikannan alustaja]
    A --> J[index.py<br/>• Sovelluksen käynnistys]
    A --> K[util.py<br/>• Yleiset apufunktiot<br/>• enumeraatiot]
````
<br><br>

# Arkkitehtuurikaavio: UI > Service > Repository > Database 
````mermaid
flowchart LR

    subgraph UI["UI Layer"]
        Tmpl[HTML Templates<br/>Static files]
        AppPy[app.py<br/>API + reitit]
    end

    subgraph Service["Service Layer"]
        RefSvc[reference_service]
        ValSvc[validation_service]
    end

    subgraph Repo["Repository Layer"]
        RefRepo[reference_repository]
        OtherRepos[muut repositoryt]
    end

    subgraph DB["Database"]
        SQL[(PostgreSQL / SQLite)]
    end

    %% Connections
    Tmpl --> AppPy
    AppPy --> ValSvc
    AppPy --> RefSvc
    RefSvc --> RefRepo
    OtherRepos --> SQL
    RefRepo --> SQL
````

<br><br>

# Sequence diagram: API → Service → Repository → Database
````mermaid

sequenceDiagram
    participant User as User/Browser
    participant App as app.py (API)
    participant Val as validation_service
    participant Svc as reference_service
    participant Repo as reference_repository
    participant DB as Database

    User ->> App: HTTP GET /reference/{id}
    App ->> Val: validate(request)
    Val -->> App: validation OK

    App ->> Svc: get_reference(id)
    Svc ->> Repo: fetch_reference(id)
    Repo ->> DB: SELECT * FROM reference WHERE id = ?

    DB -->> Repo: result row
    Repo -->> Svc: entity mapped
    Svc -->> App: entity DTO
    App -->> User: JSON/HTML response

````
<br><br>

# Kaavio: Robot Framework -testit käyttävät app_librarya
````mermaid
flowchart TB

    RF["Robot Framework testit (.robot)"] --> AL["app_library.py (Custom Keywords)"]
    AL --> AppPy["app.py (API Routes)"]
    AL --> IndexPy["index.py (Application Startup)"]

    AppPy --> Services["Services Layer"]
    Services --> Repos["Repositories Layer"]
    Repos --> DB["Test Database"]

````