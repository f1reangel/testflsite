from sqlalchemy import Column, BigInteger,Boolean,String,sql
from utils.db_api.db_gino import TimedBaseModel


class Reservation(TimedBaseModel):
    __tablename__ = 'reservations_users'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(50))
    phone_number = Column(String(20))
    date = Column(String(10))
    time = Column(String(10))
    guests_count = Column(BigInteger)
    table = Column(String(10))
    news_subscription = Column(Boolean)

    query: sql.select

    def __repr__(self):
        return f"<Reservation id={self.id} name={self.name}>"