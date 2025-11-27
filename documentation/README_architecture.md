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
       
    end

    subgraph DB["Database"]
        SQL[(PostgreSQL / SQLite)]
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