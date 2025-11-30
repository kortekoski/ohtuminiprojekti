# Arkkitehtuurikaavio: UI > Service > Repository > Database 
Projektissa on käytössä kerrosarkkitehtuuri. Lue aiheesta lisää täältä: 
[HY Ohjelmistotuotannon kurssi - Kerrosarkkitehtuuri](https://ohjelmistotuotanto-hy.github.io/osa4/#kerrosarkkitehtuuri)

```mermaid
flowchart TB

    subgraph UI["Templates (Presentation)"]
        Tmpl[HTML Templates<br/>Static files]
        AppPy[app.py<br/>API + reitit]
    end

    subgraph Service["Services  (Business logic)"]
        RefSvc[reference_service]
        ValSvc[validation_service]
        BibSvc[bibtex_service]
    end

    subgraph Repo["Repositories (Persistence)"]
        RefRepo[reference_repository]
    end

    subgraph DB["Database"]
        SQL[(PostgreSQL)]
    end

    %% Connections
    Tmpl --> AppPy

    %% UI -> Services
    AppPy --> ValSvc
    AppPy --> RefSvc
    AppPy --> BibSvc

    %% Service -> UI
    ValSvc --> AppPy
    BibSvc --> AppPy

    %% Service -> Repository -> DB
    RefSvc --> RefRepo
    RefRepo --> SQL

```

<br><br>

# Sekvenssikaavio: 
## API → Service → Repository → Database

```mermaid

sequenceDiagram
    participant User as User/Browser
    participant App as app.py (Route)
    participant G as Flask g
    participant Svc as ReferenceService
    participant Val as ValidationService
    participant Repo as ReferenceRepository
    participant DB as Database

    User ->> App: POST /create_reference <br/> form data

    App ->> App: Read form fields

    Note over App: Acquire service through DI helper
    App ->> G: get_reference_service()
    G ->> G: Create ReferenceService() if missing
    G ->> App: return cached service (Svc)

    App ->> Svc: get_citation_keys()
    Svc ->> Repo: get_citation_keys()
    Repo ->> DB: SELECT citation_key FROM reference_values
    DB -->> Repo: list of citation keys
    Repo -->> Svc: citation_key list
    Svc -->> App: citation_key list

    App ->> App: Construct Reference object

    App ->> Val: validate_reference(ref, existing_keys)
    Val -->> App: validation OK

    App ->> Svc: create_reference(citation_key, year, author, title, reftype)

    Svc ->> Repo: create_reference(...)
    Repo ->> DB: INSERT INTO reference_values (...)
    DB -->> Repo: commit OK
    Repo -->> Svc: success
    Svc -->> App: success

    App -->> User: Redirect to "/"
```
<br><br>



# Kaavio: Robot Framework -testit käyttävät app_librarya
```mermaid
flowchart TB

    RF["references.robot<br/>(varsinaiset testit)"]
    RES["resource.robot<br/>(konfiguraatio / avainsanat)"]
    AL["app_library.py<br/>(mukautettu toiminnallisuus)"]
    AppPy["app.py<br/>(API Routes)"]
    IndexPy["index.py<br/>(Sovelluksen käynnistäminen)"]
    Services["Services Layer"]
    Repos["Repositories Layer"]
    DB["Test Database"]

    RF --> RES
    RES --> AL
    AL --> AppPy
    AL --> IndexPy

    AppPy --> Services
    Services --> Repos
    Repos --> DB

```

<br><br>

# Testit ja niiden suhde ohjelmakoodiin

```mermaid
flowchart TB

    %% === APPLICATION LAYERS ===
    subgraph API["API Layer"]
        APP["app.py"]
    end

    subgraph SERVICE["Service Layer"]
        RS["reference_service.py"]
        VS["validation_service.py"]
        BS["bibtex_service.py"]
    end

    subgraph REPO["Repository Layer"]
        RR["reference_repository.py"]
    end

    DB["Database (PostgreSQL)"]


    %% === TEST LAYERS (mirroring app hierarchy) ===
    subgraph TAPI["integration"]
        T_ROUTE["test_reference_routes.py"]:::testnode
    end

    subgraph TSERVICE["services"]
        T_RS["test_reference_service.py"]:::testnode
        T_VS["test_validation_service.py"]:::testnode
        T_BS["test_bibtex_service.py"]:::testnode
    end

    subgraph TREPO["repositories"]
        T_REPO["test_reference_repository.py"]:::testnode
    end

    subgraph TDATA["Jaettu testiaineisto"]
        TD["test_data.py"]:::testnode
    end


    %% === TEST → CODE MAPPINGS ===
    T_ROUTE --> APP

    %% === APPLICATION DEPENDENCIES ===
    APP --> RS
    APP --> VS
    APP --> BS

    T_RS --> RS
    T_VS --> VS
    T_BS --> BS

    T_REPO --> RR

    TD --> T_ROUTE
    TD --> T_RS
    TD --> T_VS
    TD --> T_BS
    TD --> T_REPO

    RS --> RR
    RR --> DB


    %% === CUSTOM STYLE FOR TEST NODES ===
    classDef testnode fill:#fdf6e3,stroke:#b58900,stroke-width:2px,color:#333,font-weight:bold;

```