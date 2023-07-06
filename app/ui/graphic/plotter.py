from flet.canvas import Canvas,Circle,Line,Path 
from flet import (UserControl,Container,colors,Text,PaintingStyle,Paint,Column
)
class Graphic(UserControl):
    def __init__(self,**kw):
        super().__init__(**kw)
        self.width=600
        self.height=200
        self.dada=[120,54,90,45,76,200,120]
        self.x_init=0
        self.y_init=self.dada[0]
        self.distance=self.width/len(self.dada)
        self.ctx_padding=20
    def draw_lines(self):
        ctx_h=self.height-self.ctx_padding
        __path=Path(elements=[
            # Path.LineTo()
        ])
        _paint=Paint(color=colors.AMBER,stroke_width=self.distance*0.4,style=PaintingStyle.STROKE)
        __path.paint=_paint
        for y in self.dada:
            _move=Path.MoveTo(self.x_init+20,ctx_h)
            __path.elements.append(_move)
            line=Path.LineTo(self.x_init+20,ctx_h-y,type='lineto')
            __path.elements.append(line)
            self.x_init+=self.distance
        return __path
    def draw_graph(self):
        ctx_h=self.height-self.ctx_padding
        ctx_w=self.width-self.ctx_padding
        _stroke_painter=Paint(
            color=colors.BLUE,
            stroke_width=2,
            style=PaintingStyle.STROKE,
        )
        _circ=Circle(ctx_w/2,(ctx_h/2)+self.ctx_padding/2,ctx_h/2,paint=_stroke_painter)
        self.ctx=Canvas(
            height=ctx_h,width=ctx_w,
            shapes=[
                _circ,
            ]
        )
        _line_painter=Paint(color=colors.RED,
            stroke_width=1,
            style=PaintingStyle.STROKE,)
        lines=Line(
            x1=_circ.x,y1=_circ.y,x2=_circ.x+_circ.radius,y2=_circ.y+5-self.ctx_padding,paint=_line_painter
        )
        _dot=Circle(
            x=_circ.x,y=_circ.y,radius=2,paint=Paint(color=colors.WHITE,style=PaintingStyle.FILL,stroke_width=3)
        )
        self.ctx.shapes.append(_dot)
        self.ctx.shapes.append(lines)
        self.ctx.shapes.append(self.draw_lines())
        return self.ctx
    
    def build(self):
        return Column(
            controls=[
                Container(
            bgcolor='#002542',
            height=self.height,
            width=self.width,
            content=self.draw_graph(),),
             Container(
            bgcolor='#002542',
            height=self.height,
            width=self.width,
            # content=self.draw_graph(),
            )
            ]
            
        )