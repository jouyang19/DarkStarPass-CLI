from db.user import User
from db.password import Password
import difflib
from colorama import init, Fore, Back, Style
import os

init()
Password.create_table()
User.create_table()
user_id = None
user_instance = None
user_passwords = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

""" PROGRAM STARTS """

def sign_up():
    new_username = input(Fore.GREEN + "    Username: ")
    new_password = input(Fore.GREEN + "    Password: ")
    user = User.create(new_username, new_password)
    global user_id
    user_id = user.id
    return main()

def log_in():
    username = input(Fore.GREEN + "    Username: ")
    password = input(Fore.GREEN + "    Password: ")
    user = User.find_by_name(username)
    if user:
        if password == user.password:
            global user_id
            user_id = user.id
            global user_instance
            user_instance = User.find_by_id(user.id)
            global user_passwords
            user_passwords = user_instance.passwords()
            return user_dashboard()
    else:
        print(Fore.RED + "    Wrong username or password")
        return main()
    
""" MAIN MENU """

def user_dashboard():
    clear_screen()
    print(Style.BRIGHT + Fore.RESET + """
    ===============================================
    ****************** Dashboard ******************""")
    print(Style.NORMAL + """
    [1] Password Vault
    [2] Add Password
    [3] Search
    [4] Log Out
    """)
    choice = input(Fore.GREEN + "    Select an option: ")
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
    clear_screen()
    print(Style.BRIGHT + Fore.RESET + '''
    ===============================================
    **************** Password Vault ***************''')
    print(Style.NORMAL + """    ACCOUNTS:""")
    for item in Password.find_all_by_user_id(user_id):
        print(f"    {item}")
    print(Style.NORMAL + """
    OPTIONS:
    [1] View Acccount               [2] Edit Account
    [4] Back                        [3] Delete Account
    
    """)
    
    def select():
        choice = input(Fore.GREEN + "    Select an option: ")
        if choice == "1":
            def again():
                entry_id = input(Fore.GREEN + "    Enter Account #: ")
                if entry_id.isdigit():
                    view_entry(entry_id)
                elif entry_id.isdigit() is False:
                    print(Fore.RED + "    Please try again.")
                    again()
                else:
                    print(Fore.RED + "    Account does not exist")
                    return view_vault()
            again()
        elif choice == "2":
            entry_id = input(Fore.GREEN + "    Enter Account #: ")
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
    title = input(Fore.GREEN + "    Account Title: ")
    username = input(Fore.GREEN + "    Account Username: ")
    password = input(Fore.GREEN + "    Account Password: ")
    global user_id
    account = Password.create(title, username, password, user_id)
    return user_dashboard()

def search_query():
    clear_screen()
    print(Style.BRIGHT + Fore.RESET + '''
    ===============================================
    ******************** Search *******************''')
    search_a = input(Fore.GREEN + Style.RESET_ALL + "    Type account name: ")
    result = []
    user_passwords = user_instance.passwords()
    for item in user_passwords:
        result.append(str(item))
    matches = difflib.get_close_matches(search_a, result, n=3, cutoff=0.3)
    for item in matches:
        print(f"    {item}")
    search_view()

def search_view():
    print(Fore.RESET + Style.RESET_ALL + """
    OPTIONS:
    [1] View Acccount
    [2] Edit Account
    [3] Delete Account
    [4] Back
    """)
    
    def select():
        choice = input(Fore.GREEN + "    Select an option: ")
        if choice == "1":
            def again():
                entry_id = input(Fore.GREEN + "    Enter Account #: ")
                if entry_id.isdigit():
                    view_entry(entry_id)
                elif entry_id.isdigit() is False:
                    print(Fore.RED + "    Please try again.")
                    again()
                else:
                    print(Fore.RED + "    Account does not exist")
                    return view_vault()
            again()
        elif choice == "2":
            entry_id = input(Fore.GREEN + "    Enter Account #: ")
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
    clear_screen()
    entry = Password.find_by_id(entry_id)
    
    if entry and entry.user_id == user_id:
        print(Style.BRIGHT + Fore.RESET + """      
    ===============================================   
    *************** Account Details ***************""")
        print(Style.NORMAL + f'''
    {entry.title}
    
    Username: {entry.username}
    Password: {entry.password}
    
    [1] Edit    
    [2] Back                             [3] Delete
    ''')
        choice = input(Fore.GREEN + "    select an option: ")
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
        print(Fore.RED + "    Account does not exist")
        return view_vault()
    
def edit_entry(entry_id): 
    clear_screen()
    entry = Password.find_by_id(entry_id)
    
    if entry and entry.user_id == user_id:
        print(Style.BRIGHT + Fore.RESET + """ 
    ===============================================
    ******************** Editor *******************""")
        print(Style.NORMAL + f'''    
    {entry.title}
        
    Username: {entry.username}
    Password: {entry.password}
        
    Which field would you like to edit: 
    [1] Title
    [2] Username
    [3] Password
                                            
    [4] Back                       [5] Delete
    ''')
        choice = input(Fore.GREEN + "    select an option: ")
        if choice == "1":
            new_title = input(Fore.GREEN + "    Enter new title: ")
            entry.title = new_title
            entry.update()
            print(Fore.GREEN + "    Title updated successfully!")
            return edit_entry(entry.id)
        elif choice == "2":
            new_username = input(Fore.GREEN + "    Enter new username: ")
            entry.username = new_username
            entry.update()
            print(Fore.GREEN + "    Username updated successfully!")
            return edit_entry(entry.id)
        elif choice == "3":
            new_password = input(Fore.GREEN + "    Enter new password: ")
            entry.password = new_password
            entry.update()
            print(Fore.GREEN + "Password updated successfully!")
            return edit_entry(entry.id)
        elif choice == "4":
            return view_vault()
        elif choice == "5":
            delete_entry(entry.id)
            return view_vault()
        else:
            return edit_entry(entry.id)
    else: 
        print(Fore.RED + "    Account does not exist")
        return view_vault()

def delete_entry(entry_id=None):
    if entry_id is None:
        delete_id = input(Fore.GREEN + Style.RESET_ALL + "    Select Account # to delete: ")
        entry = Password.find_by_id(delete_id)
        entry.delete_row()
        view_vault()
    elif entry_id:
        entry = Password.find_by_id(entry_id)
        entry.delete_row()
    else:
        return view_vault()

""" Main """

def main():
    clear_screen()
    print(Style.BRIGHT + Fore.RESET + """
    ===============================================
    **************** Dark Star Pass ***************""")
    print(Style.NORMAL + """
    [1] Log In
    [2] Sign Up
    [3] Quit

    Type a number to continue.
     """)

    done = False

    while not done:
        
        choice = input(Fore.GREEN + "    Select an option: ")
        if choice == "1":
            log_in()
            return main()
        elif choice == "2":
            sign_up()
        elif choice == "3":
            exit()
        else:
            print(Fore.RED + '    Please try again.')

if __name__ == "__main__":
    main()
    