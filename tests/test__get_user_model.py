import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from twalchemy.schemas import User
from twalchemy.twalchemy import get_user_model

# load test tweet data
with open("user.json", 'r') as f:
    response = json.load(f)
users = response['data']

# validate user objects
users = [User(**tw) for tw in users]
print(users)

# convert to orm objects
users_orm = [get_user_model(tw) for tw in users]
print(users_orm)

# create session and add objects
engine = create_engine(os.environ['DB_CONNECTION_STRING'], echo=True)
with Session(engine) as session:
    session.add_all(users_orm)
    session.commit()
