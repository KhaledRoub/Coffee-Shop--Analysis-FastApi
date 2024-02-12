from sqlalchemy import Column, String, Integer, Boolean , ForeignKey
from db import Base, engine

Base.metadata.create_all(engine)

class stores(Base):
    __tablename__ = 'store'
    sales_outlet_id = Column(Integer, primary_key=True)

class customers(Base):
    __tablename__ = 'customer'
    customer_id = Column(Integer, primary_key=True)

class products(Base):
    __tablename__ = 'product'
    product_id = Column(Integer, primary_key=True)
    product_group = Column(String)
    product_category = Column(String)
    product_type = Column(String)
    product = Column(String)
    product_description = Column(String)
    unit_of_measure = Column(String)
    current_wholesale_price = Column(Integer)
    current_retail_price = Column(String) 
    tax_exempt_yn = Column(String)
    promo_yn = Column(String)
    new_product_yn = Column(String) 



class Transactions(Base):
    __tablename__ = 'transaction'
    transaction_id = Column(Integer , primary_key=True)
    transaction_date = Column(String)
    transaction_time = Column(String)
    staff_id = Column(String)
    instore_yn = Column(Boolean, default=False)
    order= Column(String)
    line_item_id=Column(String)
    quantity=Column(String)
    line_item_amount=Column(String)
    unit_price=Column(String)
    promo_item_yn=Column(String)
    hour=Column(String)
    minute=Column(String)
    second=Column(String)
    transaction_id_comb=Column(String)
    sales_outlet_id = Column(Integer, ForeignKey(stores.sales_outlet_id))
    product_id = Column(Integer , ForeignKey(products.product_id))
    customer_id = Column(Integer,ForeignKey(customers.customer_id))
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)

    def __repr__(self):
        return f"\nDescription: {self.transaction_id_comb}\n"

