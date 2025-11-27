# Arkkitehtuurikaavio: UI > Service > Repository > Database 
Projektissa on käytössä kerrosarkkitehtuuri. Lue aiheesta lisää täältä: 
[HY Ohjelmistotuotannon kurssi - Kerrosarkkitehtuuri](https://ohjelmistotuotanto-hy.github.io/osa4/#kerrosarkkitehtuuri)

````mermaid
flowchart TB

    subgraph UI["Templates (Presentation)"]
        Tmpl[HTML Templates<br/>Static files]
        AppPy[app.py<br/>API + reitit]
    end

    subgraph Service["Services  (Business logic)"]
        RefSvc[reference_service]
        ValSvc[validation_service]
    end

    subgraph Repo["Repositories (Persistence)"]
        RefRepo[reference_repository]
       
    end

    subgraph DB["Database"]
        SQL[(PostgreSQL)]
    end

    %% Connections
    Tmpl --> AppPy
    AppPy --> ValSvc
    ValSvc --> AppPy
    AppPy --> RefSvc
    RefSvc --> RefRepo
    RefRepo --> SQL
````

<br><br>

# Sekvenssikaavio: 
## API → Service → Repository → Database

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

````

<br><br>

````mermaid
flowchart TB

    %% === APPLICATION LAYERS ===
    subgraph API["API Layer"]
        APP["app.py"]
    end

    subgraph SERVICE["Service Layer"]
        RS["reference_service.py"]
        VS["validation_service.py"]
    end

    subgraph REPO["Repository Layer"]
        RR["reference_repository.py"]
    end


    DB["Database (SQLite / PostgreSQL)"]


    %% === TEST LAYERS (mirroring app structure) ===
    subgraph TAPI["API Integration Tests"]
        T_ROUTE["integration/test_reference_routes.py"]
    end

    subgraph TSERVICE["Service Tests"]
        T_RS["services/test_reference_service.py"]
        T_VS["services/test_validation_service.py"]
    end

    subgraph TREPO["Repository Tests"]
        T_REPO["repositories/test_reference_repository.py"]
    end

    subgraph TDATA["Jaettu testiaineisto"]
        TD["test_data.py"]
    end


    %% === MAPPINGS: Tests → Code ===
    %% API tests call app.py (routes)
    T_ROUTE --> APP

    %% Service tests target service layer
    T_RS --> RS
    T_VS --> VS

    %% Repository test targets repository layer
    T_REPO --> RR

    %% Shared test data is used by all tests
    TD --> T_ROUTE
    TD --> T_RS
    TD --> T_VS
    TD --> T_REPO

    %% Application dependencies
    RS --> RR
    VS --> RR
    RR --> DB


````