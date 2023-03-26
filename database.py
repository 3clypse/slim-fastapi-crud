from sqlalchemy import create_engine, MetaData
import os
from dotenv import load_dotenv

import databases

load_dotenv()

# connect_args={"check_same_thread": False}
# needed only for SQLite. It's not needed for other databases.
engine = create_engine(
    str(os.environ.get('DATABASE_URL')), connect_args={"check_same_thread": False}
)

database = databases.Database(str(os.environ.get('DATABASE_URL')))
metadata = MetaData()
