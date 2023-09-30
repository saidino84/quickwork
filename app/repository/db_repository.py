from datetime import datetime
from typing import List
from app import DataStore
from app.db.models import Base
from app.db import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from app.db.models import User,Product,Supplier
from sqlalchemy import select
import asyncio
import openpyxl
import pandas as pd
from flet import *

class DbRepository:
    products:List[Product]=[]
    # Criar uma sessão assíncrona   
    Session = sessionmaker(engine, expire_on_commit=False)

    def session():
        Session=sessionmaker(bind=engine)
        return Session

    def save_product(self,supplier,name,invoice,date,code,oldprice,newprice):
        with self.Session() as session:
            try:
                Base.metadata.create_all(engine)
            except Exception as e:
                print(e)
            else:
                produto=Product(code=code,description=name,supplier=supplier,oldprice=oldprice,newprice=newprice,date=date,
                                invoice=invoice
                                )
                d=session.add(produto)
                session.commit()
                print(f'Produto adicioado {d}')
                db=DataStore.control_reference.get('PriceReport')
                db.update() 
                print('--------------UPDATED----------------')
            asyncio.run(self.run_compilation())
    async def get_products(self)->List[Product]:
        try:
            with self.Session() as session:
                stmt = select(Product)
                # executar consulta assicrona
                result =session.execute(statement=stmt)
                # obter os resultados como uma lista de objectos
                products_list=result.scalars().all()
                self.products=products_list
                db=DataStore.control_reference.get('PriceReport')
                db.update() 
                print('--------------UPDATED----------------')
                for product  in products_list:
                    print(product.code)
                print('PRODUCT FECHET')
        except Exception as e:
            print(f'FAILED {e}')
        # pprint(self.products)
        for p in self.products:
            print(p.description)
        return self.products
    async def run_compilation(self,e=None):
        await asyncio.gather(self.get_products())

    
    def export_produts(self):
        import pandas as pd
        import os
        form= DataStore.control_reference.get('PriceReport')
        with self.Session() as session:
                stmt = select(Product)
                # executar consulta assicrona
                result =session.execute(statement=stmt)
                # obter os resultados como uma lista de objectos
                products_list=result.scalars().all()
                self.products=products_list
                ui_page=DataStore.control_reference.get('PriceReport')
                dicionario = [product.__dict__ for product in products_list]
                dataframe= pd.DataFrame(dicionario)
                date=datetime.now()
                file=f"{date.day}-{date.month}-{date.year}-{date.hour}-{date.minute}-{date.second}.xlsx"
                dataframe.to_excel(file)
        def close_dlg(e):
            dialog.open = False
            e.control.page.update()
            os.system(file)
        dialog=AlertDialog( 
                modal=True,
                title=Text("Documeto Exported",color=colors.RED),
                content=Text("Documento exportado com sucesso"),
                actions=[
                    TextButton("Abrir", on_click=close_dlg),
                    # TextButton("Sim", on_click=None),
                ],
                    actions_alignment=MainAxisAlignment.END,
                    on_dismiss=lambda e: print("Modal dialog dismissed!"),
                    )
        form.page.dialog = dialog
        dialog.open=True
        form.page.update()

       
         
