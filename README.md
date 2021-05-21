# Twitter Alchemy!

This humble package provides Sqlalchemy models for your twitter database.

To create models for your database, first set the DB_CONNECTION_STRING environment variable for your
database connection string. For example, for an in-memory sqlite database
```shell
# linux:
export DB_CONNECTION_STRING='sqlite:///:memory:'

# windows: 
setx DB_CONNECTION_STRING 'sqlite:///:memory:'
```
