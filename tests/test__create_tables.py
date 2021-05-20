import os
from twalchemy.twalchemy import create_tables

connection_string = os.environ['DB_CONNECTION_STRING']

create_tables(connection_string)
