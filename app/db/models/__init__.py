from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column,Mapped, relationship
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__='products'
    id: Mapped[int] = mapped_column(primary_key=True)
    date:Mapped[str] 
    invoice:Mapped[str] 
    supplier:Mapped[str]
    code: Mapped[str] 
    description: Mapped[str] 
    oldprice:Mapped[str] 
    newprice:Mapped[str] 

    # supplier_id: Mapped[int] = mapped_column(ForeignKey('suppliers.id'))
    # supplier: Mapped[object] = relationship("Supplier", back_populates="products")
   

    def __init__(self, description,invoice,newprice,oldprice,supplier,code,date):
        self.date=date
        self.invoice=invoice
        self.supplier=supplier
        self.code=code
        self.description = description
        self.oldprice=oldprice
        self.newprice=newprice

class Supplier(Base):
    __tablename__='suppliers'
    id:Mapped[int]=mapped_column(primary_key=True)
    fullname:Mapped[str]

    # produts:Mapped[List['Product']] = relationship(back_populates='supplier', cascade='all, delete-orphan')

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]  
    password: Mapped[str] 

    def __init__(self, name, password):
        self.name = name
        self.password = password
    
    def __repr__(self) -> str:
        return f'User(id={self.id!r}), name={self.name!r}'
