from db.init import CONN, CURSOR
from db.user import User

class Password:
    
    all = {}
    
    def __init__(self, title, username, password="", user_id=None, id=None):
        self.title = title
        self.username = username
        self.password = password
        self.user_id = user_id
        self.id = id
        
    def __repr__(self):
        return f'<Pass {self.id} {self.title}: {self.username}>'
    
    @classmethod
    def create_table(cls):
        """Creates a users table in database if it doesn't exist"""
        sql = """
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY,
                title TEXT,
                username TEXT,
                password TEXT,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def drop_table(self):
        """Drops users table from database if it exists"""
        sql = """
        DROP TABLE IF EXISTS users
        """
        CURSOR.execute(sql)
        CONN.commit()
        
    def save(self):
        """Inserts a new row with the attributes values of the current class instance. Updates instance id with primary key value of new row"""
        
        sql = """
            INSERT INTO passwords (title, username, password, user_id)
            VALUES ( ? , ? , ? , ? )
        """
        
        CURSOR.execute(sql, (self.title, self.username, self.password, self.user_id)) # executes SQL and inputs username and password as values for a new row in the passwords table in the database
        CONN.commit() #commits the changes to the DB
        
        self.id = CURSOR.lastrowid # Retrieves the primary key id of last row and saves it to instance id attribute.
        type(self).all[self.id] = self # creates a dictionary entry in Password class variable all
        
    @classmethod
    def create(cls, new_title, new_username, new_password, user_id):
        """Create new instance of user and save to users table in DB"""
        new_password = cls(new_title, new_username, new_password, user_id) # uses cls constructor to create a new instance
        new_password.save() # saves new instance into DB in users table
        return new_password
    
    def update(self):
        """Update the table row corresponding to the current Password instance"""
        sql = """
            UPDATE passwords
            SET title = ?, username = ?, password = ?, user_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.title, self.username, self.password, self.user_id, self.id)) # runs the sql, updates the table row using values from current Password class object instance
        CONN.commit()
        
    @classmethod
    def instance_in_db(cls, row):
        """Return a class object having the attribute values from the table row"""
        password = cls.all.get(row[0])
        if password: # if password exists, update values
            password.title = row[1]
            password.username = row[2]
            password.password = row[3]
            password.user_id = row[4]
        else: # if user does not exist in class variable all, then create a new instance
            password = cls(row[1], row[2]) 
            password.id = row[0]
            cls.all[password.id] = password
        return password
    
    @classmethod
    def get_all(cls):
        """Returns a list containing a password object per row in the table"""
        sql = """
            SELECT * FROM passwords
        """
        rows = CURSOR.execute(sql).fetchall() # fetch everything in the table and make objects out of this class
        return [cls.instance_in_db(row) for row in rows]
    
    @classmethod
    def get_all_by_id(cls, id):
        """Returns a list containing a password object per row in the passwords table where it matches id value"""
        sql = """
            SELECT * FROM passwords
            WHERE user_id = ?
        """
        rows = CURSOR.execute(sql, (id,)).fetchall()
        return [cls.instance_in_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        """Return a password object instance corresponding to the table row matching the specified primary key value"""
        sql = """
            SELECT * FROM passwords WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_in_db(row) if row else None # check if instance exists in Password class variable all through the instance-in-DB class method
    
    @classmethod
    def find_by_title(cls, title):
        """Return a password object instance corresponding to the table row matching the specified title"""
        sql = """
            SELECT * FROM passwords
            WHERE title = ?
        """
        row = CURSOR.execute(sql, (title,)).fetchone()
        return cls.instance_in_db(row) if row else None
    
    @classmethod
    def find_by_username(cls, username):
        """Return a password object instance corresponding to the table row matching the specified username"""
        sql = """
            SELECT * FROM passwords
            WHERE username = ?
        """
        row = CURSOR.execute(sql, (username,)).fetchone()
        return cls.instance_in_db(row) if row else None
    
    @classmethod
    def find_by_user_id(cls, user_id):
        """Return a password object instance corresponding to the table row matching the specified user_id foreign key value"""
        sql = """
            SELECT * FROM passwords
            WHERE user_id = ?
        """
        rows = CURSOR.execute(sql, (user_id, )).fetchall()
        return [cls.instance_in_db(row) for row in rows]