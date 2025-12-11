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
    Page Should Contain    Threeplog
    Page Should Contain    clover

One reference is shown after adding it via input
    Go To  ${HOME_URL}/new_reference
    Click Link  Book
    Title Should Be  Create a new reference
    Input Text  last_name  Trimmer
    Input Text  first_name  John
    Input Text  title  How to Avoid Huge Ships
    Input Text  year  1982
    Input Text  citation_key  Trimmer1982
    Click Button  Create Reference
    Title Should Be  Reference app
    Page Should Contain  created successfully!
    Page Should Contain  Trimmer, J.
    Page Should Contain  How to Avoid Huge Ships
    Page Should Contain  1982

Reference is not visible after deletion
    Add Test Reference
    Go To  ${HOME_URL}
    Click Button  delete-Test2025
    Alert Should Be Present
    Title Should Be  Reference app
    Page Should Contain  deleted successfully!
    Page Should Not Contain  Threeplog
    Page Should Not Contain  clover

Multiple references can be deleted if they are selected via checkbox
    Add Multiple Test References
    Go To  ${HOME_URL}
    Select Checkbox  select-Smith2020
    Select Checkbox  select-Johnson2021
    Click Button  delete-selected
    Handle Alert  accept
    Page Should Contain  deleted successfully
    Page Should Not Contain  Introduction to Software Testing
    Page Should Not Contain  Advanced Database Systems
    Page Should Contain  Machine Learning in Practice

If no references are selected, none will be deleted by selection delete
    Add Multiple Test References
    Go To  ${HOME_URL}
    Click Button  delete-selected
    Alert Should Be Present
    Page Should Contain  Introduction to Software Testing
    Page Should Contain  Advanced Database Systems
    Page Should Contain  Machine Learning in Practice

Reference information is changed after update
    Add Test Reference
    Go To  ${HOME_URL}
    Click Link  update-Test2025
    Page Should Contain  Update Reference
    Clear Element Text  xpath=//input[@name='last_name']
    Clear Element Text  xpath=//input[@name='first_name']
    Input Text  last_name  Kojima
    Input Text  first_name  Hideo
    Click Button  Update Reference
    Wait Until Page Contains  updated successfully!  timeout=5s
    Title Should Be  Reference app
    Page Should Contain  updated successfully!
    Page Should Contain  Kojima, H.
    Page Should Not Contain  Threeplog

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
    Should Contain  ${bibtex_content}  author = {Threeplog, Guybroom},
    Should Contain  ${bibtex_content}  title = {Different types of clover in Melee island},
    Should Contain  ${bibtex_content}  year = {2025}

