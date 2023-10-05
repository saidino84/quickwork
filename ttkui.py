import os
from tkinter import StringVar, Tk, ttk,Toplevel
from tkinter.ttk import *
import sqlite3 as sq
from tkinter.filedialog import askopenfilename
class Product :
    __tablename__='products'
    id:int
    date:str 
    invoice:str 
    supplier:str
    code: str 
    description: str 
    oldprice:str 
    newprice:str 
    def __init__(self,id, description,invoice,newprice,oldprice,supplier,code,date):
        self.date=date
        self.id=id,
        self.invoice=invoice
        self.supplier=supplier
        self.code=code
        self.description = description
        self.oldprice=oldprice
        self.newprice=newprice
    def __repr__(self) -> str:
        return f"""'id:'{self.id},'Name:',Id{self.description}"""
class DbRepository:
    def __init__(self,) -> None:
        self.conn=None
    
    def connect_db(self,file):
        try:
            self.conn=sq.connect(file)
            print('Connect has stabilished')
        except sq.Error as e:
            print(f'Connection Failed: {e}')
    def list_tables(self):
        if self.conn is not None:
            try:
                cursor=self.conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables=cursor.fetchall()
                cursor.close()
                return tables
            except sq.Error as e:
                print(f'ERRO AO ENCONTRAR TABELAS {e}')
        else:
            print('[+] PLEASE CONENCT FIRSR OF ALL')  
    def show_table_data(self,tabela,data=None):
        if self.conn is not None:
            try:
                cursor =self.conn.cursor()
                if(data is not None):
                    cursor.execute(f'SELECT * FROM {tabela} WHERE date="29/09/2023";') 
                else:
                    cursor.execute(f'SELECT * FROM {tabela} ;') 
                dados=cursor.fetchall()
                print("Data feched ....")
                
                cursor.close()
                return dados
            except sq.Error as e:
                print('ERRO AO IMPRIMIR DADOS')
    def list_columns(self, table_name):
        if self.conn is not None:
            try:
                cursor=self.conn.cursor()
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns=cursor.fetchall()
                cursor.close()
                return columns
            except sq.Error as e:
                print(f'ERRO AO ENCONTRAR COLUNAS {e}')
        else:
            print('[+] PLEASE CONENCT FIRST OF ALL')
    def exec_sql_command(self,sql):
        if self.conn:
            try:
                cursor=self.conn.cursor()
                cursor.execute(sql)
                cursor.fetchall()
                cursor.close()
            except sq.Error as e:
                print(f'ERROR COMMAND {e}')
        else:
            print('[X] no connection found !')
    def close_connection(self):
    
        if self.conn is not None:
            self.conn.close()
            print('[+] CONNECTION CLOSED')
        else:
            print('[+] PLEASE CONENCT FIRST')
    def update_product(self,product:Product):
        tables=self.list_tables()
        print("TABELAS",tables)
        print(f'ID TO UPDATE TYPE :{type(product.id)}')
        if self.conn is not None:
            cursor=self.conn.cursor()
            update_stmt=  f""" UPDATE products SET date={product.date}, 
            invoice={product.invoice}, oldprice={product.oldprice}, 
            newprice={product.newprice}, code={product.code}  WHERE id={product.id[0]};"""
    
            print(f'UCTUALIZANDO PRODUCT ID: {product.id[0]}')
            print(update_stmt)
            st=cursor.execute(
                update_stmt
                )
            
            self.conn.commit()
            print(f'Product Updated...{cursor.rowcount} registros atualizados  ')
            cursor.close()

    def delete_product(self,product:Product):
        if self.conn is not None:
            cursor=self.conn.cursor()
            print(f'ID DELETANDO :{product.id}')
            delete_stmt='''
            DELETE FROM products
            WHERE id = ?;
            '''
            st=cursor.execute(
                delete_stmt,
                product.id,
            )
            # commit data to file
            self.conn.commit()
            print(f'delete suceeded :{st}')
            
            cursor.close()
    def insert_product(self,product:Product):
        if self.conn is not None:
            cursor=self.cursor()
