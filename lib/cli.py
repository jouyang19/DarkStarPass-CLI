
user_id = None

user_instance = None

user_passwords = None

user_pass = None


""" PROGRAM STARTS """

def sign_up():
    new_username = input("    Username: ")
    new_password = input("    Password: ")
    password = hashlib.sha256(new_password.encode()).hexdigest()
    user = User.create(new_username, password)
    global user_id
    user_id = user.id
    return main()

def log_in():
    username = input("    Username: ")
    password = input("    Password: ")
    global user_pass
    user_pass = password
    user = User.find_by_name(username)
    h_password = hashlib.sha256(password.encode()).hexdigest()
    if user:
        if h_password == user.password:
            global user_id
            user_id = user.id
            global user_instance
            user_instance = User.find_by_id(user.id)
            global user_passwords
            user_passwords = user_instance.passwords()
            return user_dashboard()
    else:
        print("    Wrong username or password")
        return main()
    
""" MAIN MENU """

def user_dashboard():
    print("""
    ===============================================
    ****************** Dashboard ******************

    [1] Password Vault
    [2] Add Password
    [3] Search
    [4] Log Out

    """)
    choice = input("    Select an option: ")
    if choice == "1":
        view_vault()
    elif choice == "2":
        add_password()
    elif choice == "3":
        search_query()
    elif choice == "4":
        user_id = None
        return main()
    else:
        return user_dashboard()

""" DASHBOARD OPTIONS """

def view_vault():
    print('''
    ================================================
    **************** Password Vault ****************
    Accounts:''')
    for item in Password.find_all_by_user_id(user_id):
        print(f"    {item}")
    print("""
    Options:
    [1] View Acccount
    [2] Edit Account
    [3] Delete Account
    [4] Go Back
    
    """)
    
    def select():
        choice = input("    Select an option: ")
        if choice == "1":
            def again():
                entry_id = input("    Enter Account #: ")
                if entry_id.isdigit():
                    view_entry(entry_id)
                elif entry_id.isdigit() is False:
                    print("    Please try again.")
                    again()
                else:
                    print("    Account does not exist")
                    return view_vault()
            again()
        elif choice == "2":
            entry_id = input("    Enter Account #: ")
            return edit_entry(entry_id)
        elif choice == "3":
            return delete_entry()
        elif choice == "4": 
            return user_dashboard()
        else:
            return view_vault()
        
    select()

def add_password():
    Password.create_table()
    title = input("    Account Title: ")
    username = input("    Account Username: ")
    password = input("    Account Password: ")
    e_password = password_encrypt(password.encode(), user_pass)
    global user_id
    account = Password.create(title, username, e_password, user_id)
    return user_dashboard()

def search_query():
    print('''
    ================================================
    ******************** Search ********************
    ''')
    search_a = input("    Type account name: ")
    result = []
    user_passwords = user_instance.passwords()
    for item in user_passwords:
        result.append(str(item))
    matches = difflib.get_close_matches(search_a, result, n=3, cutoff=0.3)
    for item in matches:
        print(f"    {item}")
    search_view()

def search_view():
    print("""
    Options:
    [1] View Account
    [2] Edit Account
    [3] Delete Account
    [4] Go Back
    
    """)
    
    def select():
        choice = input("    Select an option: ")
        if choice == "1":
            def again():
                entry_id = input("    Enter Account #: ")
                if entry_id.isdigit():
                    view_entry(entry_id)
                elif entry_id.isdigit() is False:
                    print("    Please try again.")
                    again()
                else:
                    print("    Account does not exist")
                    return view_vault()
            again()
        elif choice == "2":
            entry_id = input("    Enter Account #: ")
            return edit_entry(entry_id)
        elif choice == "3":
            return delete_entry()
        elif choice == "4": 
            return user_dashboard()
        else:
            return view_vault()
        
    select()

""" ENTRY OPTIONS """  

def view_entry(entry_id):
    
    entry = Password.find_by_id(entry_id)
    
    d_password = password_decrypt(entry.password, user_pass).decode()
    
    if entry and entry.user_id == user_id:
        print(f''' 
    ===============================================   
    *************** Account Details ***************
    
    {entry.title}
    
    Username: {entry.username}
    Password: {d_password}
    
    [1] Edit    
    [2] Back                             [3] Delete
    ''')
        choice = input("    select an option: ")
        if choice == "1":
            edit_entry(entry.id)
        elif choice == "2":
            return view_vault()
        elif choice == "3":
            delete_entry()
        elif choice == "4": 
            return user_dashboard()

        else:
            return view_entry(entry.id)
    else:
        print("    Account does not exist")
        return view_vault()
    
def edit_entry(entry_id): 
    
    entry = Password.find_by_id(entry_id)
    
    d_password = password_decrypt(entry.password, user_pass).decode()
    
    print(entry, entry.id, entry_id) 
    
    if entry and entry.user_id == user_id:
        print(f'''
    ===============================================
    *************** Account Details ***************
        
    {entry.title}
        
    Username: {entry.username}
    Password: {d_password}
        
    Which field would you like to edit:
        
    (1) Title? or (2) Username? or (3) Password?
                                            
    (4) Back                       (5) Delete entry                        
    ===============================================
    ''')
        choice = input("    select an option: ")
        if choice == "1":
            new_title = input("    Enter new title: ")
            entry.title = new_title
            entry.update()
            print("    Title updated successfully!")
            return edit_entry(entry.id)
        elif choice == "2":
            new_username = input("    Enter new username: ")
            entry.username = new_username
            entry.update()
            print("    Username updated successfully!")
            return edit_entry(entry.id)
        elif choice == "3":
            new_password = input("    Enter new password: ")
            e_new_password = password_encrypt(new_password.encode(), user_pass)
            entry.password = e_new_password
            entry.update()
            print("    Password updated successfully!")
            return edit_entry(entry.id)
        elif choice == "4":
            return view_entry(entry.id)
        elif choice == "5":
            delete_entry(entry.id)
            return view_vault()
        else:
            return edit_entry(entry.id)
    else: 
        print("    Account does not exist")
        return view_vault()

def delete_entry(entry_id=None):
    if entry_id is None:
        delete_id = input("    Type account # to delete: ")
        entry = Password.find_by_id(delete_id)
        entry.delete_row()
        view_vault()
    elif entry_id:
        entry = Password.find_by_id(entry_id)
        entry.delete_row()
    else:
        return view_vault()

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
    import difflib
    import hashlib
    from db.encryption import password_decrypt, password_encrypt
    from db.user import User
    from db.password import Password
    Password.create_table()
    User.create_table()
    main()
    