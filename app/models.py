from sqlalchemy import Column, Sequence, Integer, Float, String, DateTime
from database import Base

class CoinInfo(Base):
  __tablename__ = 'coin_info'
  id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
  name = Column(String(11))
  image_name = Column(String(11))
  code = Column(String(10))
  place = Column(String(20))
  amount = Column(Float)
  price_init = Column(Integer)
  memo = Column(String(200))
  
  def __init__(self, name, image_name, code, place, amount, price_init, memo):
    self.name = name
    self.image_name = image_name
    self.code = code
    self.place = place
    self.amount = amount
    self.price_init = price_init
    self.memo = memo
    
  def __repr__(self):
    return "<CoinInfo('%d', '%s', '%s', '%s', '%s', '%f', '%d','%s'>" %(self.id, self.name, self.image_name, self.code, self.place, self.amount, self.price_init, self.memo)
