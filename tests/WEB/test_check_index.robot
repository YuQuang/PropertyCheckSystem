*** Settings ***
Library    Browser
Variables  ../variables.py

Suite Setup        SuiteSetup
Suite Teardown     SuiteTeardown

*** Test Cases ***
Index page can show chart after login
    [Setup]    Login with valid user
    Verify chart shown after login
    [Teardown]    Go To    ${SITE_BASE_URL}/accounts/logout/

*** Keywords ***
SuiteSetup
    New Browser    browser=chromium    headless=${TRUE}
    New Context    ignoreHTTPSErrors=${TRUE}    recordVideo=${RECORD_SETTING}
    New Page    ${SITE_BASE_URL}

SuiteTeardown
    Close Browser

Login with valid user
    Go To    ${SITE_BASE_URL}/accounts/login/
    Fill Text    //*[@id="id_username"]    ${VALID_USER}
    Fill Text    //*[@id="id_password"]    ${VALID_PW}
    Click    //*[@id="login-button"]
    Wait Until Network Is Idle

Verify chart shown after login
    Wait Until Network Is Idle
    Wait For Elements State    //*[@id="rent_status"]
    Wait For Elements State    //*[@id="pandian_status"]
    Wait For Elements State    //*[@id="position_status"]
    Wait For Elements State    //*[@id="limit_status"]