from database import init_db
from database import db_session
from models import CoinInfo

def show_tables():
  queries = db_session.query(CoinInfo)
#  queries = db_session.query(CoinInfo).filter_by(id='11').first() 
  entries = [dict(id=q.id, name=q.name, image_name=q.image_name, code=q.code, place=q.place, iswallet=q.iswallet, amount=q.amount, price_init=q.price_init, memo=q.memo) for q in queries]
  db_session.close()
  return entries
  
def add_entry(datetime, string):
  t = CoinInfo(datetime, string)
  db_session.add(t)
  db_session.commit()
  
def delete_entry(datetime, string):
  db_session.query(CoinInfo).filter(CoinInfo.datetime==datetime, CoinInfo.string==string).delete()
  db_session.commit()
  
def main():
#  print CoinInfo.__table__
#  add_entry("2015-02-06 09:00:05", "test1")
#  delete_entry("2015-02-06 09:00:05","test1")

  show_tables()
#  db_session.close()
  
if __name__ == "__main__" :
  main()
