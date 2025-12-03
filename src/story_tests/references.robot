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
    Title Should Be  Reference app
    Page Should Contain  created succesfully!
    Page Should Contain  Construction of a reference material
