from db.user import User
from db.password import Password

user_id = None

def sign_up():
    new_username = input("Username: ")
    new_password = input("Password: ")
    User.create_table()
    user = User.create(new_username, new_password)
    user_id = user.id
    return main()

def log_in():
    username = input("Username: ")
    password = input("Password: ")
    User.create_table()
    user = User.find_by_name(username)
    if user:
        if password == user.password:
            user_id = user.id
            return user_dashboard()
    else:
        print("Wrong username or password")
        return log_in()
    


def user_dashboard():
    print("""
    (1) Password Vault
    (2) Add Password
    (3) Search
    """)
    choice = input("select an option: ")
    if choice == "1":
        Password.create_table()
        print(Password.get_all())
    elif choice == "2":
        title = input("Title: ")
        username = input("Username: ")
        password = input("Password: ")
        account = Password.create(title, username, password, user_id)
        print(account)


def main():

    print("Dark Star Pass Online")

    print("""
    (1) Log In
    (2) Sign Up
    """)

    done = False

    while not done:
        
        choice = input("select an option: ")
        if choice == "2":
            sign_up()
        elif choice == "1":
            log_in()

if __name__ == "__main__":
    main()