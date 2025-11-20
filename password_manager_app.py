import os
import base64
import random
import string


def load_passwords():
    storage = {}
    if os.path.exists("app_passwords.txt"):
        with open("app_passwords.txt", "r") as f:
            for line in f:
                if ":" in line:
                    account, encoded_pw = line.strip().split(":")
                    storage[account] = encoded_pw
    return storage


def save_passwords(storage):
    with open("app_passwords.txt", "w") as f:
        for account, encoded_pw in storage.items():
            f.write(account + ":" + encoded_pw + "\n")


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

    if len(pw) >= 8:
        result["length_ok"] = True
        score += 20

    if any(char.isupper() for char in pw):
        result["has_upper"] = True
        score += 20

    if any(char.islower() for char in pw):
        result["has_lower"] = True
        score += 20

    if any(char.isdigit() for char in pw):
        result["has_digit"] = True
        score += 20

    symbols = "!@#$%^&*()-_=+[]{};:,.<>/"
    if any(char in symbols for char in pw):
        result["has_symbol"] = True
        score += 20

    if score >= 80:
        result["strength"] = "Strong"
    elif score >= 50:
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


def add_password(storage):
    account = input("Account's name:").title()
    password = input('Password:')


    evaluation = evaluate_password(password)
    print(f"Password strength: {evaluation['strength']}")

    encoded_password = base64.b64encode(password.encode()).decode()
    storage[account] = encoded_password
    print("Password added successfully.")


def update_password(storage):

    for i,a in enumerate(storage.keys(), start=1):
        print(f'{i}: {a}')
        
    account = input("Enter the account to update: ")

    if account not in storage:
        print("Account not found.")
        return

    new_pw = input("Enter the new password: ")
    evaluation = evaluate_password(new_pw)

    if evaluation["strength"] == "Weak":
        print("Password too weak — update denied.")
        return

    encoded = base64.b64encode(new_pw.encode()).decode()
    storage[account] = encoded
    print("Password updated successfully.")


def delete_password(storage):
    
    for i,a in enumerate(storage.keys(), start=1):
        print(f'{i}: {a}')
    
    account = input("Enter the account to delete: ")

    if account.title() not in storage:
        print("Account not found.")
        return

    del storage[account.title()]
    print("Password deleted.")


def view_passwords(storage):
    
    if not storage:
        return "No passwords stored."

    filtered_storage = storage
    sorted_accounts = sorted(filtered_storage.items(), key=lambda x: x[0])

    result = ""
    result += f"Total passwords: {len(sorted_accounts)}\n"
    result += "=========================\n"
    
    query = input('Searching for a specific account? Yes or No /n')
    
    if query.lower() == 'yes':
        
        search = input('What account are you looking for: /n')
        
        filtered_storage = {
            acc: pw for acc, pw in storage.items() if search.lower() in acc.lower()
        }
        
        sorted_accounts = sorted(filtered_storage.items(), key=lambda x: x[0])
        
        if not filtered_storage:
            return f"No results found for '{search}'."

    show_passwords = input('Show passwords? Yes/No')
    
    if show_passwords.lower() == 'yes':
        result += "Stored Passwords:\n"
        for i, (acc, pw) in enumerate(sorted_accounts, start=1):
            password_display = base64.b64decode(pw.encode()).decode()
            result += f"{i}) {acc} : {password_display}\n"
        return result
                
    else:
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

