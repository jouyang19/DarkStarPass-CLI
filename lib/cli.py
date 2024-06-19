from db.user import User
from db.password import Password

user_id = None

def sign_up():
    new_username = input("Username: ")
    new_password = input("Password: ")
    user = User.create(new_username, new_password)
    global user_id
    user_id = user.id
    return main()

def log_in():
    username = input("Username: ")
    password = input("Password: ")
    user = User.find_by_name(username)
    if user:
        if password == user.password:
            global user_id
            user_id = user.id
            return user_dashboard()
    else:
        print("Wrong username or password")
        return main()
    
    
    
def view_vault():
    for item in Password.find_all_by_user_id(user_id):
        print(item)
    print("""
    ===============================================
    ******************** Vault ********************
    (1) View Entry
    (2) Edit Entry
    (3) Delete Entry
    (4) Go Back
    ===============================================
    """)
    
    def select():
        choice = input("select an option: ")
        if choice == "1":
            def again():
                entry_id = input("Enter Account #: ")
                if entry_id.isdigit():
                    view_entry(entry_id)
                elif entry_id.isdigit() is False:
                    print("Please try again.")
                    again()
                else:
                    return view_vault()
            again()
        elif choice == "2":
            entry_id = input("Enter Account #: ")
            return edit_entry(entry_id)
        elif choice == "3":
            pass
        elif choice == "4": 
            return user_dashboard()
        else:
            return view_vault()
        
    select()
    
    
def view_entry(entry_id):
    
    entry = Password.find_by_id(entry_id)
    
    print(f'''
    ===============================================
    Account Entry # {entry.id}
    
    *************** Account Details ***************
    
    Title: {entry.title}
    
    Username: {entry.username}
    Password: {entry.password}
    
                                         (1) Edit    
    (2) Back                             (3) Delete
    ===============================================
    ''')
    
    choice = input("select an option: ")
    if choice == "1":
        edit_entry(entry.id)
    elif choice == "2":
        return view_vault()
    elif choice == "3":
        pass
    else:
        return view_entry(entry.id)
    
def edit_entry(entry_id): 
    
    entry = Password.find_by_id(entry_id)
    
    print(f'''
    ===============================================
    Account Entry # {entry.id}
    
    *************** Account Details ***************
    
    Title: {entry.title}
    
    Username: {entry.username}
    Password: {entry.password}
    
    Which field would you like to edit:
    
    (1) Title? or (2) Username? or (3) Password?
                                           
    (4) Back                       (5) Delete entry                        
    ===============================================
    ''')
    choice = input("select an option: ")
    if choice == "1":
        new_title = input("Enter new title: ")
        entry.title = new_title
        entry.update()
        print("Title updated successfully!")
        return edit_entry(entry.id)
    elif choice == "2":
        new_username = input("Enter new username: ")
        entry.username = new_username
        entry.update()
        print("Username updated successfully!")
        return edit_entry(entry.id)
    elif choice == "3":
        new_password = input("Enter new password: ")
        entry.password = new_password
        entry.update()
        print("Password updated successfully!")
        return edit_entry(entry.id)
    elif choice == "4":
        return view_entry(entry.id)
    elif choice == "5":
        pass
    else:
        return edit_entry(entry.id)

def user_dashboard():
    print("""
    ===============================================
    ****************** Dashboard ******************
    (1) Password Vault
    (2) Add Password
    (3) Search
    (4) Log Out
    ===============================================
    """)
    choice = input("select an option: ")
    if choice == "1":
        view_vault()
    elif choice == "2":
        Password.create_table()
        title = input("Account Title: ")
        username = input("Account Username: ")
        password = input("Account Password: ")
        account = Password.create(title, username, password, user_id)
        print(account)
        return user_dashboard()
    elif choice == "3":
        pass
    elif choice == "4":
        user_id = None
        return main()
    else:
        return user_dashboard()

def main():

    print("""
    ===============================================
    ********** Welcome to Dark Star Pass **********
    (1) Log In
    (2) Sign Up
    (3) Quit
    ===============================================
    """)

    done = False

    while not done:
        
        choice = input("select an option: ")
        if choice == "2":
            sign_up()
        elif choice == "1":
            log_in()
        elif choice == "3":
            exit()
        else:
            print('Please try again.')

if __name__ == "__main__":
    Password.create_table()
    User.create_table()
    main()
    