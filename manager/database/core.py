from sqlalchemy.engine import create_engine

# specify the location of the generated database file.
database_url = "sqlite+pysqlite:///./library.db"

# create database engine using sqlachemy
engine = create_engine(
    url=database_url,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False},
)
