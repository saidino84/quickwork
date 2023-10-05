_tree_colunas=('id',
            "date","barcode","description",
             "old_cost","new_cost","difer",
            "obs","invoice","provider",'user')
tree=event.widget
data=tree.selection()[0]
print(f'Id: {data}')
values=tree.item(data)['values']
print(f'Values: {values}')
colunas=[tree.heading(col,"text") for col in tree["columns"]]

top_level=Toplevel()
# top_level.geometry('300x220')
_fram=Frame(top_level,)
_fram.grid(row=0,column=0,padx=10,sticky='nesw',pady=10)
top_level.columnconfigure(0,weight=1)
top_level.rowconfigure(0,weight=1)

id_var=StringVar(value=str(values[0]))
date_var=StringVar(value=values[1])
description_var=StringVar(value=values[3])
top_level.title(description_var.get())
old_price_var=StringVar(value=values[4])
new_price_var=StringVar(value=values[5])
supplier_var=StringVar(value=values[9])
invoice_var=StringVar(value=values[8])

barcode_var=StringVar(value='values[2]' )
_label=Label(_fram,text='Barcode')
_label.grid(row=0,column=0,sticky='w',padx=10,pady=10, )
entry=Entry(_fram,textvariable=barcode_var)
entry.grid(row=0,column=1,sticky='ew',pady=10)
_fram.columnconfigure(1,weight=1)

# self.get_input(label='Barcode',root=_fram,variable=barcode_var,row=2,lcol=0,icol=1,)
# self.get_input(label='Date',root=_fram,variable=date_var,row=1,lcol=0,icol=1, )
# self.get_input(label='Nome',root=_fram,variable=date_var,row=3,lcol=0,icol=1, )
# self.get_input(label='Barcode',root=_fram,variable=barcode_var,row=2,lcol=0,icol=1, )
# self.get_input(label='Description',root=_fram,variable=description_var,row=3,lcol=0,icol=1, )
# self.get_input(label='Old Price',root=_fram,variable=old_price_var,row=4,lcol=0,icol=1, )
# self.get_input(label='New Price',root=_fram,variable=new_price_var,row=5,lcol=0,icol=1, )
# self.get_input(label='Provider',root=_fram,variable=supplier_var,row=6,lcol=0,icol=1, )

_label=Label(_fram,text='Human')
_label.grid(row=6,column=0,sticky='w',padx=10,pady=10, )
entry=Entry(_fram,textvariable=description_var)
entry.grid(row=6,column=1,sticky='ew',pady=10)

_btn_update=Button(_fram,text='Actualizar')
_btn_update.grid(row=8, column=0, pady=10,sticky='e',padx=10)
_btn_delete=Button(_fram,text='Apagar')
_btn_delete.grid(row=8, column=1, pady=10,sticky='w')

product=Product (
            id=id_var.get(),
            description=description_var.get(),
            invoice=invoice_var.get(),
            newprice=new_price_var.get(),
            oldprice=old_price_var.get(),
            supplier=supplier_var.get(),
            code=barcode_var.get(),
            date=date_var.get(),
                )
_btn_update.bind('<Button-1>',lambda x:self.update_product(x,product))
_btn_delete.bind("<Button-1>",lambda x:self.delete_product(x,product))
self.input_edit_form(label='Entry By',root=_fram,variable=description_var,row=7,lcol=0,icol=1, )