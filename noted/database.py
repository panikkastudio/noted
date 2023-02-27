import databases
import sqlalchemy

from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import Column, ForeignKey, select, UniqueConstraint

from ._internal.path import get_base_dir, create_dir_if_not_exist


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
    __table_args__ = (UniqueConstraint("dataset_id", "task_hash", name="_example_uc"),)

    id = Column("id", sqlalchemy.Integer, primary_key=True)
    task_hash = Column("task_hash", sqlalchemy.CHAR, nullable=False)
    verdict = Column("verdict", sqlalchemy.CHAR, nullable=True)
    content = Column("content", sqlalchemy.JSON, nullable=False)

    dataset_id = Column(sqlalchemy.Integer, ForeignKey("dataset.id"), nullable=False)
    dataset = relationship("Dataset", back_populates="examples")


class Database:
    def __init__(self) -> None:
        base_dir = get_base_dir()
        database_dir = f"{base_dir}/dataset"
        create_dir_if_not_exist(database_dir)

        self._database_url = f"sqlite:///{database_dir}/zatabase.db"
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

    def add_example(self, dataset: str, example):
        with Session(self._engine) as session:
            stmt = select(Dataset).where(Dataset.name == dataset)
            result = session.execute(stmt)
            (dataset_,) = result.fetchone()

            values = {
                "dataset_id": dataset_.id,
                "task_hash": example.get("task_hash"),
                "verdict": example.get("verdict"),
                "content": example,
            }

            stmt = insert(Example).values(values).on_conflict_do_nothing()
            session.execute(stmt)
            session.commit()
