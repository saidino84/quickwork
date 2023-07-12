import aiohttp
import asyncio
from pprint import pprint
import pandas as pd
from app.db.models.invoice import Invoice
from flet import (DataCell,DataColumn,Text,DataRow,colors,Icon,icons)

class ApiTester:
    def __init__(self,loader_value=None,loader=None,datatable=None) -> None:
        self.loader_value=loader_value
        self.loader=loader
        self.invoices=[]
        self.datatable=datatable

    async def run_compilation(self,e):
        # self.loader_value=True
        # self.loader.value=self.loader_value
        self.loader.update()
        print(self.loader)
        # await asyncio.gather(self.get_data())
        await asyncio.gather(self.read_file('assets/invoice_report.xlsx'))
        # print(f"*********INVOICES : {self.invoices}*************")
        self.loader.update()
        self.datatable.update()
        print(len(self.datatable.columns))
        print(f' LOADERS VALUE IS {self.loader}')
    async def read_file(self,file):
        self.loader_value=True
        self.loader.value=self.loader_value
        self.loader.update()
        xlx = pd.ExcelFile(file)
        data_frame= pd.read_excel(xlx,sheet_name="invoices",skiprows=[0,1])
         
        invoices =[Invoice(id=index,
                    date=row['DATA'],
                    number=row['NUMERO'],
                    supplier=row['FORNECEDOR'],
                    entry_done=bool(row['ENTRADA']) if row['ENTRADA'] !='nan' else False,
                    has_finalized=bool(row['FINALIZAÇÃO']) if row['FINALIZAÇÃO'] !='nan' else False,
                    sujit=bool(row['SUJIT']) if row['SUJIT'] !='nan' else False)
                    for index,row in data_frame.iterrows()
                           ]
        self.invoices=invoices
        self.loader_value=0
        self.loader.value=self.loader_value
        self.loader.update()
        self.datatable.rows=ApiTester._get_invoices_from_doc(invoices=invoices)
        self.datatable.update()
        print(len(self.datatable.rows))
        await asyncio.sleep(1)



    async def get_data(self):
        temp_list =[]
        print(self.loader_value)
        async with aiohttp.ClientSession() as session:
            async with session.get('https://jsonplaceholder.typicode.com/posts/2') as response:
                res = await response.json()
                pprint(res)
        self.loader_value=0
        self.loader.value=self.loader_value
        self.loader.update()
    @staticmethod
    def _get_invoice_row_item(invoice:Invoice)->DataRow:
        return DataRow(
            color=colors.WHITE,
            on_select_changed=lambda x:print(invoice.number),
            cells=[
                DataCell(content=Text(f"{invoice.date}")),
                DataCell(content=Text(f"{invoice.number}")),
                DataCell(content=Text(f"{invoice.supplier}")),
                DataCell(content=Icon(name=icons.DONE if invoice.entry_done else icons.CANCEL,color=colors.BLUE_ACCENT if invoice.entry_done else colors.RED_ACCENT),),
                DataCell(content=Icon(name=icons.DONE_ALL_ROUNDED if invoice.has_finalized else icons.CANCEL,color=colors.BLUE_ACCENT if invoice.has_finalized else colors.RED_ACCENT)),
                DataCell(content=Icon(name=icons.DONE if invoice.sujit else icons.CANCEL_ROUNDED,color=colors.BLUE_ACCENT if invoice.sujit else colors.RED_ACCENT), ) 
            ]
        )
    def _get_invoices_from_doc(invoices:list[Invoice]) ->list[DataRow]:
        '''getting data from excel sheet'''
        
        return list(map(lambda item:ApiTester._get_invoice_row_item(item),invoices))
        
    #         )