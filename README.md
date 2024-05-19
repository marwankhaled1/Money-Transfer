# Money_Transfer

## Introduction :-

a small web app using Django that handles fund transfers between two accounts, the app should support importing a list of accounts with opening balances, querying these accounts, and transferring funds between any two accounts.

## Functional Requirements :-

The web app needs to provide the following functional requirements

• Import accounts from CSV files or other formats

• List all accounts.

• Get account information.

• Transfer funds between two accounts.  

# How to use 
1. Create a virtual env and activate it 
2. install packages in the requirements.txt 
```cmd
pip install -r requirements.txt
```
3. if you want a new db delete current and remove migrations folders then make migrations and migrate
4. run the project using this command
```cmd 
python3 manage.py runserver 
```
5. the main page is localhost/accounts
