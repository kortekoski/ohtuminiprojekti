*** Settings ***
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References

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
    Input Text  author  John Trimmer
    Input Text  title  How to Avoid Huge Ships
    Input Text  year  1982
    Input Text  citation_key  Trimmer1982
    Select From List By Value  reftype  book
    Scroll Element Into View    xpath=//button[@type='submit']
    Click Button  Create
    Title Should Be  Reference app
    Page Should Contain  Reference created successfully!
    Page Should Contain  John Trimmer
    Page Should Contain  How to Avoid Huge Ships
    Page Should Contain  1982