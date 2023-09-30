from tkinter import Tk, ttk
from tkinter.ttk import *
import sqlite3 as sq
from tkinter.filedialog import askopenfilename

class DbRepository:
    def __init__(self) -> None:
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
                    cursor.execute(f'SELECT * FROM {tabela} WHERE date="29/09/2023"') 
                else:
                    cursor.execute(f'SELECT * FROM {tabela} ') 
                dados=cursor.fetchall()
                print("Data feched ....")
                print(dados[0])
                cursor.close()
                return dados
            except sq.Error as e:
                print('ERRO AO IMPRIMIR DADOS')

    def close_connection(self,file_path):
        if self.conn is not None:
            self.conn.close()
            print('[+] CONNECTION CLOSED')
        else:
            print('[+] PLEASE CONENCT FIRST')
class AppUi(ttk.Frame):
    def __init__(self,master=None, **args):
        super().__init__(master,**args )

        # self_mframe=ttk.Frame(root)
        # _mframe.pack(fill='both',expand=True)
        self.pack(fill='both',expand=True)
        self.init_components()

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
        columns=('id',"date","barcode","description","old_cost","new_cost","difer","obs","invoice","provider",'user')
        self.tree=Treeview(self,columns=columns,show='headings',
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
        self.tree.bind("<<TreeviewSelect>>", lambda event: self.tree.edit_modified(True))
        self.tree.bind("<Double-1>", lambda event: self.tree.edit_modified(False))

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
         

    def load_file(self,event):
        repo=DbRepository()
        file=askopenfilename(title='Select File',filetypes=[("Database Files", "*.db")])
        repo.connect_db(file)
        self._label_file_res.config(text=file)
        rows=repo.list_tables()
        print(rows)
        data=repo.show_table_data(rows[0][0])
        self.tree.delete(*self.tree.get_children())
        for product in data:
            tag='impar' if product[0]%2==0 else 'par'
            id=product[0]
            barcode=product[2]
            descriptio=product[1]
            old_cost=product[3]
            new_cost=product[4]
            differ=round(float(old_cost)-float(new_cost))
            obs='BAIXOU' if differ<0 else 'SUBIU'
            provider='Vip Armazem Muxara'
            date=product[5]
            invoice=product[6]
            _tag='increased' if obs.endswith('SUBIU') else tag
            prod=(id,date,barcode,descriptio,old_cost,new_cost,differ,obs,invoice,provider)
          
            self.tree.insert('', 'end', values=prod, tags=(_tag,tag))
            self.tree.tag_configure('impar', background= '#ffffff',font=("Calibri", 11, "bold"))
            self.tree.tag_configure('par', background= "#D4F1DD",font=("Calibri", 11, "bold"))
            self.tree.tag_configure('increased',foreground= "#EE2A08",font=("Calibri", 11, "bold"))

def main():
    _root=Tk()
    _root.title('Product Price Control')
    _root.geometry('750x400')
    ui=AppUi(_root)
    ui.pack()
    _root.mainloop()
if __name__=='__main__':
    main()