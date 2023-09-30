import asyncio
from typing import List
from app import DataStore
from app.db.models import Product
from app.repository.db_repository import DbRepository
# from app.ui.price_report import PriceReport
from flet import *
from datetime import datetime

class AppController:
  
    @staticmethod
    def get_input_data():
        
        form= DataStore.control_reference.get('DocGenerator')
        # date=datetime.now()
        # form.date_inpt.current.value=f"{date.day}/{date.month}/{date.year}"
        print(form.fornecedor_inpt.current.value)
        _fornecedor=form.fornecedor_inpt.current.value
        _product_name=form.product_name_inpt.current.value
        _invoice_num=form.invoice_num_inpt.current.value
        _date=form.date_inpt.current.value
        _product_code =form.produt_code_inpt.current.value
        _old_price=form.old_pice_inpt.current.value
        _new_price=form.new_pice_inpt.current.value
        fields=[_new_price,_old_price,_product_code,_date,_invoice_num,_product_name,_fornecedor]
        for field in fields:
            if len(field.strip()) <2:
                print('Preecher os dados')
                def close_dlg(e):
                    dialog.open = False
                    e.control.page.update()
                dialog=AlertDialog( 
                    modal=True,
                    title=Text("Falha Sua !",color=colors.RED),
                    content=Text("Preecher Todos os campos se for pra salvar"),
                    actions=[
                        TextButton("Okay", on_click=close_dlg),
                        # TextButton("Sim", on_click=None),
                    ],
                        actions_alignment=MainAxisAlignment.END,
                        on_dismiss=lambda e: print("Modal dialog dismissed!"),
                    )
                form.page.dialog = dialog
                dialog.open=True
                form.page.update()
                return 'Preecher os dados'
            
        DbRepository().save_product(
                    supplier=_fornecedor,
                    name=_product_name,
                    invoice=_invoice_num,
                    date=_date,
                    code=_product_code,
                    oldprice=_old_price,
                    newprice=_new_price
                )
        repo=DbRepository() 
        asyncio.run(repo.run_compilation())
        form.product_name_inpt.current.value=''
        form.produt_code_inpt.current.value=''
        form.old_pice_inpt.current.value=''
        form.new_pice_inpt.current.value=''
        form.data_table.rows=AppController.get_product_from_db()  
        print('-----update from controller ------')
        form.update()
    def _get_data_row_item(product:Product)->DataRow:
        return DataRow(
            cells=[
                DataCell( content=Text(f"{product.code}") ),
                DataCell( content=Text(f"{product.oldprice}") ),
                DataCell( content=Text(f"{product.newprice}") ),
                DataCell( content=Text(f"{product.invoice}") ),
                DataCell( content=Text(f'{product.date}') ),
                DataCell( content=Text(f'{product.supplier}') ),
                DataCell( content=Text(f'{product.description}') ),
            ]
        )

        ...
    def get_product_from_db() ->List[DataRow]:
        db_repository=DbRepository()
        asyncio.run(db_repository.run_compilation())
        produtos=db_repository.products
        print('#############GEEETING PRODUTS FROM REPOSITORY##########')
        # print(self.produtos)
        print('#############GEEETING PRODUTS FROM REPOSITORY##########')
        # self.update()
        return list(map(lambda item:AppController._get_data_row_item(item),produtos
                         ))
        
        
        