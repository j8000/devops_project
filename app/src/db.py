from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import os
import time
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:password@localhost/dbname")

engine = create_engine(DATABASE_URL)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.
    import app.src.models
    
    # Retry loop to wait for DB to be ready
    retries = 30
    while retries > 0:
        try:
            # Try to connect
            connection = engine.connect()
            connection.close()
            print("Database connection successful.")
            break
        except OperationalError:
            print(f"Database unavailable, retrying... ({retries} retries left)")
            time.sleep(1)
            retries -= 1
            
    if retries == 0:
        print("Could not connect to database after multiple attempts.")
        # Proceeding might fail, but let's try to create_all anyway to show the real error
        
    Base.metadata.create_all(bind=engine)
