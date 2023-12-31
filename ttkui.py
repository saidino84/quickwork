import os,re
from tkinter import StringVar, Tk, ttk,Toplevel
from tkinter.ttk import *
import sqlite3 as sq
from tkinter.filedialog import askopenfilename
from dataclasses import dataclass
from typing import List
from tkinter.messagebox import showinfo

@dataclass
class Product :
    id:int
    date:str 
    invoice:str 
    supplier:str
    code: str 
    description: str 
    oldprice:str 
    newprice:str 
    
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
    def show_table_data(self,tabela,category=None,search_v=None) :
        message=None
        if self.conn is not None:
            try:
                cursor =self.conn.cursor()
                if(search_v and category is not None):
                    try:
                        cursor.execute(f"SELECT * FROM {tabela} WHERE {category}='{search_v}';") 
                    except sq.Error as qlerror:
                        print("[SQLERROR] sqlerror")
                        message='ERROR'
                        # cursor.execute(f'SELECT * FROM {tabela} ;') 
                else:
                    cursor.execute(f'SELECT * FROM {tabela} ;') 
                dados=cursor.fetchall()
                print("Data feched ....")
                if len(dados)<1:
                    print('FETCHING AGAIN....')
                    cursor.execute(f'SELECT * FROM {tabela} ;') 
                    dados=cursor.fetchall()
                    message='ERROR: Dados nao encontrados !'
                
                cursor.close()
                return (message,dados)
            except sq.Error as e:
                print( '[ERROR in =[DbRepository().show_table_data(self,tabela,date=Non)] \n ERRO AO IMPRIMIR DADOS ERR:  ')
                return []
    def list_columns(self, table_name):
        if self.conn is not None:
            try:
                cursor=self.conn.cursor()
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns=cursor.fetchall()
                cursor.close()
                print(columns)
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
        print("[ UP ] TABELAS",tables)
        print(f'ID TO UPDATE TYPE :{type(product.id)}')
        if self.conn is not None:
            cursor=self.conn.cursor()
            update_stmt=  f''' UPDATE products SET date =   "{product.date}", 
            invoice={product.invoice}, oldprice={product.oldprice}, description = " {product.description} ",
            supplier = "{product.supplier}", 
            newprice={product.newprice}, code={product.code}  WHERE id={product.id[0]};'''
    
            print(f'UCTUALIZANDO PRODUCT ID: {product.id[0]}')
            print(update_stmt)
            try:
                st=cursor.execute(
                    update_stmt
                    )
            except sq.Error as e:
                print(f'ERROR COMMAND {e}')
            self.conn.commit()
            print(f'Product Updated...{cursor.rowcount} registros atualizados  ')
            cursor.close()

    def delete_product(self,prod_id):
        if self.conn is not None:
            cursor=self.conn.cursor()
            print(f'ID DELETANDO :{prod_id}')
            delete_stmt=f'''
            DELETE FROM products
            WHERE id = {prod_id};
            '''
            try:
                st=cursor.execute(
                    delete_stmt
                )
                self.conn.commit()
                print(f'delete suceeded :{st}')
            except sq.Error as e:
                print(f'ERROR DELETE COMMAND {e}')
            # commit data to file
            
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
        self.columns=('id',"date","barcode","description","old_cost","new_cost","difer","obs","invoice","provider",'user')
        _fram_seachbar=ttk.Frame(self)
        _fram_seachbar.grid(row=0,column=0,pady=10,sticky='ew',)
        self._label=ttk.Label(_fram_seachbar,text='Procurar',width=20)
        self._label.grid(row=0,column=0,sticky='ew',padx=10)
        self._input_search=ttk.Entry(_fram_seachbar, )
        self._input_search.grid(row=0,column=1,  padx=10,sticky='ew')
        
        self._sort_comboBox=ttk.Combobox(_fram_seachbar,values=list(x.capitalize() for x in ['invoice','oldprice','supplier','newprice','description','code','date']))
        self._sort_comboBox.grid(row=0,column=2,padx=10,sticky='ew')
        self._sort_comboBox.current(0)

        self._input_search.bind('<Return>', self.treeview_sort_product_by_column)
        # _fram_seachbar.rowconfigure(0,weight=1)
        _fram_seachbar.columnconfigure(1,weight=1)
        # _fram_seachbar.rowconfigure(0,weight=1)
        # _fram_seachbar.columnconfigure(0,weight=1)
        self.tree=Treeview(self,columns=self.columns, show='headings',
                    displaycolumns=[1,2,3,4,5,6,7,8,9 ])
        self.tree.grid(row=1,column=0,columnspan=4,padx=10,sticky='NSEW')
        self.rowconfigure(1,weight=1)
        self.columnconfigure(0,weight=1)
        self.tree.heading('#0',text='ID',)
        self.tree.heading('date',text='DATE')
        self.tree.heading('invoice',text='INVOICE')
        self.tree.heading('barcode',text='BARCODE')
        self.tree.heading("description",text="DESCRIPTION", )
        self.tree.heading("old_cost",text='OLD COST')
        self.tree.heading("new_cost",text='NEW COST')
        self.tree.heading('difer',text='DIFF')
        self.tree.heading('obs',text='OBS')
        self.tree.heading('provider',text='SUPPLIER')
        self.tree.heading('user',text='Entry By')
        
        # Configurar as larguras das colunas
        # tree.column("#0", width=10)
        # tree.column("description", width=100)
        self.tree.column('#0',width=5 )
        self.tree.column('date',width=5 )
        self.tree.column('invoice',width=5 )
        self.tree.column('barcode',width=10)
        self.tree.column("description",width=220 , )
        self.tree.column("old_cost",width=20 )
        self.tree.column("new_cost",width=20 )
        self.tree.column('difer',width=10 )
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
        
    def treeview_sort_product_by_column(self,event):
        search_value=self._input_search.get()
        category=self._sort_comboBox.get().lower()
        print(category," Has been chossen !")
        if category.__contains__('description'):
            print('NOT ALOWED CATEGORY')
            return self.deep_query_by_description(value=search_value)
        message,produts=self.repo.show_table_data(tabela='products',category=category,search_v=search_value)
        self.update_tree(products=produts)
        if message:
            showinfo(title='Falha Na Busca', message=message)
       
    def deep_query_by_description(self,value=None):
        products=[]
        message,self.products=message,self.products=self.repo.show_table_data('products')
        for product in self.products:
            found=re.search(value,product[5],re.IGNORECASE)
            if found is not None:
                products.append(product)
                print(product)
                self.update_tree(products=products)
        if len(products) <0:
            showinfo(title='Name Not Found',message='Produto Nao encontrado')
            # return self.pr
        return products
        

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
        top_level.geometry('480x360')
        centralizar_ajanela(top_level)
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
        def update_product( event):
            product=Product (
                        id=id_var.get(),
                        description=_entry.get(),
                        invoice=invoice.get(),
                        newprice=newprice.get(),
                        oldprice=oldprice.get(),
                        supplier=provider.get(),
                        code=code.get(),
                        date=date.get(),
                            )
            print(f'ID DO PRODUTO={product}')
            if self.repo.conn is not None:
                print('Connection Has stabished...')
                self.repo.update_product(product)
                print(f"aLLReady:{product.description}")
            else:
                print('connection not found...')
            print(product.description)
            self.preloaded_db(self.db)
            event.widget.master.master.destroy()
        
         
        def get_input( root,label,variable=None,row=0,lcol=0,icol=1):
            value=variable.get()
            print(f'GET INPUT CALLED->{label}={value}')
            _label=Label(root,text=label)
            _label.grid(row=row,column=lcol,sticky='w',padx=10,pady=10, )
            entry=Entry(root,)
            entry.grid(row=row,column=icol,sticky='ew',pady=10)
            entry.insert(0,value)
            root.columnconfigure(icol,weight=1)
            return entry
        
        code=get_input(label='Barcode',root=_fram,variable=barcode_var,row=2,lcol=0,icol=1,)
        date=get_input(label='Date',root=_fram,variable=date_var,row=1,lcol=0,icol=1, )
        # desc=get_input(label='Description',root=_fram,variable=description_var,row=3,lcol=0,icol=1, )
        oldprice=get_input(label='Old Price',root=_fram,variable=old_price_var,row=4,lcol=0,icol=1, )
        newprice=get_input(label='New Price',root=_fram,variable=new_price_var,row=5,lcol=0,icol=1, )
        provider=get_input(label='Provider',root=_fram,variable=supplier_var,row=6,lcol=0,icol=1, )
        invoice=get_input(label='Invoice',root=_fram,variable=invoice_var,row=7,lcol=0,icol=1, )
        
        _label=Label(_fram,text='Descricao')
        _label.grid(row=3,column=0,sticky='w',padx=10,pady=10, )
        _entry=Entry(_fram,width=200)
        _entry.grid(row=3,column=1,sticky='ew',pady=10,)
        _entry.insert(0,description_var.get())
        _fram.columnconfigure(1,weight=1)



        _btn_update=Button(_fram,text='Actualizar')
        _btn_update.grid(row=9, column=0, pady=10,sticky='e',padx=10)
        _btn_delete=Button(_fram,text='Apagar')
        _btn_delete.grid(row=9, column=1, pady=10,sticky='w')

        
        _btn_update.bind('<Button-1>',lambda x:update_product(x))
        _btn_delete.bind("<Button-1>",lambda x:self.delete_product(x,id_var.get()))
        
        top_level.wait_window()
         
        
    def delete_product(self,event,id):
        if self.repo.conn is not None:
            print('Connection Has stabished...')
            self.repo.delete_product(id)
        else:
            print('connection not found...')
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
        data=[]
        try:
            message,self.products=self.repo.show_table_data('products')
        except Exception as e:
            return
        self.tree.delete(*self.tree.get_children())
        for product in self.products:
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
                provider=product[3]
            except IndexError as e:
                id=product[0]
                barcode=product[2]
                descriptio=product[1]
                old_cost=product[3]
                new_cost=product[4]
                date=product[5]
                invoice=product[6]
                provider='Vip Armazem Muxara'
            differ=round(float(new_cost)-float(old_cost))
            obs='SUBIU' if differ>0 else 'BAIXOU'
            
            
            
            _tag='increased' if obs.endswith('SUBIU') else tag
            prod=(id,date,barcode,descriptio,old_cost,new_cost,differ,obs,invoice,provider)
          
            self.tree.insert('', 'end', values=prod, tags=(_tag,tag))
            self.tree.tag_configure('impar', background= '#e6e8e6',  ) #if light
            # self.tree.tag_configure('impar', background= '#242423', ) #if dark

            # self.tree.tag_configure('par', background= "#D4F1DD",font=("Calibri", 11, "bold"))
            self.tree.tag_configure('increased',foreground= "#EE2A08",font=("Calibri", 11, "bold"))

    def load_file(self,event):
        
        self.repo=DbRepository()
        if self.repo.conn is not None:
            self.repo.close_connection()
            
        self.db=askopenfilename(title='Select File',filetypes=[("Database Files", "*.db")])
        self.repo.connect_db(self.db)
        self._label_file_res.config(text=self.db)
        rows=self.repo.list_tables()
        print(f'TABLES LOADES ARE : {rows}')
        message,self.products=self.repo.show_table_data(rows[0][0])
        self.tree.delete(*self.tree.get_children())
        for product in self.products:
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
    def update_tree(self,products):
        self.products=products
        if self.repo is None:
            print('NO CONNECTION FOUND')
            return
        print(f"[COLUMNS]=>{self.repo.list_columns('products')}")
        self.tree.delete(*self.tree.get_children())
        for product in  self.products:
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



def centralizar_ajanela(root):
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
def main(path=None):
    _root=Tk()
    _root.title('Product Price Control')
     # Simply set the theme
    # _root.tk.call("source", "azure.tcl")
    # _root.tk.call("set_theme", "light")
    # Create a style
    style = ttk.Style(_root)
    _root.update()
    # Import the tcl file
    _root.tk.call("source", "forest-dark.tcl")
    _root.tk.call("source", "forest-light.tcl")
    # Set the theme with the theme_use method
    style.theme_use("forest-light")
    _root.geometry('750x400')
    centralizar_ajanela(_root)
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