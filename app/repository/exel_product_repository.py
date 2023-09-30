import re, csv
import asyncio
from app.db.models.product import ProductModel
class ProductRepository:
    def _read_file(self,file):
        _produts=[]
        if self.__check_file__(file):
            try:
                with open(file,'r') as doc:
                    csv_reader=csv.reader(doc)
                    print('file readed ...')
                    for row in csv_reader:
                        print('reading line')
                        print(row)
                        product:ProductModel=ProductModel(code=int(row[0]),barcode=row[5],name=row[1],price=float(row[3].replace(',','')))
                        # _produts.append(product)
       
            except IOError as e:
                print('ERRO AO LER')
            except Exception as e:
                print(e)
        return _produts
    def __check_file__(self,file):
        
        # regx=re.compile(r'(.csv)')
        # regx.findall(file)
        if file.endswith('.csv'):
            print('file found')
            return True
        
        return False