from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session


database_url = "sqlite+pysqlite:///./library.db"

engine = create_engine(url=database_url, echo=False, future=True)