BibTeX is downloadable for a selected reference
    Add Test Reference
    Go To  ${HOME_URL}
    Page Should Contain  Download selected BibTeX
    Click Button  download-selected
    Page Should Contain  No references selected for download
    Select Checkbox  select-Test2025
    ${response}=  GET On Session    app    url=/download_selected_bibtex?ids=Test2025
    Should Be Equal As Integers  ${response.status_code}  200
    ${bibtex_content}=  Set Variable  ${response.text}
    Should Contain  ${bibtex_content}  @book{Test2025,
    Should Contain  ${bibtex_content}  author = {Threeplog, Guybroom},
    Should Contain  ${bibtex_content}  title = {Different types of clover in Melee island},
    Should Contain  ${bibtex_content}  year = {2025}

Copy BibTeX button copies all references to clipboard
    Add Test Reference
    Go To  ${HOME_URL}
    Page Should Contain  Copy BibTeX to Clipboard
    Click Button  clipboardcopy
    Handle Alert  accept
    Sleep  500ms
    ${clipboard_content}=  Execute Javascript  return window.lastCopiedBibtex || '';
    Should Contain  ${clipboard_content}  @book{Test2025,
    Should Contain  ${clipboard_content}  author = {Threeplog, Guybroom},
    Should Contain  ${clipboard_content}  title = {Different types of clover in Melee island},
    Should Contain  ${clipboard_content}  year = {2025}

Copy selected BibTeX button copies selected references to clipboard
    Add Test Reference
    Go To  ${HOME_URL}
    Page Should Contain  Copy selected BibTeX to Clipboard
    Click Button  clipboardcopy-selected
    Alert Should Be Present  No entries to copy!
    Select Checkbox  select-Test2025
    Click Button  clipboardcopy-selected
    Handle Alert  accept
    Sleep  500ms
    ${clipboard_content}=  Execute Javascript  return window.lastCopiedBibtex || '';
    Should Contain  ${clipboard_content}  @book{Test2025,
    Should Contain  ${clipboard_content}  author = {Threeplog, Guybroom},
    Should Contain  ${clipboard_content}  title = {Different types of clover in Melee island},
    Should Contain  ${clipboard_content}  year = {2025}

Reference can be added by DOI
    Go To  ${HOME_URL}/new_reference
    Click Link  From DOI
    Title Should Be  Add a new reference from a DOI
    Input Text  doi  10.1136/jclinpath-2020-206745
    Input Text  citation_key  doicitation
    Click Button  Get Reference
    Wait Until Page Contains  created successfully!  timeout=10s
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
    Input Text  last_name  Author
    Input Text  first_name  Test
    Input Text  title  Ti
    Input Text  year  2000
    Input Text  citation_key  AB2000
    Click Button  Create Reference
    Page Should Contain  created successfully!
    Page Should Contain  Author, T.
    Page Should Contain  Ti

Two references can share the same author
    # Add first reference with author "Martin Fowler"
    Go To  ${HOME_URL}/new_reference
    Click Link  Book
    Input Text  last_name  Fowler
    Input Text  first_name  Martin
    Input Text  title  Refactoring
    Input Text  year  1999
    Input Text  citation_key  Fowler1999
    Click Button  Create Reference
    Page Should Contain  created successfully!
    
    # Add second reference with the same author "Martin Fowler"
    Go To  ${HOME_URL}/new_reference
    Click Link  Book
    Input Text  last_name  Fowler
    Input Text  first_name  Martin
    Input Text  title  Patterns of Enterprise Application Architecture
    Input Text  year  2002
    Input Text  citation_key  Fowler2002
    Click Button  Create Reference
    Page Should Contain  created successfully!
    
    # Verify both references appear on the home page with the shared author
    Go To  ${HOME_URL}
    Page Should Contain  Fowler, M.
    Page Should Contain  Refactoring
    Page Should Contain  1999
    Page Should Contain  Patterns of Enterprise Application Architecture
    Page Should Contain  2002

Duplicate authors in a single reference are rejected
    Go To  ${HOME_URL}/new_reference
    Click Link  Book
    Wait Until Page Contains Element  name:last_name  timeout=5s
    # Fill first author
    Input Text  xpath=(//input[@name='last_name'])[1]  Martin
    Input Text  xpath=(//input[@name='first_name'])[1]  Robert
    # Click the button to add another author field
    Wait Until Page Contains Element  css:button[onclick="addAuthor()"]  timeout=5s
    Click Element  css:button[onclick="addAuthor()"]
    # Wait for the second author input to appear
    Wait Until Element Is Visible  xpath=(//input[@name='last_name'])[2]  timeout=5s
    # Fill second author with same name
    Input Text  xpath=(//input[@name='last_name'])[2]  Martin
    Input Text  xpath=(//input[@name='first_name'])[2]  Robert
    # Fill other required fields
    Input Text  title  Clean Code
    Input Text  year  2008
    Input Text  citation_key  Martin2008
    # Submit the form
    Click Button  Create Reference
    # Should see error about duplicates
    Page Should Contain  duplicate
    Page Should Not Contain  created successfully!

Author names are displayed with proper abbreviation format
    # Test with 1 author - should display as "Lastname, F."
    Go To  ${HOME_URL}/new_reference
    Click Link  Book
    Input Text  last_name  Smith
    Input Text  first_name  John
    Input Text  title  One Author Book
    Input Text  year  2020
    Input Text  citation_key  Smith2020
    Click Button  Create Reference
    Go To  ${HOME_URL}
    Page Should Contain  Smith, J.
    
    # Test with 2 authors - should display as "X and Y"
    Go To  ${HOME_URL}/new_reference
    Click Link  Book
    Input Text  xpath=(//input[@name='last_name'])[1]  Johnson
    Input Text  xpath=(//input[@name='first_name'])[1]  Alice
    Wait Until Page Contains Element  css:button[onclick="addAuthor()"]  timeout=5s
    Click Element  css:button[onclick="addAuthor()"]
    Wait Until Element Is Visible  xpath=(//input[@name='last_name'])[2]  timeout=5s
    Input Text  xpath=(//input[@name='last_name'])[2]  Brown
    Input Text  xpath=(//input[@name='first_name'])[2]  Bob
    Input Text  title  Two Authors Book
    Input Text  year  2021
    Input Text  citation_key  Johnson2021
    Click Button  Create Reference
    Go To  ${HOME_URL}
    Page Should Contain  Johnson, A. and Brown, B.
    
    # Test with 3 authors - should display as "X and Y and Z"
    Go To  ${HOME_URL}/new_reference
    Click Link  Book
    Input Text  xpath=(//input[@name='last_name'])[1]  Davis
    Input Text  xpath=(//input[@name='first_name'])[1]  Carol
    Wait Until Page Contains Element  css:button[onclick="addAuthor()"]  timeout=5s
    Click Element  css:button[onclick="addAuthor()"]
    Wait Until Element Is Visible  xpath=(//input[@name='last_name'])[2]  timeout=5s
    Input Text  xpath=(//input[@name='last_name'])[2]  Evans
    Input Text  xpath=(//input[@name='first_name'])[2]  David
    Click Element  css:button[onclick="addAuthor()"]
    Wait Until Element Is Visible  xpath=(//input[@name='last_name'])[3]  timeout=5s
    Input Text  xpath=(//input[@name='last_name'])[3]  Foster
    Input Text  xpath=(//input[@name='first_name'])[3]  Emily
    Input Text  title  Three Authors Book
    Input Text  year  2022
    Input Text  citation_key  Davis2022
    Click Button  Create Reference
    Go To  ${HOME_URL}
    Page Should Contain  Davis, C. and Evans, D. and Foster, E.
    
    # Test with 4+ authors - should display as "X et al."
    Go To  ${HOME_URL}/new_reference
    Click Link  Book
    Input Text  xpath=(//input[@name='last_name'])[1]  Garcia
    Input Text  xpath=(//input[@name='first_name'])[1]  Frank
    Wait Until Page Contains Element  css:button[onclick="addAuthor()"]  timeout=5s
    Click Element  css:button[onclick="addAuthor()"]
    Wait Until Element Is Visible  xpath=(//input[@name='last_name'])[2]  timeout=5s
    Input Text  xpath=(//input[@name='last_name'])[2]  Harris
    Input Text  xpath=(//input[@name='first_name'])[2]  Grace
    Click Element  css:button[onclick="addAuthor()"]
    Wait Until Element Is Visible  xpath=(//input[@name='last_name'])[3]  timeout=5s
    Input Text  xpath=(//input[@name='last_name'])[3]  Irving
    Input Text  xpath=(//input[@name='first_name'])[3]  Henry
    Click Element  css:button[onclick="addAuthor()"]
    Wait Until Element Is Visible  xpath=(//input[@name='last_name'])[4]  timeout=5s
    Input Text  xpath=(//input[@name='last_name'])[4]  Jackson
    Input Text  xpath=(//input[@name='first_name'])[4]  Iris
    Input Text  title  Four Authors Book
    Input Text  year  2023
    Input Text  citation_key  Garcia2023
    Click Button  Create Reference
    Go To  ${HOME_URL}
    Page Should Contain  Garcia, F. et al.


As a user I can see all fields of a reference in the main view
    Add Test Reference
    Go To  ${HOME_URL}
    Page Should Contain  Test2025
    Page Should Contain  Threeplog, G.
    Page Should Contain  Different types of clover in Melee island
    Page Should Contain  2025
    Page Should Contain  LocusArts
    Page Should Contain  A classic adventure game reference

