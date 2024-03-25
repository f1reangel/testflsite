import asyncio
from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean
from sqlalchemy.ext.asyncio import create_async_engine
from data import config

metadata = MetaData()

reservations = Table(
    "reservations_users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("phone_number", String(20)),
    Column("date", String(10)),
    Column("time", String(10)),
    Column("guests_count", Integer),
    Column("table", String(10)),
    Column("news_subscription", Boolean),
)

async def add_reservation(name, phone_number, date, time, guests_count, table, news_subscription):
    engine = create_async_engine(config.POSTGRES_URI)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
        await conn.execute(
            reservations.insert().values(
                name=name,
                phone_number=phone_number,
                date=date,
                time=time,
                guests_count=guests_count,
                table=table,
                news_subscription=news_subscription,
            )
        )

async def db_test():
    await add_reservation('John Doe', '(408)-111-1234', '2024-03-25', '18:00', 4, 'Table 1', True)

asyncio.run(db_test())