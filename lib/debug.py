#!/usr/bin/env python3
# lib/debug.py

from db.init import CONN, CURSOR
from db.user import User
from db.password import Password
from db.seed import seed_database
import ipdb

def reset_database():
    User.drop_table()
    Password.drop_table()
    User.create_table()
    Password.create_table()
    seed_database()
    
if __name__ == "__main__":
    reset_database()

ipdb.set_trace()
