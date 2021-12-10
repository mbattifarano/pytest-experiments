import datetime as dt
from typing import List
from sqlalchemy import (
    create_engine, select, Column, Integer, Text, JSON, DateTime
)
from sqlalchemy.orm import declarative_base, Session
from .config import EXPERIMENT_TABLENAME
from .common import mark_utc
from .json_tools import json_serializer, json_deserializer


Base = declarative_base()


class ExperimentModel(Base):
    """The data model for an experiment.

    This model leverages the `JSON` datatype which is currently only supported
    by the following backends:

    - PostgreSQL
    - MySQL
    - SQLite as of version 3.9
    - Microsoft SQL Server 2016 and later

    See https://docs.sqlalchemy.org/en/14/core/type_basics.html?highlight=data%20types#sqlalchemy.types.JSON  # noqa
    """
    __tablename__ = EXPERIMENT_TABLENAME

    id = Column("id", Integer, primary_key=True, autoincrement=True,
                comment="A unique identifier for an experiment run")
    start_time = Column("start_time", DateTime,
                        comment="The UTC timestamp of the experiment start")
    end_time = Column("end_time", DateTime,
                      comment="The UTC timestamp of the experiment end")
    name = Column("name", Text, nullable=False,
                  comment="The name of the experiment")
    outcome = Column("outcome", Text, nullable=False,
                     comment="The outcome of the experiment")
    parameters = Column("parameters", JSON, nullable=False,
                        comment="The experiment input parameters")
    data = Column("data", JSON, nullable=False,
                  comment="Data collected during the experiment")

    @property
    def start_time_tz(self) -> dt.datetime:
        """The timezone-aware experiment start timestamp."""
        return mark_utc(self.start_time)

    @property
    def end_time_tz(self) -> dt.datetime:
        """The timezone-aware experiment end timestamp."""
        return mark_utc(self.end_time)


def initialize_database(engine):
    """Initialize a database with the experiments table."""
    return Base.metadata.create_all(engine)


class StorageManager:
    def __init__(self, db_uri: str) -> None:
        self._db_uri = db_uri
        self.engine = create_engine(
            db_uri,
            json_serializer=json_serializer,
            json_deserializer=json_deserializer,
            future=True
        )
        initialize_database(self.engine)

    @property
    def db_uri(self) -> str:
        return self._db_uri

    def create_session(self) -> Session:
        """Create a database session."""
        return Session(self.engine)

    def record_experiment(self, experiment: ExperimentModel):
        """Record an experiment to the database.

        Args:
            experiment (ExperimentModel): The experiment to record.
        """
        with self.create_session() as session, session.begin():
            session.add(experiment)

    def get_all_experiments(self) -> List[ExperimentModel]:
        """Return all experiments in the database."""
        with self.create_session() as session:
            return (
                session.execute(select(ExperimentModel))
                       .scalars()
                       .all()
            )
