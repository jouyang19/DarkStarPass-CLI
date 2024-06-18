from db.init import CONN, CURSOR

class User:
    
    # Dictionary of objects saved to DB
    all = {}
    
    def __init__(self, username, password, id=None):
        self.username = username
        self.password = password
        self.id = id
        
    def __repr__(self) -> str:
        return f'<User {self.id}: {self.username}>'
    
    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, new_username):
        if type(new_username) is str and len(new_username):
            self._username = new_username
        else:
            raise ValueError('New username must be of string greater than 0 characters')
        
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, new_password):
        if type(new_password) is str and len(new_password):
            self._password = new_password
        else:
            raise ValueError('New password must be a string greater than 0 characters')
    
    @classmethod
    def create_table(cls):
        """Creates a users table in database if it doesn't exist"""
        sql = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT
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
            INSERT INTO users (username, password)
            VALUES ( ? , ? )
        """
        usernames = []
        for user in User.get_all():
            usernames.append(user.username)
        if self.username not in usernames:
            CURSOR.execute(sql, (self.username, self.password)) # executes SQL and inputs username and password as values for a new row in the users table in the vault database
            CONN.commit() #commits the changes to the DB
            self.id = CURSOR.lastrowid # Retrieves the primary key id of last row and saves it to instance id attribute.
            type(self).all[self.id] = self # creates a dictionary entry in User.all
        else:
            print('Account already exists. Please sign up.')
        
    @classmethod
    def create(cls, new_username, new_password):
        """Create new instance of user and save to users table in DB"""
        new_user = cls(new_username, new_password) # uses cls constructor to create a new instance
        new_user.save() # saves new instance into DB in users table
        return new_user
    
    def update(self):
        """Update the table row corresponding to the current User instance"""
        sql = """
            UPDATE users
            SET username = ?, password = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.username, self.password, self.id)) # runs the sql, updates the table row using values from current User instance
        CONN.commit()
        
    @classmethod
    def instance_in_db(cls, row):
        """Return a class object having the attribute values from the table row"""
        user = cls.all.get(row[0])
        if user: # if user exists, update values
            user.username = row[1]
            user.password = row[2]
        else: # if user does not exist in class variable all, then create a new instance
            user = cls(row[1], row[2]) 
            user.id = row[0]
            cls.all[user.id] = user
        return user
    
    @classmethod
    def get_all(cls):
        """Returns a list containing a user object per row in the table"""
        sql = """
            SELECT * FROM users
        """
        rows = CURSOR.execute(sql).fetchall() # fetch everything in the table and make objects out of this class
        return [cls.instance_in_db(row) for row in rows]
        
    @classmethod
    def find_by_id(cls, id):
        """Return a user object corresponding to the table row matching the specified primary key value"""
        sql = """
            SELECT * FROM users WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone() 
        return cls.instance_in_db(row) if row else None # check if instance exists in User Class variable All through the instance in DB method
    
    @classmethod
    def find_by_name(cls, name):
        """Return a user object corresponding to the table row matching the specified given name"""
        sql = """
        SELECT * FROM users WHERE username = ?
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_in_db(row) if row else None # check if instance exists in User Class variable All through the instance in DB method
    
    def delete(self):
        """Delete the table row corresponding to the current class instance"""
        sql = """
            DELETE FROM users
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id] # deletes instance record from User Class variable all
        self.id = None # sets the id as None
        
    def passwords(self):
        from db.password import Password
        sql = """
            SELECT * FROM passwords
            WHERE user_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Password.instance_in_db(row) for row in rows]
        