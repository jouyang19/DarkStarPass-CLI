
user_id = None

user_instance = None

user_passwords = None

def main():

    print("""
    ===============================================
    **************** Dark Star Pass ***************

    [1] Log In
    [2] Sign Up
    [3] Quit

    """)

    done = False

    while not done:
        
        choice = input("    Select an option: ")
        if choice == "1":
            log_in()
            return main()
        elif choice == "2":
            sign_up()
        elif choice == "3":
            exit()
        else:
            print('Please try again.')

if __name__ == "__main__":
    from db.user import User
    from db.password import Password
    from helpers import (
    delete_entry,
    sign_up,
    log_in,
    view_vault,
    view_entry,
    edit_entry,
    user_dashboard,
    add_password,
    search_query,
    search_view
    )
    Password.create_table()
    User.create_table()
    main()
    