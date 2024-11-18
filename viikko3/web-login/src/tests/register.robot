*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Input Username  super
    Input Password  super123
    Input Password Confirmation   super123
    Submit Registration
    Registration Should Succeed
    

Register With Too Short Username And Valid Password
    Input Username  su
    Input Password  super123
    Input Password Confirmation   super123
    Submit Registration
    Registration Should Fail With Message	Username must be at least 3 characters long
    

Register With Valid Username And Too Short Password
    Input Username  super
    Input Password  super
    Input Password Confirmation   super
    Submit Registration
    Registration Should Fail With Message   Password must be at least 8 characters long
    

Register With Valid Username And Invalid Password
# salasana ei sisällä halutunlaisia merkkejä
    Input Username  super
    Input Password  supersuper
    Input Password Confirmation   supersuper
    Submit Registration
    Registration Should Fail With Message   Password must include at least one number or special character
    

Register With Nonmatching Password And Password Confirmation
    Input Username  super
    Input Password  super123
    Input Password Confirmation   super1234
    Submit Registration
    Registration Should Fail With Message   Passwords do not match
    

Register With Username That Is Already In Use
    Input Username  kalle
    Input Password  kalle123
    Input Password Confirmation   kalle123
    Submit Registration
    Registration Should Fail With Message   Username is already taken
    
Login After Successful Registration
    Input Username  super
    Input Password  super123
    Input Password Confirmation    super123
    Submit Registration
    Registration Should Succeed
    Go To Login Page
    Input Username  super
    Input Password  super123
    Submit Credentials
    Login Should Succeed

Login After Failed Registration
    Input Username  super
    Input Password  super123
    Input Password Confirmation    super1234
    Submit Registration
    Registration Should Fail With Message   Passwords do not match
    Go To Login Page
    Input Username  super
    Input Password  super123
    Submit Credentials
    Login Should Fail With Message   Invalid username or password
    

*** Keywords ***

Registration Should Succeed
    Page Should Contain   Welcome to Ohtu Application!

Submit Registration
    Click Button  Register
    
Submit Credentials
    Click Button  Login

Input Username
    [Arguments]    ${username}
    Input Text    id=username    ${username}

Input Password
    [Arguments]    ${password}
    Input Text    id=password    ${password}

Input Password confirmation
    [Arguments]    ${password_confirmation}
    Input Text    id=password_confirmation    ${password_confirmation}

Registration Should Fail With Message
    [Arguments]    ${message}
    Register Page Should Be Open
    Page Should Contain   ${message}

Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page

Go To Register Page
    Go To  ${REGISTER_URL}
    
Logout
    Click Link  Logout
    Login Page Should Be Open

Go To Login Page
    Go To  ${LOGIN_URL}

Login Should Succeed
    Main Page Should Be Open

Login Should Fail With Message
    [Arguments]    ${message}
    Login Page Should Be Open
    Page Should Contain   ${message}
