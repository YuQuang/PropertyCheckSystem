*** Settings ***
Library      Browser
Variables    ../variables.py

Suite Setup        SuiteSetup
Suite Teardown     SuiteTeardown

*** Test Cases ***
Check top navbar have list links
    Get Attribute    //*[@id="navbar"]/nav/div[1]/div/div[2]/div[2]/div/a[1]    href    ==    /
    Get Attribute    //*[@id="navbar"]/nav/div[1]/div/div[2]/div[2]/div/a[2]    href    ==    /importXslxFromSchool/
    Get Attribute    //*[@id="navbar"]/nav/div[1]/div/div[2]/div[2]/div/a[3]    href    ==    /search
    Get Attribute    //*[@id="navbar"]/nav/div[1]/div/div[2]/div[2]/div/a[4]    href    ==    /addData/
    Get Attribute    //*[@id="navbar"]/nav/div[1]/div/div[2]/div[2]/div/a[5]    href    ==    /leaseProperty/

*** Keywords ***
SuiteSetup
    New Browser    browser=chromium    headless=${TRUE}
    New Context    ignoreHTTPSErrors=${TRUE}
    New Page    ${SITE_BASE_URL}/accounts/login/
    Fill Text    //*[@id="id_username"]    ${VALID_USER}
    Fill Text    //*[@id="id_password"]    ${VALID_PW}
    Click    //*[@id="login-button"]

SuiteTeardown
    Go To    ${SITE_BASE_URL}/accounts/logout/
    Close Browser