"""Create database object, connect and do on-start actions"""
from database.methods import Database


database = Database()
database.connect()
database.create_link_table()
