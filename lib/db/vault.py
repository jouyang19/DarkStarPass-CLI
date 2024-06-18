import sqlite3
import getpass
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Connect to the SQLite database
conn = sqlite3.connect('password_manager.db')
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    account_name TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')
conn.commit()

TERMINAL_WIDTH = 80

def center_text(text):
    if len(text) >= TERMINAL_WIDTH:
        return text
    padding = (TERMINAL_WIDTH - len(text)) // 2
    return ' ' * padding + text

def print_centered_border(message):
    border = '+' + '-' * (len(message) + 2) + '+'
    print(Fore.YELLOW + center_text(border))
    print(Fore.YELLOW + center_text(f"| {message} |"))
    print(Fore.YELLOW + center_text(border))

def sign_up():
    print_centered_border("Sign Up")
    account_name = input(center_text("Enter your account name: "))
    username = input(center_text("Enter your username: "))
    password = getpass.getpass(center_text("Enter your password: "))

    cursor.execute("INSERT INTO users (account_name, username, password) VALUES (?, ?, ?)", 
                   (account_name, username, password))
    conn.commit()
    print(Fore.GREEN + center_text("Sign up successful!"))

def login():
    print_centered_border("Login")
    username = input(center_text("Enter your username: "))
    password = getpass.getpass(center_text("Enter your password: "))

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                   (username, password))
    user = cursor.fetchone()

    if user:
        print(Fore.GREEN + center_text("Login successful!"))
        return True
    else:
        print(Fore.RED + center_text("Invalid username or password"))
        return False

def view_accounts():
    cursor.execute("SELECT * FROM users")
    accounts = cursor.fetchall()
    print_centered_border("Stored Accounts")
    for account in accounts:
        print(center_text(f"{Fore.YELLOW}Account Name: {account[0]}, Username: {account[1]}, Password: {account[2]}"))

def add_account():
    print_centered_border("Add Account")
    account_name = input(center_text("Enter new account name: "))
    username = input(center_text("Enter new username: "))
    password = getpass.getpass(center_text("Enter new password: "))

    cursor.execute("INSERT INTO users (account_name, username, password) VALUES (?, ?, ?)", 
                   (account_name, username, password))
    conn.commit()
    print(Fore.GREEN + center_text("Account added successfully!"))

def update_account():
    print_centered_border("Update Account")
    account_name = input(center_text("Enter the account name to update: "))
    new_username = input(center_text("Enter new username: "))
    new_password = getpass.getpass(center_text("Enter new password: "))

    cursor.execute("UPDATE users SET username = ?, password = ? WHERE account_name = ?", 
                   (new_username, new_password, account_name))
    conn.commit()
    print(Fore.GREEN + center_text("Account updated successfully!"))

def delete_account():
    print_centered_border("Delete Account")
    account_name = input(center_text("Enter the account name to delete: "))

    cursor.execute("DELETE FROM users WHERE account_name = ?", (account_name,))
    conn.commit()

    if cursor.rowcount > 0:
        print(Fore.GREEN + center_text("Account deleted successfully!"))
    else:
        print(Fore.RED + center_text("Account not found."))

def main():
    while True:
        print(Fore.CYAN + center_text("\nDo you want to (1) Login or (2) Sign Up? (Enter 1 or 2): "), end='')
        choice = input()

        if choice == '1':
            if login():
                break
        elif choice == '2':
            sign_up()
        else:
            print(Fore.RED + center_text("Invalid choice. Please enter 1 or 2."))

    while True:
        print_centered_border("Options")
        print(Fore.CYAN + center_text("(1) View Accounts"))
        print(Fore.CYAN + center_text("(2) Add Account"))
        print(Fore.CYAN + center_text("(3) Update Account"))
        print(Fore.CYAN + center_text("(4) Delete Account"))
        print(Fore.CYAN + center_text("(5) Quit"))
        option = input(center_text("Choose an option: "))

        if option == '1':
            view_accounts()
        elif option == '2':
            add_account()
        elif option == '3':
            update_account()
        elif option == '4':
            delete_account()
        elif option == '5':
            break
        else:
            print(Fore.RED + center_text("Invalid option. Please choose again."))

if __name__ == "__main__":
    main()
