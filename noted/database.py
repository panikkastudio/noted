import databases
import sqlalchemy

from sqlalchemy.dialects.sqlite import insert
from sqlalchemy import Column, ForeignKey, select
from sqlalchemy.orm import declarative_base, relationship, Session


Base = declarative_base()


class Dataset(Base):
    __tablename__ = "dataset"

    id = Column("id", sqlalchemy.Integer, primary_key=True)
    name = Column("name", sqlalchemy.CHAR, unique=True)

    examples = relationship(
        "Example",
        back_populates="dataset",
        cascade="all, delete-orphan",
    )


class Example(Base):
    __tablename__ = "example"

    id = Column("id", sqlalchemy.Integer, primary_key=True)
    task_hash = Column("task_hash", sqlalchemy.CHAR, nullable=False)
    payload = Column("payload", sqlalchemy.JSON, nullable=False)
    verdict = Column("verdict", sqlalchemy.CHAR, nullable=True)

    dataset_id = Column(sqlalchemy.Integer, ForeignKey("dataset.id"), nullable=False)
    dataset = relationship("Dataset", back_populates="examples")


class Database:
    def __init__(self) -> None:
        self._database_url = f"sqlite:///./zatabase.db"
        self._database = databases.Database(self._database_url)
        self._engine = self.start_engine()

    def start_engine(self) -> None:
        """Prepare tables and start the engine"""
        engine = sqlalchemy.create_engine(
            self._database_url,
            connect_args={"check_same_thread": False},
        )

        Base.metadata.create_all(engine)
        return engine

    def add_dataset(self, dataset: str):
        with Session(self._engine) as session:
            stmt = insert(Dataset).values(name=dataset).on_conflict_do_nothing()
            session.execute(stmt)
            session.commit()

    def get_datasets(self):
        with Session(self._engine) as session:
            stmt = select(Dataset)
            result = session.execute(stmt)
            return [r[0].name for r in result]

    def get_examples(self, dataset: str):
        with Session(self._engine) as session:
            stmt = select(Dataset).where(Dataset.name == dataset)
            result = session.execute(stmt)

            dataset = result.fetchone()
            if dataset is None:
                return None

            # examples = dataset.examples()
            # print(examples)
