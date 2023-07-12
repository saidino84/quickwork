from random import randint

import asyncio
from flet import *

from app import DataStore
from flet.canvas import Canvas,Line,Circle,Path
from app.db.models.invoice import Invoice

from app.db.models.product import ProductModel
from app.repository.product_repository import ProductRepository
from app.ui.sevices.api import ApiTester

class DocGenerator(UserControl):
    def __init__(self,size=None,**kw):
        super().__init__(**kw)
        self.size :list=size
    
    def _loader_state(self):
        progress_state=Container(
            opacity=0,
            margin=margin.symmetric(horizontal=5),
            height=2,
                content=ProgressBar(value=True,bgcolor=colors.RED_ACCENT,color=colors.WHITE),
                              ),
        return progress_state

    def _input(self,label:str=None,width=None):
        return Container(
            width=width,
            padding=padding.all(5),
            margin=margin.symmetric(horizontal=5),
            height=70, bgcolor=colors.WHITE,
                            border_radius=BorderRadius(bottom_right=2,bottom_left=2,top_left=0,top_right=0) ,
                         content=Column(controls=[
                             Text(f'{label} ',style=TextStyle(color=colors.BLACK),color=colors.BLACK87 ),
                             TextField(
                            height=32,content_padding=5,cursor_color='white', bgcolor=colors.BLACK12,
                             text_style=TextStyle(weight=FontWeight.BOLD,color=colors.RED_ACCENT,
                                                  ),border_color=colors.TRANSPARENT,
                            
                            )
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
    
    def instace(self):
        DataStore.add_to_control_reference('DocGenerator',self)
    
    def build(self):
        self._progress_value=0
        self._loaderuix=self._loader()
        self.instace()
        _input_with_label = Container(
                    ),
        return Container(
            
            content=Row(
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
                        self._setup_left_box(),
                    ],
                ),
            ),
                        # MIDDLE BOX
                        self._setup_main_box()
                ]
            )


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
        
    def _setup_left_box(self):
        return Column(
            controls=[
                    self._search_input(), 
                    # self._loader_state(),
                    Container(
            # opacity=0,
                margin=margin.symmetric(horizontal=5),
                height=2,
                content=self._loaderuix,
                              ),
                    self._input(label='DATA'),
                    self._input(label='NUMERO'),
                    self._input(label='FORNECEDOR'),
                    Row( controls=[
                        self._input(label='ENTRADA',width=80),
                        self._input(label='FINALIZADA',width=100),
                        ]),
                    self._btn_go(),
                    self._graphic(),
            ]
        )
    
    def _btn_go(self):
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
            # Icon(name=icons.ADD_ROUNDED,size=12),
            Text("LER O EXCEL FILE" , style=TextStyle(weight=FontWeight.BOLD,color=colors.BLACK87,
                                                  ),),
            ]
            ),style=ButtonStyle(shape={'':RoundedRectangleBorder(radius=2)}),
            
            # on_click=lambda x:ProductRepository()._read_file('assets/mercearia.csv')
            # on_click=lambda x:asyncio.run(ApiTester(loader_value=self._progress_value,loader=self._loaderuix).run_compilation(x))
            on_click=lambda x:asyncio.run(ApiTester(loader_value=self._progress_value,loader=self._loaderuix,datatable=DocGenerator._datatable_list).run_compilation(x))
            )
        )
    

    #  MAIN BOX SETUP
    def _setup_main_box(self):
        return Column(
            controls=[
                Container(
                    width=770,
                    height=300,
                    content=ListView(
            
                    controls=[
                        
                        
                        DocGenerator._datatable_list
                        
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