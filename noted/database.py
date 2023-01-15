import databases
import sqlalchemy


class Database:
    DATABASE_URL = "sqlite:///./test.db"

    def __init__(self) -> None:
        self._database = databases.Database(self.DATABASE_URL)

        [tasks] = self.start_engine()
        self._tasks = tasks

    async def connect(self) -> None:
        await self._database.connect()

    def start_engine(self) -> None:
        """Prepare tables and start the engine"""
        metadata = sqlalchemy.MetaData()

        tasks = sqlalchemy.Table(
            "tasks",
            metadata,
            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column("text", sqlalchemy.String),
            sqlalchemy.Column("is_completed", sqlalchemy.Boolean),
        )

        engine = sqlalchemy.create_engine(
            self.DATABASE_URL,
            connect_args={"check_same_thread": False},
        )

        metadata.create_all(engine)

        return [tasks]
