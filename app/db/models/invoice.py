from dataclasses import dataclass

@dataclass
class Invoice:
    id:int=0
    date:str=None
    number:int=None
    supplier:str=None
    entry:bool=False
    finalized:bool=0
    sujit:bool=0
     
        
        