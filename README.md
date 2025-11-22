
# Passwords Manager App

# Description
A regular tech user nowadays has more than ten accounts on average. A good security practice states that each account should have a unique password. This has made memorizing passwords an impossible mission and raised an extensive demand for trustworthy password management tools. In this project, we aim to provide a repository of passwords where users can locally store, generate, view, and manage passwords of different accounts. 

# Features
1. Adding a new account/password. 
2. Encoding all stored passwords using Base64
3. Evaluating each passwords stored in the repository. 
4. Viewing the list of stored accounts, with the option of viewing their decoded passwords. 
5. Generating a new password that adheres to user’s preferences. 
6. Update/Delete stored accounts. 
7. Authenticating user logins using master password.

# Libraries & Data Types
1. OS library to interact with the system and check the existence of certain files. 
2. Base64 library to encode/decode passwords 
3. Random library to generate random passwords
4. String library to import characters of different types
Accounts & Passwords are grouped together using dictionary data type. 

# Functions
1. Login. 
2. Load passwords.
3. Add account.
4. Password generator.
5. Evaluate passwords. 
6. Update Password Function 
7. Delete account function
8. View Accounts.
9. Save Changes.
10. Main function 

# Usage
The script will start by asking the user to enter a master password for logging in and compare it to the one stored on the system. If a master password file is not already stored on the user’s computer, the script will create a new file on the system and prompt the user to enter a new master password. Users will have three attempts to enter the correct password before shutting down the app. 

Once logged in, the script will use the loading function to initiate a new dictionary, where all accounts and passwords will be stored. The function will interact with the system to see if the password manager file exists. If yes, the load function will read the file and fill the new dictionary with its contents. 

After that, the user will have a menu of six choices (Add, View, Generate, Update, Delete, Exit&Save). 

Adding a function will allow users to enter a new account name and password. The password will then get encoded and saved to the dictionary of passwords. 

Viewing function will display all stored accounts’ names, along with the option of viewing their encoded passwords. 

Generate password function will take the user’s preferences as input and output a random password that adheres to the user’s preferences. 

Update function will allow the user to change the password of a stored account. 

Delete function will allow the user to permanently delete an account. 

Exit&Save function will rewrite the dictionary back to the password manager file, and exit the script. 

To run the streamlit app use:

pip install streamlit

streamlit run POC_streamlit_app.py




