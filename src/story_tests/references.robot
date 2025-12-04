*** Settings ***
Library          OperatingSystem
Library          RequestsLibrary
Resource         resource.robot
Suite Setup      Setup Suite
Suite Teardown   Close Browser
Test Setup       Reset References

*** Keywords ***
Setup Suite
    Open And Configure Browser
    Create Session    app    ${HOME_URL}

*** Test Cases ***
At start there are no references
    Go To  ${HOME_URL}
    Title Should Be  Reference app
    Page Should Contain  No references found

One reference is shown after adding it
    Add Test Reference
    Go To  ${HOME_URL}
    Page Should Contain    Threepwood
    Page Should Contain    clover

One reference is shown after adding it via input
    Go To  ${HOME_URL}/new_reference
    Click Link  Book
    Title Should Be  Create a new reference
    Input Text  author  John Trimmer
    Input Text  title  How to Avoid Huge Ships
    Input Text  year  1982
    Input Text  citation_key  Trimmer1982
    Click Button  Create Reference
    Title Should Be  Reference app
    Page Should Contain  created successfully!
    Page Should Contain  John Trimmer
    Page Should Contain  How to Avoid Huge Ships
    Page Should Contain  1982

Reference is not visible after deletion
    Add Test Reference
    Go To  ${HOME_URL}
    Click Button  delete-Test2025
    Alert Should Be Present
    Title Should Be  Reference app
    Page Should Contain  deleted successfully!
    Page Should Not Contain  Threepwood
    Page Should Not Contain  clover

Reference information is changed after update
    Add Test Reference
    Go To  ${HOME_URL}
    Click Link  update-Test2025
    Page Should Contain  Update Reference
    Clear Element Text  author
    Input Text  author  Hideo Kojima
    Click Button  Update Reference
    Wait Until Page Contains  updated successfully!  timeout=5s
    Title Should Be  Reference app
    Page Should Contain  updated successfully!
    Page Should Contain  Hideo Kojima
    Page Should Not Contain  Threepwood

Get to create reference via navbar
    Go To  ${HOME_URL}
    Click Link  Create Reference
    Title Should Be  Choose reference type

Get to frontpage via navbar
    Go To  ${HOME_URL}/new_reference
    Click Link  Home
    Title Should Be  Reference app

BibTeX is downloadable for a reference
    Add Test Reference
    Go To  ${HOME_URL}
    Page Should Contain  Download BibTeX
    ${response}=  GET On Session    app    /download_bibtex
    Should Be Equal As Integers  ${response.status_code}  200
    ${bibtex_content}=  Set Variable  ${response.text}
    Should Contain  ${bibtex_content}  @book{Test2025,
    Should Contain  ${bibtex_content}  author = {Guybrush Threepwood},
    Should Contain  ${bibtex_content}  title = {Different types of clover in Melee island},
    Should Contain  ${bibtex_content}  year = {2025}

Reference can be added by DOI
    Go To  ${HOME_URL}/new_reference
    Click Link  From DOI
    Title Should Be  Add a new reference from a DOI
    Input Text  doi  10.1136/jclinpath-2020-206745
    Input Text  citation_key  doicitation
    Click Button  Get Reference
    Wait Until Page Contains  created succesfully!  timeout=10s
    Title Should Be  Reference app
    Page Should Contain  Construction of a reference material

BibTeX download starts
    Add Test Reference
    Go To  ${HOME_URL}
    Click Link  Download BibTeX
    Alert Should Be Present

As a user I can choose only certain reference types
    Go To  ${HOME_URL}/new_reference
    Page Should Contain  Book
    Page Should Contain  Article
    Page Should Not Contain  Inproceedings
    Page Should Not Contain  Miscellaneous

When adding a book reference only the book specific fields are shown
    Go To  ${HOME_URL}/new_reference
    Click Link  Book
    Title Should Be  Create a new reference
    Page Should Contain  Author
    Page Should Contain  Title
    Page Should Contain  Year
    Page Should Contain  Citation Key
    Page Should Contain  Publisher
    Page Should Contain  ISBN
    Page Should Not Contain  Journal

When adding an article reference only the article specific fields are shown
    Go To  ${HOME_URL}/new_reference
    Click Link  Article
    Title Should Be  Create a new reference
    Page Should Contain  Author
    Page Should Contain  Title
    Page Should Contain  Year
    Page Should Contain  Citation Key
    Page Should Contain  Journal
    Page Should Contain  Number
    Page Should Contain  Pages
    Page Should Contain  DOI
    Page Should Not Contain  ISBN

As a user I want to add a title that is very short
    Go To  ${HOME_URL}/new_reference
    Click Link  Book
    Input Text  author  Test Author A
    Input Text  title  Ti
    Input Text  year  2000
    Input Text  citation_key  AB2000
    Click Button  Create Reference
    Page Should Contain  created successfully!
    Page Should Contain  Test Author A
    Page Should Contain  Ti

Two references can share the same author
    # Add first reference with author "Martin Fowler"
    Go To  ${HOME_URL}/new_reference
    Click Link  Book
    Input Text  author  Martin Fowler
    Input Text  title  Refactoring
    Input Text  year  1999
    Input Text  citation_key  Fowler1999
    Click Button  Create Reference
    Page Should Contain  created successfully!
    
    # Add second reference with the same author "Martin Fowler"
    Go To  ${HOME_URL}/new_reference
    Click Link  Book
    Input Text  author  Martin Fowler
    Input Text  title  Patterns of Enterprise Application Architecture
    Input Text  year  2002
    Input Text  citation_key  Fowler2002
    Click Button  Create Reference
    Page Should Contain  created successfully!
    
    # Verify both references appear on the home page with the shared author
    Go To  ${HOME_URL}
    Page Should Contain  Martin Fowler
    Page Should Contain  Refactoring
    Page Should Contain  1999
    Page Should Contain  Patterns of Enterprise Application Architecture
    Page Should Contain  2002
