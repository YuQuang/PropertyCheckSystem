*** Settings ***
Library    Browser
Variables  ../variables.py

Suite Setup        SuiteSetup
Suite Teardown     SuiteTeardown

*** Test Cases ***
Check accept cookie popup window
    Get Text    //*[@id="navbar"]/div/div[1]    ==    Welcome
    Get Text    //*[@id="navbar"]/div/div[2]    ==    You need to accept using Cookie, you can see detail on EULA, thanks.
    Wait For Elements State    //*[@id="navbar"]/div/button[1]
    Wait For Elements State    //*[@id="navbar"]/div/button[2]
    Click    //*[@id="navbar"]/div/button[1]
    Get Element States    //*[@id="navbar"]/div    *=    hidden
    

*** Keywords ***
SuiteSetup
    New Browser    browser=chromium    headless=${TRUE}
    New Context    ignoreHTTPSErrors=${TRUE}    recordVideo=${RECORD_SETTING}
    New Page    ${SITE_BASE_URL}

SuiteTeardown
    Close Browser