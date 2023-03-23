*** Settings ***
Library    Browser

Suite Setup        SuiteSetup
Suite Teardown     SuiteTeardown

*** Variables ***
${SITE_BASE_URL} =   http://127.0.0.1:8000/
${VALID_USER} =      testuser
${VALID_PW} =        testpassword
${INVALID_USER} =    invalidUser
${INVALID_PW} =      invalidPassword


*** Test Cases ***
Login with valid user should success
    [Setup]    Go To    ${SITE_BASE_URL}/accounts/login/
    Fill Text    //*[@id="id_username"]    ${VALID_USER}
    Fill Text    //*[@id="id_password"]    ${VALID_PW}
    Click    //*[@id="login-button"]
    Verify chart shown after login
    [Teardown]    Go To    ${SITE_BASE_URL}/accounts/logout/

Login with invalid user should get error message
    [Setup]    Go To    ${SITE_BASE_URL}/accounts/login/
    Fill Text    //*[@id="id_username"]    ${INVALID_USER}
    Fill Text    //*[@id="id_password"]    ${INVALID_PW}
    Click    //*[@id="login-button"]
    Verify login failed error message

*** Keywords ***
SuiteSetup
    New Browser    browser=chromium    headless=${TRUE}
    New Page    ${SITE_BASE_URL}

SuiteTeardown
    Close Browser

Verify chart shown after login
    Wait Until Network Is Idle
    Wait For Elements State    //*[@id="rent_status"]
    Wait For Elements State    //*[@id="pandian_status"]
    Wait For Elements State    //*[@id="position_status"]
    Wait For Elements State    //*[@id="limit_status"]

Verify login failed error message
    Wait Until Network Is Idle
    Get Text    //p[@class="login-hint"]    ==    username or password is incorrect.