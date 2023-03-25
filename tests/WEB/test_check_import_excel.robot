*** Settings ***
Library    Browser
Variables  ../variables.py

Suite Setup        SuiteSetup
Suite Teardown     SuiteTeardown

*** Test Cases ***
Check upload excel will show data
    [Setup]    Go To    ${SITE_BASE_URL}/importXslxFromSchool/
    Upload File By Selector    //input[@id='excelInputField']    ${RESOURCE_PATH}/112年盤點計畫盤點表.xlsx
    Get Element Count    //*[@id="showExcel"]/div[1]/div[2]/table/tbody/tr    ==    550

*** Keywords ***
SuiteSetup
    New Browser    browser=chromium    headless=${TRUE}
    New Context    ignoreHTTPSErrors=${TRUE}    recordVideo=${RECORD_SETTING}
    New Page    ${SITE_BASE_URL}/accounts/login/
    Fill Text    //*[@id="id_username"]    ${VALID_USER}
    Fill Text    //*[@id="id_password"]    ${VALID_PW}
    Click    //*[@id="login-button"]
    Wait Until Network Is Idle

SuiteTeardown
    Close Browser