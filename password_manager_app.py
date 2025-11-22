import os
import base64
import random
import string


#This function loads stored passwords from a file.
def load_passwords():
    storage = {}
    if os.path.exists("app_passwords.txt"):
        with open("app_passwords.txt", "r") as f:
            #Read each line and split the account and encoded password.
            for line in f:
                if ":" in line:
                    account, encoded_pw = line.strip().split(":")
                    storage[account] = encoded_pw
    return storage


#This function saves passwords to the file.
def save_passwords(storage):
    with open("app_passwords.txt", "w") as f:
        #Write each account and encoded password to the file.
        for account, encoded_pw in storage.items():
            f.write(account + ":" + encoded_pw + "\n")


#This function evaluates the strength of the given password.
def evaluate_password(pw):
    score = 0
    result = {
        "length_ok": False,
        "has_upper": False,
        "has_lower": False,
        "has_digit": False,
        "has_symbol": False,
        "strength": "Weak"
    }

    #Check if the password is at least 8 characters long.
    if len(pw) >= 8:
        result["length_ok"] = True
        score += 20

    #Check for the presence of an uppercase letter in the password.
    if any(char.isupper() for char in pw):
        result["has_upper"] = True
        score += 20

    #Check for the presence of a lowercase letter in the password.
    if any(char.islower() for char in pw):
        result["has_lower"] = True
        score += 20

    #Check for the presence of a digit in the password.
    if any(char.isdigit() for char in pw):
        result["has_digit"] = True
        score += 20

    #Check for the presence of a special symbol in the password.
    symbols = "!@#$%^&*()-_=+[]{};:,.<>/"
    if any(char in symbols for char in pw):
        result["has_symbol"] = True
        score += 20

    #Determine the password strength based on the total score.
    if score == 100:
        result["strength"] = "Strong"
    elif 80>= score >= 50:
        result["strength"] = "Medium"
    else:
        result["strength"] = "Weak"

    return result

def password_generator(length, preference):
    all_char = [string.ascii_lowercase]
    if preference[0] == 'yes':
        all_char.append(string.ascii_uppercase)
    if preference[1] == 'yes':
        all_char.append(string.digits)
    if preference[2] == 'yes':
        all_char.append(string.punctuation)

    password = ""
    while len(password) < length:
        password += random.choice(random.choice(all_char))

    eval_results = evaluate_password(password)
    eval = eval_results["strength"]

    return password, eval

""" Login() function to validate the master password entered by a user,
    and allow the user to create a new one if a master password doesn't exist.
    A user has three attempts to enter a correct master password. """
def login():
    master_password = None
    
    if not os.path.exists('master_password.txt'):
        password = input('Create a master password: ')

        evaluation = evaluate_password(password)
        print(f"Password strength: {evaluation['strength']}")

        encoded_password = base64.b64encode(password.encode()).decode()
        with open('master_password.txt', mode='w') as f:
            f.write(encoded_password)
        master_password = encoded_password
        print('Succuessfully Created a Master Password.')
        return True
    else:
        with open('master_password.txt', mode='r') as r:
            master_password = r.read()

    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        user_password = input('Enter Password: ')
        encoded_user_password = base64.b64encode(user_password.encode()).decode()

        if master_password == encoded_user_password:
            return True
        else:
            print('Wrong Password. Try Again!')
            attempts += 1
            continue
    else:
        return False

# Allow the user to a manually add a new account to the list. 
# Password gets encoded using Base64 
def add_password(storage):
    account = input("Account's name:").title()
    password = input('Password:')


    evaluation = evaluate_password(password)
    print(f"Password strength: {evaluation['strength']}")

    encoded_password = base64.b64encode(password.encode()).decode()
    storage[account] = encoded_password
    print("Password added successfully.")


