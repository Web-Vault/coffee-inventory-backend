import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# MySQL Connection Details
MYSQL_USER = os.getenv("MYSQL_USER", "root")
# Ensure MYSQL_PASSWORD is an empty string if it's not provided or is just an empty line
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DB", "inventory_db")

# Fallback to SQLite if MySQL is not preferred or unavailable
USE_SQLITE = os.getenv("USE_SQLITE", "false").lower() == "true"

if USE_SQLITE:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./inventory.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # Handle empty password correctly in the connection string
    password_part = f":{MYSQL_PASSWORD}" if MYSQL_PASSWORD else ""
    SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}{password_part}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        # Test connection
        with engine.connect() as conn:
            pass
    except Exception as e:
        print(f"MySQL connection failed: {e}. Falling back to SQLite...")
        # Try without password explicitly for blank password scenarios
        try:
            SQLALCHEMY_DATABASE_URL_NOPASS = f"mysql+mysqlconnector://{MYSQL_USER}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
            engine = create_engine(SQLALCHEMY_DATABASE_URL_NOPASS)
            with engine.connect() as conn:
                print("Connected to MySQL with blank password.")
        except:
            SQLALCHEMY_DATABASE_URL = "sqlite:///./inventory.db"
            engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
