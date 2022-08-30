from sqlalchemy.engine import create_engine


database_url = "sqlite+pysqlite:///./library.db"

engine = create_engine(url=database_url, echo=False, future=True)
