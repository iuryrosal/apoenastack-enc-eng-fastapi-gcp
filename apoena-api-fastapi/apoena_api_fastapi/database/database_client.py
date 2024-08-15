from sqlalchemy import create_engine, MetaData


class DatabaseClient:
    def __init__(self) -> None:
        self.metadata = MetaData()
        self.engine = create_engine("postgresql://postgres:postgres@localhost:5432/fakedata")