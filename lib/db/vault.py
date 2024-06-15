import sqlite3
import getpass

conn = sqlite3.connect("password_manager.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    account_name TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')
conn.commit()

def sign_up():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                   (username, password))
    conn.commit()
    print("Sign up successful!")

def login():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                   (username, password))
    user = cursor.fetchone()

    if user:
        print("Login successful!")
        return True
    else:
        print("Invalid username or password")
        return False
    
def main():
    while True:
        choice = input("Do you want to (1) Login or (2) Sign Up? (Enter 1 or 2): ")

        if choice == '1':
            if login():
                break
        elif choice == '2':
            sign_up()
        else:
            print("Invalid choice. Please enter 1 or 2.")

    while True:
        print("\nOptions: (1) View Accounts, (2) Add Account, (3) Update Account, (4) Quit")
        option = input("Choose an option: ")

        if option == '1':
            view_accounts()
        elif option == '2':
            add_account()
        elif option == '3':
            update_account()
        elif option == '4':
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()

