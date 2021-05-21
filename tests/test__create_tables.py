import os
from twitteralchemy import create_tables

connection_string = os.environ['DB_CONNECTION_STRING']

create_tables(connection_string)
