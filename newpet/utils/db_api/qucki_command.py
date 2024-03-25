from asyncpg import UniqueViolationError
from utils.db_api.dbtest import Reservation


async def add_reservation(name: str, phone_number: str, date: str, time: str, guests_count: int, table: str, news_subscription: bool):
    try:
        reservation = Reservation(name=name, phone_number=phone_number, date=date, time=time, guests_count=guests_count, table=table, news_subscription=news_subscription)
        await reservation.create()
    except UniqueViolationError:
        print('Запис не доданий')


async def select_all_reservations():
    reservations = await Reservation.query.gino.all()
    return reservations


async def count_reservations():
    count = await Reservation.query.count().gino.scalar()
    return count


async def select_reservation(reservation_id):
    reservation = await Reservation.query.where(Reservation.id == reservation_id).gino.first()
    return reservation


async def update_reservation(reservation_id, **kwargs):
    reservation = await select_reservation(reservation_id)
    await reservation.update(**kwargs).apply()