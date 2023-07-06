from dataclasses import dataclass

@dataclass
class ProductModel:
    code:int
    barcode:str
    name:str
    price:float
    cost:float=1.0
    image_uri:str='/assets/'

    def from_json(self,json:dict):
        return ProductModel(
            code=json['code'],
            barcode=json['barcode'],
            name=json['name'],
            price=json['price'],
            cost=json['cost'],
            image_uri=json['image_uri']
        )
        ...
    def copy_with(self,code:int,barcode:str,name:str,price:float,cost:float,image_uri:str):

        ...