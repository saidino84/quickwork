from random import randint
from datetime import date

import asyncio
from typing import List
from flet import *

from app import DataStore
from flet.canvas import Canvas,Line,Circle,Path
from app.db.models import Product
from app.db.models.invoice import Invoice

from app.db.models.product import ProductModel
from app.repository.db_repository import DbRepository
from app.repository.exel_product_repository import ProductRepository
from app.controllers.app_controller import AppController
from app.ui.header import HeaderAction
from app.ui.sevices.api import ApiTester
from settings import Utils
from app.ui.sevices.openeditor import start_app

class DocGenerator(UserControl):
    def __init__(self,size=None,**kw):
        super().__init__(**kw)
        self.size :list=size
        self.fornecedor_inpt= Ref[TextField]()
        self.invoice_num_inpt= Ref[TextField]()
        self.product_name_inpt= Ref[TextField]()
        self.date_inpt= Ref[TextField]()
        self.old_pice_inpt= Ref[TextField]()
        self.new_pice_inpt= Ref[TextField]()
        self.produt_code_inpt=Ref[TextField]()
        self.db_repository=DbRepository()
    
    
    
    def instace(self):
        DataStore.add_to_control_reference('DocGenerator',self)
    
    def build(self):
        self._progress_value=0
        self._loaderuix=self._loader()
        self.instace()
        self.data_table=DataTable(
            # height=400, 
            # scroll=True,
            column_spacing=12,
            columns=[
                DataColumn(label=Text('BARCODE'),),
                DataColumn(label= Text('OLD', ) ,),
                DataColumn(label=Text('NEW', ),),
                DataColumn(label=Text('INVOICE')),
                DataColumn(label=Text('DATE')),
                DataColumn(label=Text('provider'.upper())),
                DataColumn(label=Text('description'.upper())),
            ],
            rows= self.get_product_from_db()  
        )
        return Container(
            content=Row(
            alignment=MainAxisAlignment.START, 
            vertical_alignment=CrossAxisAlignment.START,
                controls=[
                    Container(
                 width=self.size[0]/3,bgcolor=colors.WHITE38,border_radius=8,
                border=Border(bottom=BorderSide(width=30,color=colors.RED_400),left=BorderSide(width=2,color=colors.RED_400),right=BorderSide(width=2,color=colors.RED_400)),
                # padding=padding.all(8),
                content=Column(
                    alignment=MainAxisAlignment.START,
                    horizontal_alignment=CrossAxisAlignment.START,
                    controls=[
                        # LEFT BOX
                        self._setup_left_box(width=self.size[0]/3),
                    ],
                ),
            ),
                        # MIDDLE BOX
                        
                        self._setup_main_box()
                ]
            )


        )
    def _loader_state(self):
        progress_state=Container(
            opacity=0,
            margin=margin.symmetric(horizontal=5),
            height=2,
                content=ProgressBar(value=True,bgcolor=colors.RED_ACCENT,color=colors.WHITE),
                              ),
        return progress_state

    def _input(self,label:str=None,width=None,value=None,ref:Ref=None):
        return Container(
            width=width,
            padding=padding.all(5),
            margin=margin.symmetric(horizontal=5),
            height=70, bgcolor=colors.WHITE,
                            border_radius=BorderRadius(bottom_right=2,bottom_left=2,top_left=0,top_right=0) ,
                         content=Column(controls=[
                             Text(f'{label} ',style=TextStyle(color=colors.BLACK),color=colors.BLACK87 ),
                             TextField(
                            ref=ref,
                            value=value,
                            height=32,content_padding=5,cursor_color='white', bgcolor=colors.BLACK12,
                             text_style=TextStyle(weight=FontWeight.BOLD,color=colors.RED_ACCENT,
                                                  ),border_color=colors.TRANSPARENT,
                            
                            )
                         ])
                         )
    
    def _dropdown_input(self,label='',width=None,ref:Ref=None):
        return Container(
            width=width,
            padding=padding.all(5),
            margin=margin.symmetric(horizontal=5),
            height=70, bgcolor=colors.WHITE,
                            border_radius=BorderRadius(bottom_right=2,bottom_left=2,top_left=0,top_right=0) ,
                         content=Column(controls=[
                             Text(f'{label} ',style=TextStyle(color=colors.BLACK),color=colors.BLACK87 ),
                             Container(
                                bgcolor=colors.BLACK12,
                                # bgcolor=colors.RED_ACCENT,
                                # padding=padding.only(bottom=8),
                                content=Dropdown(
                                ref=ref,
                                content_padding=8,
                            height=30,
                            value=Utils.get_providers()[0],
                            filled=False,
                            border_color='transparent',
                            bgcolor=colors.BLACK12,
                            text_size=12,
                            color=colors.RED_ACCENT,text_style=TextStyle(18,weight=FontWeight.W_600),
                            options=
                                    list(map(lambda item:dropdown.Option(item),Utils.get_providers())),
                        ))
                         ])
                         )
    def _search_input(self):
         return Container(
             height=70,
            # margin=margin.all(8),
            padding=padding.all(5),
            bgcolor=colors.RED_ACCENT,
            border_radius=BorderRadius(bottom_right=2,bottom_left=2,top_left=0,top_right=0),
            content=Column(
                    controls=[
                        Text('Procurar Transferencia ', style=TextStyle(color=colors.RED,)),
                        TextField(
                height=32,content_padding=5,cursor_color='white', bgcolor=colors.BLACK12,
                    text_style=TextStyle(weight=FontWeight.BOLD,color=colors.WHITE
                                        ),border_color=colors.RED_ACCENT,
                ),
                    ]
            ),
             
         )
    
    def _setup_left_box(self,width):
        return Container(
            content=Column(
                controls=[
                    # self._search_input(), 
                    # self._loader_state(),
                    Container(
            #  height=20,
            width=width,
            # margin=margin.all(8),
            padding=padding.all(5),
            bgcolor=colors.RED_ACCENT,
            border_radius=BorderRadius(bottom_right=2,bottom_left=2,top_left=0,top_right=0),
            content=Text('COMPARAÇÃO DE PREÇOS',color=colors.WHITE,style=TextStyle(size=8,
                    weight=FontWeight.W_900,color=colors.WHITE,
                                                                ))),
                    Container(
            # opacity=0,
            border_radius=border_radius.all(8),
                margin=margin.symmetric(horizontal=5),
                height=10,
                content=self._loaderuix,
                              ),
            #inputs
            Container(
                height=200,
                content=ListView(
            controls=[
                Column(
            # height=350,
            auto_scroll=True,
            controls=[
                    self._dropdown_input(label='FORNECEDOR',ref=self.fornecedor_inpt),
                    Row( controls=[
                        self._input(ref=self.date_inpt,label='DATA',width=(width/2)-20,value=date.today().strftime("%d/%m/%Y")),
                        self._input(ref=self.invoice_num_inpt,label='INVOICE',width=(width/2)-16),
                        ]),
                    self._input(ref=self.product_name_inpt,label='DESCRIPTION',),
                    self._input(ref=self.produt_code_inpt,label='BARCODE'),
                    Row( controls=[
                        self._input(ref=self.old_pice_inpt,label='OLD COST',width=(width/2)-20),
                        self._input(ref=self.new_pice_inpt,label='NEW COST',width=(width/2)-16),
                        ]),
            ]
        )])),#container #inputs
                    self._btn_go(label="S A V E",func=self.save_data),
            Container(
                margin=margin.symmetric(horizontal=5,vertical=12),
                bgcolor=colors.WHITE24,
                gradient=LinearGradient(
                        colors=[colors.BLACK26,colors.WHITE,colors.BLACK]
                ),
                width=width,
                padding=8,
                alignment=Alignment(5,5),
                content=Text('Calculo de Iva')


            ),
            # self.data_table,
            # DATA TABLE
            Container(
            height=200,
            
            content=Column(
                scroll=ScrollMode.ADAPTIVE,
                
                controls=[
                    #TODO ENABLE IT TO LOAD DATA
                    self.data_table,
                     ]
                            )
                 ) ,
            ListTile(width=width,
                     on_click=lambda x:asyncio.run(start_app(x)),
                     title=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                
                controls=[
                Text("Backers Cream Crackers  Crisp Crackers 200g".split('  ')[0],max_lines=2,overflow=TextOverflow.FADE,size=12),
                Icon(icons.ARROW_CIRCLE_UP,color=colors.RED_ACCENT),
                Container(width=20),
                ]),
                     subtitle=Column(
                                    run_spacing=2,
                                    spacing=2,
                                    controls=[
                                    self.section('Barcode:',value="8745852425"),
                                    self.section('Old price:',value="87.25"),
                                    self.section('New Price:',value="175.25"),
                                    ]),),
                    self._graphic(),

                ])
        )
    def section(self,section,value=""):
        return Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            # vertical_alignment=CrossAxisAlignment.START,
            controls=[
                Text(f'{section}'),
                Text(f'{value}',style=TextStyle(weight=FontWeight.BOLD),color="#0B4B8F"),
                      ]
        )

    def _btn_go(self,label='BOTAO',func=None):
        return Container(
            alignment=alignment.center,
            border_radius=2,
            padding=padding.all(5),
            content=ElevatedButton(
            bgcolor =colors.RED_ACCENT,#"#081d33",
            color=colors.WHITE,#colors.RED_ACCENT,
            content=Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
            Icon(name=icons.ADD_ROUNDED,size=12),
            Text(label , style=TextStyle(weight=FontWeight.BOLD,color=colors.BLACK87,
                                                  ),),
            ]
            ),style=ButtonStyle(shape={'':RoundedRectangleBorder(radius=20)}),
            
            # on_click=lambda x:ProductRepository()._read_file('assets/mercearia.csv')
            # on_click=lambda x:asyncio.run(ApiTester(loader_value=self._progress_value,loader=self._loaderuix).run_compilation(x))
            #on_click=lambda x:asyncio.run(ApiTester(loader_value=self._progress_value,loader=self._loaderuix,datatable=DocGenerator._datatable_list).run_compilation(x))
            on_click=lambda x:func(),
            )
        )
    

    #  MAIN BOX SETUP
    def _setup_main_box(self):
        return Column(
            alignment=MainAxisAlignment.START, 
            controls=[
                HeaderAction(),
                Container(
                    width=770,
                    height=300,
                    content=ListView(
            
                    controls=[
                        
                        
                        DocGenerator._datatable_list,
                        Container(height=32,bgcolor=colors.AMBER_100,content=Row(
                            controls=[
                                Text('#'),
                                Text('Barcode'),
                                Text('Description'),
                                Text('Old Price'),
                                Text('New Price'),
                                 
                            ],
                        )),
                        GridView(
                            expand=1,
                            runs_count=5,
                            max_extent=100,
                            child_aspect_ratio=2.5,
                            spacing=5,run_spacing=5,
                            controls=[
                            Text('#'),
                                Container(
                                    height=10,width=10,bgcolor=colors.RED,
                                    content=Text('Barcode'),),
                                Text('Description'),
                                Text('Old Price'),
                                Text('New Price')
                        ])

                        
                        ],
                    auto_scroll=True,
                    ),
                    ),
                    Container(
                        alignment=alignment.center,
                        border_radius=2,
                        # padding=padding.all(5),
                        content=ElevatedButton(
                        bgcolor =colors.WHITE,#"#081d33",
                        color=colors.RED_ACCENT,
                        content=Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                        # Icon(name=icons.ADD_ROUNDED,size=12),
                        Text("GERAR RELATORIO" , style=TextStyle(weight=FontWeight.BOLD,color=colors.BLACK87,
                                                            ),),
                        ]
                        ),style=ButtonStyle(shape={'':RoundedRectangleBorder(radius=2)}),
                        
                        on_click=lambda x:ProductRepository()._read_file('assets/mercearia.csv')
                        )
                    )
                    
            ]
        ) 
    def _graphic(self):
        cv_height=190
        _line_painter=Paint(color=colors.RED,
            stroke_width=1,
            style=PaintingStyle.STROKE,)
        _lines=Line(
            25,125,85,65,_line_painter,
        )
        _ctx=Canvas(
            height=cv_height,
            width=self.size[0]/3,
            
            shapes=[
                # _lines,
            ],
            
        )
        _graph_lines=self.draw_lines(dada=[0,80,35,115,70,60],height=cv_height,width=self.size[0]/3,)
        _ctx.shapes.append(_graph_lines)
        return Container(
            margin=margin.all(5),
            height=100,
            bgcolor='#17043A',
            # gradient=RadialGradient(center=Alignment(3.25,-1.25),radius=1.4,
            # colors=['#D4430A','#0DC6FF', ]),
            border=Border(),
            # content=_ctx,
            content=Image('assets/plotted.png')
        )
    def draw_lines(self,dada:list,width:int,height:int):
        ctx_h=height-8
        distance=width/len(dada)
        __path=Path(elements=[
            # Path.LineTo()
        ])
        _paint=Paint(color=colors.AMBER,stroke_width=3,#distance*0.4,
                     style=PaintingStyle.STROKE)
        __path.paint=_paint
        x_init=5
        # _move=Path.MoveTo(x_init+20,ctx_h)    
        for y in  dada:
            # __path.elements.append(_move)
            line=Path.LineTo(x_init+20,ctx_h-y,type='lineto')
            __path.elements.append(line)
            x_init+= distance
        return __path
    
    def _loader(self  ):
        return ProgressBar( bgcolor=colors.RED_ACCENT,value=self._progress_value)
       
 
    def _get_data_row_item(self,product:Product)->DataRow:
        return DataRow(
            cells=[
                DataCell( content=Text(f"{product.code}") ),
                DataCell( content=Text(f"{product.oldprice}", ) ),
                DataCell( content=Text(f"{product.newprice}", ) ),
                DataCell( content=Text(f"{product.invoice}") ),
                DataCell( content=Text(f'{product.date}') ),
                DataCell( content=Text(f'{product.supplier}') ),
                DataCell( content=Text(f'{product.description}') ),
            ]
        )

        ...
    def get_product_from_db(self) ->List[DataRow]:
        asyncio.run(self.db_repository.run_compilation())
        print('#############GEEETING PRODUTS FROM REPOSITORY##########')
        self.produtos=self.db_repository.products
        print(self.produtos)
        # self.update()
        return list(map(lambda item:self._get_data_row_item(item),self.produtos
                         ))   
    
    def _get_product_row_item(self,product:ProductModel)->DataRow:
        return DataRow(
            color=colors.BLACK,
            cells=[
                DataCell(content=Text(f"{product.code}")),
                DataCell(content=Text(f"{product.barcode}")),
                DataCell(content=Text(f"{product.name}")),
                DataCell(content=Text(f"{product.price}")) 
            ]
        )
    @staticmethod
    def _get_invoice_row_item(invoice:Invoice)->DataRow:
        return DataRow(
            color=colors.BLACK,
            cells=[
                DataCell(content=Text(f"{invoice.date}")),
                DataCell(content=Text(f"{invoice.number}")),
                DataCell(content=Text(f"{invoice.supplier}")),
                DataCell(content=Text(f"{invoice.entry_done}")),
                DataCell(content=Text(f"{invoice.has_finalized}")),
                DataCell(content=Text(f"{invoice.sujit}")) 
            ]
        )
    def __get_produts(self,count:int) -> list[DataRow]:
        '''eXample method'''
        _products=[]

        for i in range(count):
            _products.append(
                ProductModel(
                    code=randint(12,15)*i+1,
                    barcode=randint(12532,65455)*i+1,
                    name=f'PRODUCT Item {i}',
                    price=randint(251,365)
                )
            )
        return  list(map(lambda item:self._get_product_row_item(item),_products))
    
    def _get_products_from_doc(self,products:list[ProductModel]) ->list[DataRow]:
        '''getting data from excel sheet'''
        
        return list(map(lambda item:self._get_product_row_item(item),products))
    @staticmethod
    def _get_invoices_from_doc(invoices:list[Invoice]) ->list[DataRow]:
        '''getting data from excel sheet'''
        return list(map(lambda item:DocGenerator._get_invoice_row_item(item),invoices))
    
    _datatable_list=DataTable(
            heading_row_color=colors.RED_ACCENT,
            data_row_color=colors.WHITE,
            show_checkbox_column=True,
            columns=[
                    DataColumn(label=Text('Date')),
                    DataColumn(label=Text('Numero')),
                    DataColumn(label=Text('Fornecedor')),
                    DataColumn(label=Text('Entrada')),
                    DataColumn(label=Text('Finalizacao')),
                    DataColumn(label=Text('Sujit')),
                 ],
            # rows = self.__get_produts(10)
            # rows = self._get_products_from_doc(products=ProductRepository()._read_file('assets/mercearia.csv'))
            rows = _get_invoices_from_doc(invoices=ApiTester().invoices)
                
             )

    def save_data(self):
        AppController.get_input_data()