#This function updates the password for a specified account.
def update_password(storage):

    for i,a in enumerate(storage.keys(), start=1):
        print(f'{i}: {a}')

    account = input("Enter the account to update: ").title()

    if account not in storage:
        print("Account not found.")
        return

    new_pw = input("Enter the new password: ")
    evaluation = evaluate_password(new_pw)
    print(f"Password strength: {evaluation['strength']}")

    #Check if the new password is strong enough.
    if evaluation["strength"] == "Weak":
        print("Password too weak — update denied.")
        return

    #Encode the new password and update the storage.
    encoded = base64.b64encode(new_pw.encode()).decode()
    storage[account] = encoded
    print("Password updated successfully.")


#This function deletes a specified account's password.
def delete_password(storage):

    for i,a in enumerate(storage.keys(), start=1):
        print(f'{i}: {a}')

    account = input("Enter the account to delete: ")

    if account.title() not in storage:
        print("Account not found.")
        return

    #Remove the account from storage.
    del storage[account.title()]
    print("Password deleted.")

def view_passwords(storage):
    """
    This function displays stored account passwords from the 'storage' dictionary.
    
    Features:
    - Shows the total number of saved passwords.
    - Allows optional searching for a specific account name.
    - Provides the option to show passwords decoded from Base64 OR show only account names.
    
    Parameters:
    storage (dict): A dictionary where keys are account names and values are Base64-encoded passwords.
    
    Returns:
    str: A formatted string containing either a list of accounts or accounts with their decoded passwords.
    """

    # If storage is empty, return a simple message
    if not storage:
        return "No passwords stored."

    # Default: use all accounts before filtering
    filtered_storage = storage

    # Sort accounts alphabetically (A → Z)
    sorted_accounts = sorted(filtered_storage.items(), key=lambda x: x[0])

    result = ""
    result += f"Total passwords: {len(sorted_accounts)}\n"
    result += "=========================\n"

    # Ask user if they want to search for a specific account
    query = input('Searching for a specific account? Yes or No\n')

    if query.lower() == 'yes':

        # The account name (or part of it) to search for
        search = input('What account are you looking for:\n')

        # Filter only accounts that contain the search term (case-insensitive)
        filtered_storage = {
            acc: pw for acc, pw in storage.items() if search.lower() in acc.lower()
        }

        # Sort the filtered accounts alphabetically
        sorted_accounts = sorted(filtered_storage.items(), key=lambda x: x[0])

        # If search found nothing
        if not filtered_storage:
            return f"No results found for '{search}'."

    # Ask user if they want to show real passwords
    show_passwords = input('Show passwords? Yes/No\n')

    if show_passwords.lower() == 'yes':
        result += "Stored Passwords:\n"
        for i, (acc, pw) in enumerate(sorted_accounts, start=1):

            # Decode Base64-encoded password before showing it
            password_display = base64.b64decode(pw.encode()).decode()

            result += f"{i}) {acc} : {password_display}\n"
        return result

    else:
        # If not showing passwords → show only account names
        result += "Accounts List:\n"
        for i, (acc, _) in enumerate(sorted_accounts, start=1):
            result += f"{i}) {acc}\n"
        return result



def menu(storage):
    while True:
        print("\n=========== PASSWORD MANAGER ==========")
        print("1. Add password")
        print("2. Update password")
        print("3. Delete password")
        print("4. Generate password")
        print("5. Show saved accounts")
        print("6. Exit")
        print("=======================================")

        choice = input("Choose an option: ")

        if choice == "1":
            add_password(storage)

        elif choice == "2":
            update_password(storage)

        elif choice == "3":
            delete_password(storage)

        elif choice == "4":
            length = int(input("Enter password length: "))
            upper = input("Include uppercase? (yes/no): ").lower()
            nums = input("Include numbers? (yes/no): ").lower()
            symbols = input("Include symbols? (yes/no): ").lower()

            pw, strength = password_generator(length, [upper, nums, symbols])
            print(f"Generated password: {pw} (Strength: {strength})")

        elif choice == "5":
            print(view_passwords(storage))

        elif choice == "6":
            save_passwords(storage)
            print("Saved. Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":

    if login():
        storage = load_passwords()
        menu(storage)
    else:
        print("Access denied.")
