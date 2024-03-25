from typing import List
from sqlalchemy import create_engine, Column, DateTime
import sqlalchemy as sa
from gino import Gino
from data import config
from sqlalchemy.ext.declarative import declarative_base
import datetime

db = Gino()
Base = declarative_base()

class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, column.name)
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"

class TimedBaseModel(BaseModel):
    __abstract__ = True
    created_at = Column(DateTime(True), server_default=sa.func.now())
    updated_at = Column(
        DateTime(True),
        default=datetime.datetime.now(tz=datetime.timezone.utc),
        onupdate=datetime.datetime.now(tz=datetime.timezone.utc),
        server_default=sa.func.now(),
    )

try:
    engine = create_engine(config.POSTGRES_URI)
    with engine.connect() as connection:
        print("Підключення успішне! Можете виконувати запити до бази даних.")
except Exception as e:
    print(f"Підключення не вдалося. Помилка: {e}")