from db.user import User
from db.password import Password

def main():

    print("Dark Star Pass Online")

    print("""
    (1) Log In
    (2) Sign Up
    """)

    done = False

    while not done:
        
        choice = input("select an option:")
        if choice == "2":
            new_username = input("Username: ")
            new_password = input("Password: ")
            new_user = User(new_username, new_password)
            new_user.save()
            


        



if __name__ == "__main__":
    main()