import asyncio
import flet.canvas  as cv
from flet import *
from app.services.scrap.scrapper import Scrapper
from app.ui.doc_generator import DocGenerator
from app.ui.graphic.plotter import Graphic
from app.services.reports import generate_doc
from app.db.models import Product,Supplier,Base
# from app.services.scrap.scrapper import Scrapper
''''ChatGpt Services
from app.services.ia.config import get_password,set_env_data
from app.services.ia import IaService

get_password('ROOT')
set_env_data('USER','ADMIN')

IaService().chat_bot()
'''
def main(page:Page):
    width=285
    height=740
    page.window_width=width
    page.window_always_on_top=True
    page.window_height=height
    page.window_resizable=True
    page.bgcolor=colors.WHITE70
    page.padding=0
    page.window_title_bar_buttons_hidden=True
    page.window_title_bar_hidden=False
    page.update()
    _cv=cv.Canvas(
        [cv.Rect(20,50,200,250,paint=Paint(style=PaintingStyle.STROKE,color=colors.RED,),),]
    )
    __root=Column(
        scroll=ScrollMode.ALWAYS,
        auto_scroll=True,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        alignment=MainAxisAlignment.CENTER,
        controls=[
            Container(
        width=page.window_width,
        height=44,
        bgcolor=colors.BLUE_800,
        content=Row(
        alignment=MainAxisAlignment.CENTER,
        controls=[
             Text('Grafico de Transferncias Diarias'),
        ]
        )
            ),
        
        Graphic() ,
        Container(height=36,width=100,content=
                  TextButton(text='Generate Doc',on_click=lambda x:generate_doc(),
                             )),

       
        ]
        )
    
    _root=Column(
        controls=[
            DocGenerator(size=(width,height),)
            
        ]
    )

    page.add(Container(content=_root))
    page.update()
app(target=main,port=5555,
    #view=WEB_BROWSER, web_renderer="html"
    )
