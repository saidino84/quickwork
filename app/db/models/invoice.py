from dataclasses import dataclass

@dataclass
class Invoice:
    id:int=0
    date:str=None
    number:int=None
    supplier:str=None
    entry_done:bool=False
    has_finalized:bool=0
    sujit:bool=0
     
        
    def from_json(self,json)->object:
        return Invoice(
            date=json['DATA'],
            number=json['NUMERO'],
            supplier=json['FORNECEDOR'],
            entry_done=json['ENTRADA'],
            has_finalized=json['FINALIZAÇÃO'],
            sujit=json['SUJIT']
        )
    def copy_with(self,id:int=None,date:str=None,number:int=None,supplier:str=None,entry_done:bool=None,has_finalized:bool=None,sujit:bool=None):
        ...