class AppUi(ttk.Frame):
    def __init__(self,master=None,db=None ,**args):
        super().__init__(master,**args )
        self.db=db
        self.pack(fill='both',expand=True)
        # self.sql_command_var=StringVar()
        self._sqlres=StringVar(value='Comand not found')
        self.init_components()
        if self.db is not None:
            print('DB FILE LOADED')
            self.preloaded_db(db)
        else:
            print('DB FILE NOT FOUND')

    def init_components(self):
        _fram_seachbar=ttk.Frame(self)
        _fram_seachbar.grid(row=0,column=0,pady=10,sticky='ew',)
        self._label=ttk.Label(_fram_seachbar,text='Procurar',width=20)
        self._label.grid(row=0,column=0,sticky='ew',padx=10)
        self._input_search=ttk.Entry(_fram_seachbar, )
        self._input_search.grid(row=0,column=1,  padx=10,sticky='ew')
        
        # _fram_seachbar.rowconfigure(0,weight=1)
        _fram_seachbar.columnconfigure(1,weight=1)
        # _fram_seachbar.rowconfigure(0,weight=1)
        # _fram_seachbar.columnconfigure(0,weight=1)
        self.columns=('id',"date","barcode","description","old_cost","new_cost","difer","obs","invoice","provider",'user')
        self.tree=Treeview(self,columns=self.columns,show='headings',
                    displaycolumns=[1,2,3,4,5,6,7,8,9 ])
        self.tree.grid(row=1,column=0,columnspan=4,padx=10,sticky='NSEW')
        self.rowconfigure(1,weight=1)
        self.columnconfigure(0,weight=1)
        self.tree.heading('#0',text='id',)
        self.tree.heading('date',text='Date')
        self.tree.heading('invoice',text='Invoice')
        self.tree.heading('barcode',text='Barcode')
        self.tree.heading("description",text="Description", )
        self.tree.heading("old_cost",text='old cost')
        self.tree.heading("new_cost",text='New cost')
        self.tree.heading('difer',text='Difer')
        self.tree.heading('obs',text='Obs')
        self.tree.heading('provider',text='Provider')
        self.tree.heading('user',text='Entry By')
        
        # Configurar as larguras das colunas
        # tree.column("#0", width=10)
        # tree.column("description", width=100)
        self.tree.column('#0', )
        self.tree.column('date',width=5 )
        self.tree.column('invoice',width=5 )
        self.tree.column('barcode',width=10)
        self.tree.column("description",width=200 , )
        self.tree.column("old_cost",width=10 )
        self.tree.column("new_cost",width=10 )
        self.tree.column('difer',width=5 )
        self.tree.column('obs', width=5)
        self.tree.column('provider',width=10 )
        self.tree.column('user',width=5 )

        # SCROLLBARS FOR TREEVIW
        scroll_x=ttk.Scrollbar(self,orient='horizontal',command=self.tree.xview)
        scroll_x.grid(row=2,column=0,sticky='we',columnspan=4,padx=10,)

        scroll_y=ttk.Scrollbar(self,orient='vertical',command=self.tree.yview)
        scroll_y.grid(row=1,column=2,sticky='ns',rowspan=2,padx=10,)
        self.tree.configure(yscrollcommand=scroll_y.set)
        self.tree.configure(xscrollcommand=scroll_x.set)


         
        # Eventos do treeview
        # self.tree.bind("<<TreeviewSelect>>",self.open_popup_editor)
        self.tree.bind("<Double-1>",self.open_popup_editor)

        # Frame de botao de load e text res
        _btn_frame=ttk.Frame(self)
        _btn_frame.grid(row=3,column=0,sticky='ew',pady=10)
        self.btn_save=Button(_btn_frame,text='Load File',width=20)
        self.btn_save.grid(row=0,column=0,sticky='w',padx=10, )
        self.btn_save.bind('<Button-1>',self.load_file)
        
        
        self.btn_extract=Button(_btn_frame,text='Extract',width=20)
        self.btn_extract.grid(row=0,column=1,sticky='e',padx=10)
        # self.btn_extract.bind('<Button-1>',self.extract_data)
        _btn_frame.columnconfigure(1,weight=1)
        # Label for db/res
        self._label_file_res=ttk.Label(self,text='file not Loaded',padding=20)
        self._label_file_res.grid(row=4,sticky='ew', )


    def open_popup_editor(self,event):
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
    
        id_var=StringVar(value=values[0])
        date_var=StringVar(value=values[1])
        description_var=StringVar(value=values[3])
        top_level.title(description_var.get())
        old_price_var=StringVar(value=values[4])
        new_price_var=StringVar(value=values[5])
        supplier_var=StringVar(value=values[9])
        invoice_var=StringVar(value=values[8])
        
        barcode_var=StringVar(value=values[2] )
         
        def get_input( root,label,variable=None,row=0,lcol=0,icol=1):
            print(f'GET INPUT CALLED->{label}={variable.get()}')
            _label=Label(root,text=label)
            _label.grid(row=row,column=lcol,sticky='w',padx=10,pady=10, )
            entry=Entry(root,textvariable=variable)
            entry.grid(row=row,column=icol,sticky='ew',pady=10)
            root.columnconfigure(icol,weight=1)
            return entry
        
        get_input(label='Barcode',root=_fram,variable=barcode_var,row=2,lcol=0,icol=1,)
        get_input(label='Date',root=_fram,variable=date_var,row=1,lcol=0,icol=1, )
        get_input(label='Description',root=_fram,variable=description_var,row=3,lcol=0,icol=1, )
        get_input(label='Old Price',root=_fram,variable=old_price_var,row=4,lcol=0,icol=1, )
        get_input(label='New Price',root=_fram,variable=new_price_var,row=5,lcol=0,icol=1, )
        get_input(label='Provider',root=_fram,variable=supplier_var,row=6,lcol=0,icol=1, )



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
        
        top_level.wait_window()
         
    def update_product(self,event,product:Product):
        print(f'ID DO PRODUTO={type(product.oldprice)}')
        if self.repo.conn is not None:
            print('Connection Has stabished...')
            self.repo.update_product(product)
            print(f"Ready:{product.description}")
        else:
            print('connection not found...')
        print(product.description)
        self.preloaded_db(self.db)
        event.widget.master.master.destroy()
    def delete_product(self,event,product:Product):
        if self.repo.conn is not None:
            print('Connection Has stabished...')
            self.repo.delete_product(product)
        else:
            print('connection not found...')
        print(f"Deleted :{product.description}")
        self.preloaded_db(self.db)
        event.widget.master.master.destroy()

     
    

    def preloaded_db(self,path):
        self.repo=DbRepository()
        self.db=path
        print(f'DB FILE FOUND ...{self.db}')
        self.repo.connect_db(self.db)
        self._label_file_res.config(text=self.db)
        rows=self.repo.list_tables()
        print(rows)
        data=self.repo.show_table_data(rows[0][0])
        self.tree.delete(*self.tree.get_children())
        for product in data:
            print(product)
            tag='impar' if product[0]%2==0 else 'par'
            id=product[0]
            barcode= None
            descriptio=None
            old_cost=0
            new_cost=0
            try:
                id=product[0]
                barcode=product[4]
                descriptio=product[5]
                old_cost=product[6]
                new_cost=product[7]
                date=product[1]
                invoice=product[2]
            except IndexError as e:
                id=product[0]
                barcode=product[2]
                descriptio=product[1]
                old_cost=product[3]
                new_cost=product[4]
                date=product[5]
                invoice=product[6]
            differ=round(float(new_cost)-float(old_cost))
            obs='SUBIU' if differ>0 else 'BAIXOU'
            provider='Vip Armazem Muxara'
            
            
            _tag='increased' if obs.endswith('SUBIU') else tag
            prod=(id,date,barcode,descriptio,old_cost,new_cost,differ,obs,invoice,provider)
          
            self.tree.insert('', 'end', values=prod, tags=(_tag,tag))
            self.tree.tag_configure('impar', background= '#ffffff',font=("Calibri", 11, "bold"))
            self.tree.tag_configure('par', background= "#D4F1DD",font=("Calibri", 11, "bold"))
            self.tree.tag_configure('increased',foreground= "#EE2A08",font=("Calibri", 11, "bold"))

    def load_file(self,event):
        
        self.repo=DbRepository()
        if self.repo.conn is not None:
            self.repo.close_connection()
            
        self.db=askopenfilename(title='Select File',filetypes=[("Database Files", "*.db")])
        self.repo.connect_db(self.db)
        self._label_file_res.config(text=file)
        rows=self.repo.list_tables()
        data=self.repo.show_table_data(rows[0][0])
        self.tree.delete(*self.tree.get_children())
        for product in data:
            # print(product)
            tag='impar' if product[0]%2==0 else 'par'
            id=product[0]
            barcode= None
            descriptio=None
            old_cost=0
            new_cost=0
            try:
                id=product[0]
                barcode=product[4]
                descriptio=product[5]
                old_cost=product[6]
                new_cost=product[7]
                date=product[1]
                invoice=product[2]
            except IndexError as e:
                id=product[0]
                barcode=product[2]
                descriptio=product[1]
                old_cost=product[3]
                new_cost=product[4]
                date=product[5]
                invoice=product[6]
            differ=round(float(new_cost)-float(old_cost))
            obs='SUBIU' if differ>0 else 'BAIXOU'
            provider='Vip Armazem Muxara'
            
            
            _tag='increased' if obs.endswith('SUBIU') else tag
            prod=(id,date,barcode,descriptio,old_cost,new_cost,differ,obs,invoice,provider)
          
            self.tree.insert('', 'end', values=prod, tags=(_tag,tag))
            self.tree.tag_configure('impar', background= '#ffffff',font=("Calibri", 11, "bold"))
            self.tree.tag_configure('par', background= "#D4F1DD",font=("Calibri", 11, "bold"))
            self.tree.tag_configure('increased',foreground= "#EE2A08",font=("Calibri", 11, "bold"))

def main(path=None):
    _root=Tk()
    _root.title('Product Price Control')
    _root.geometry('750x400')
    ui=AppUi(_root,db=path)
    ui.pack()
    _root.mainloop()
if __name__=='__main__':
    files=os.listdir(".")
    db=None
    for file in files:
        if file.endswith('db.db'):
            db=file
    main(path=db)