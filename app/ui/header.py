from flet import UserControl,colors,Container,Text

from app import DataStore

class HeaderAction(UserControl):
    def __init__(self,*k,**kw):
        super().__init__(*k,**kw)
    def instace(self):
        DataStore.add_to_control_reference('HeaderAction',self)
    
    def build(self):
        return Container(
            height=45,bgcolor=colors.RED_900,
            content=Text('Transferencias'),
            )