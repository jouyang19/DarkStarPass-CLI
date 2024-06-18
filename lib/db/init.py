# lib/.__init__.py
import sqlite3

CONN = sqlite3.connect('dark_star_vault.db')
CURSOR = CONN.cursor()
