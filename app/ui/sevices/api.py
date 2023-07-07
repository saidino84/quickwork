import aiohttp
import asyncio
from pprint import pprint
import pandas as pd
from app.db.models.invoice import Invoice

class ApiTester:
    def __init__(self,loader_value=None,loader=None) -> None:
        self.loader_value=loader_value
        self.loader=loader

    async def run_compilation(self,e):
        # self.loader_value=True
        # self.loader.value=self.loader_value
        self.loader.update()
        print(self.loader)
        # await asyncio.gather(self.get_data())
        await asyncio.gather(self.read_file('assets/invoice_report.xlsx'))
      
        self.loader.update()
        print(f' LOADERS VALUE IS {self.loader}')
    def read_file(self,file):
        self.loader_value=True
        self.loader.value=self.loader_value
        self.loader.update()
        xlx = pd.ExcelFile(file)
        data_frame= pd.read_excel(xlx,sheet_name="invoices",skiprows=[0,1])
        invoices =[Invoice(id=index,
                            date=row['DATA'],
                           number=row['NUMERO'],
                           supplier=row['FORNECEDOR'],
                           entry=row['ENTRADA'],finalized=row['FINALIZAÇÃO'],
                           sujit=row['SUJIT'])
                           for index,row in data_frame.iterrows()]
        pprint(invoices)
        self.loader_value=0
        self.loader.value=self.loader_value
        self.loader.update()



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