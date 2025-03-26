from tkinter import *
from tkinter import ttk
from tkinter import Canvas
from tkinter import messagebox
import pyodbc
from motorista import *



class Onibus(Toplevel):
    
    cor_white = '#edf6f9'
    cor_fundo = '#b6e0f8'
    
    def __init__(self, original):
        self.frame_original = original
        self.tela4()
        self.frames_tela()
        self.grid_bus()
        self.widgets_frame1()
        self.Menus()
        self.select_lista()
        self.buscar_bus()

    def tela4(self):
        Toplevel.__init__(self)
        self.config(cursor="target")
        self.title("Tela Ônibus")
        self.configure(background='black')
        self.iconbitmap('imagens/umbrella.ico')
        self.geometry("1280x720")
        self.resizable(True, True)
        self.maxsize(width=1280, height=720)
        self.minsize(width=400, height=300)


    def limpar_campos(self):
        self.entry_num_placa.delete(0, END)
        self.entry_num_linha.delete(0, END)
        self.entry_mod_bus.delete(0, END)
        self.entry_ano_fab.delete(0, END)
        
        
        
    def db_conect(self):
        driver = '{ODBC Driver 17 for SQL Server}'
        server = 'sql-estudo.database.windows.net'
        database = 'db-estudos'
        username = 'geovani.pereira@blueshift.com.br'
        Authentication = 'ActiveDirectoryInteractive'
        port = '1433'
        self.conexao = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';AUTHENTICATION=' +
                                Authentication+';PORT='+port+';DATABASE='+database+';UID='+username)
        
        self.cursor = self.conexao.cursor()
        print("conectando ao banco de dados")
        
    def db_desconect(self):
        self.conexao.close();print("Desconectando ao banco de dados sqlite3")
        
    
        
    def capturar_campos(self):
        self.num_placa = self.entry_num_placa.get()
        self.num_linha = self.entry_num_linha.get()
        self.mod_bus = self.entry_mod_bus.get()
        self.ano_fab = self.entry_ano_fab.get()
        
        
    def add_bus(self):
        #obter dados dos campos
        self.capturar_campos()
        if self.entry_num_placa.get() == "":
            msg = "Para cadastrar novo ÔNIBUS é necessário \n"
            msg += "preencher o campo NÚMERO DA PLACA"
            messagebox.showinfo("Cadastro ÔNIBUS >> Aviso!!!", msg)
        elif self.entry_num_linha.get() == "":
            msg = "Para cadastrar novo ÔNIBUS é necessário \n"
            msg += "preencher o campo NÚMERO DA LINHA"
            messagebox.showinfo("Cadastro ÔNIBUSs >> Aviso!!!", msg)
        elif self.entry_mod_bus.get() == "":
            msg = "Para cadastrar novo ÔNIBUS é necessário \n"
            msg += "preencher o campo MODELO DO ÔNIBUS"
            messagebox.showinfo("Cadastro ÔNIBUS >> Aviso!!!", msg)
        elif self.entry_ano_fab.get() == "":
            msg = "Para cadastrar novo ÔNIBUS é necessário \n"
            msg += "preencher o campo ANO DE FABRICAÇÃO"
            messagebox.showinfo("Cadastro ÔNIBUS >> Aviso!!!", msg)
        else:
            self.db_conect()
            self.cursor.execute("""INSERT INTO geovani_martins_pereira.onibus (num_placa, num_linha, mod_bus, ano_fab) 
            VALUES(?,?,?,?)""",(self.num_placa,self.num_linha,self.mod_bus,self.ano_fab))
            self.conexao.commit()
            self.db_desconect()
            self.select_lista()
            self.limpar_campos()
        
    def select_lista(self):
        self.lista_grid.delete(*self.lista_grid.get_children())
        self.db_conect()
        lista = self.cursor.execute("""SELECT  id_motorista, num_placa, num_linha, mod_bus, ano_fab
        FROM geovani_martins_pereira.onibus ORDER BY id_motorista ASC;""")
        for l in lista:
            self.lista_grid.insert("",END,values=l)
        self.db_desconect()
        
    def buscar_bus(self):
        self.db_conect()
        self.lista_grid.delete(*self.lista_grid.get_children())
        
        self.entry_num_placa.insert(END, '%')
        num_placa = self.entry_num_placa.get()
        self.cursor.execute(
            """ SELECT id_motorista, num_placa, num_linha, mod_bus, ano_fab  FROM geovani_martins_pereira.onibus
            WHERE num_placa LIKE '%s' ORDER BY id_motorista ASC""" % num_placa)
        buscanome = self.cursor.fetchall()
        for i in buscanome:
            self.lista_grid.insert("", END, values=i)
        self.limpar_campos()
        self.db_desconect()
        
        
    def OnDubleClick(self, event):
        self.limpar_campos()
        self.lista_grid.selection()

        for x in self.lista_grid.selection():
            col1,col2,col3,col4 = self.lista_grid.item(x,'values')
            self.entry_num_placa.insert(END, col1)
            self.entry_num_linha.insert(END, col2)
            self.entry_mod_bus.insert(END, col3)
            self.entry_ano_fab.insert(END, col4)
      
            
            

    def deleta_bus(self):
        self.capturar_campos()
        self.db_conect()
        self.cursor.execute("""DELETE FROM geovani_martins_pereira.onibus WHERE id_motorista = ?""",(self.id_motorista))
        self.conexao.commit()
        self.db_desconect()
        self.limpar_campos()
        self.select_lista()

    def alterar_bus(self):
        self.capturar_campos()
        self.db_conect()
        self.cursor.execute("""UPDATE geovani_martins_pereira.onibus SET num_placa=?, num_linha=?, mod_bus=?, ano_fab = ?
        WHERE id_motorista = ?;
        """,(self.num_placa, self.num_linha,self.mod_bus,self.ano_fab,self.id_motorista))
        self.conexao.commit()
        self.db_desconect()
        self.limpar_campos()
        self.select_lista()


    def frames_tela(self):
        self.frame1 = Frame(self, bd=4, bg="#962129",
                            highlightbackground="black", highlightthickness=3)
        self.frame1.place(relx=0.02, rely=0.01, relwidth=0.96, relheight=0.46)

        self.frame2 = Frame(self, bd=4, bg="#dfe3ee",
                            highlightbackground='#759fe6', highlightthickness=3)
        self.frame2.place(relx=0.1, rely=0.48, relwidth=0.80, relheight=0.46)


    def widgets_frame1(self):
        self.canvas_bt = Canvas(self.frame1, bd=1, bg='#062617', highlightbackground='black',
                     highlightthickness=3)
        self.canvas_bt.place(relx=0.24, rely=0.08, relwidth=0.27, relheight=0.19)
        
        self.canvas_bt2 = Canvas(self.frame1, bd=1, bg='#062617', highlightbackground='black',
                     highlightthickness=3)
        self.canvas_bt2.place(relx=0.57, rely=0.08, relwidth=0.34, relheight=0.19)
        
        self.modelo  = PhotoImage(file='imagens/bustela.png')
        self.img1 = Label(self.frame1, image=self.modelo, bd=0, highlightbackground="black", highlightthickness=1)
        self.img1.place(relx=0.010, rely=0.050)
  
        self.modelo2  = PhotoImage(file='imagens/umbrela.png')
        self.img2 = Label(self, image=self.modelo2, bd=0, highlightbackground="black", highlightthickness=1)
        self.img2.place(relx=0.01, rely=0.65)
        
        self.modelo3  = PhotoImage(file='imagens/umbrela.png')
        self.img3 = Label(self, image=self.modelo3, bd=0, highlightbackground="black", highlightthickness=1)
        self.img3.place(relx=0.90, rely=0.65)
        
        # botão limpar
        self.bt_limpar = Button(self.frame1, text="Limpar campos", bd=6, 
                                bg="#062617", fg="#9e0b13", activebackground='red', activeforeground="yellow", font=('segoe print', 12, 'bold'), command=self.limpar_campos)
        self.bt_limpar.place(relx=0.25, rely=0.1, relwidth=0.12, relheight=0.15)
        
        self.bt_buscar = Button(self.frame1, text="Buscar placa", bd=6, 
                                bg="#062617", fg="#9e0b13", activebackground='red', activeforeground="yellow", font=('segoe print', 12, 'bold'), command=self.buscar_bus)
        self.bt_buscar.place(relx=0.38, rely=0.1, relwidth=0.12, relheight=0.15)
        
        # botão Novo
        self.bt_novo = Button(self.frame1, text="Inserir", bd=6, 
                                bg="#062617", fg="#9e0b13", font=('segoe print', 12, 'bold'),command=self.add_bus)
        self.bt_novo.place(relx=0.58, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão Altera
        self.bt_alterar = Button(self.frame1, text="Alterar", bd=6, 
                                bg="#062617", fg="#9e0b13", font=('segoe print', 12, 'bold'),command=self.alterar_bus)
        self.bt_alterar.place(relx=0.69, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão Apagar
        self.bt_apagar = Button(self.frame1, text="Apagar", bd=6, 
                               bg="#062617", fg="#9e0b13", font=('segoe print', 12, 'bold'),command=self.deleta_bus)
        self.bt_apagar.place(relx=0.80, rely=0.1, relwidth=0.1, relheight=0.15)

        # label e entry - codigo -----------------------------
    
        
        

        self.lb_num_placa = Label(self.frame1, text="*Número da placa:",
                            bg="#962129", fg="black", font=('segoe print', 12, 'bold'))
        self.lb_num_placa.place(relx=0.30, rely=0.30)

        self.entry_num_placa = Entry(self.frame1,
                                bg="#212021", fg="white", font=('segoe print', 12, 'bold'))
        self.entry_num_placa.place(relx=0.30, rely=0.40, relwidth=0.10)

        self.lb_num_linha = Label(self.frame1, text="*Número da linha:",
                            bg="#962129", fg="black", font=('segoe print', 12, 'bold'))
        self.lb_num_linha.place(relx=0.45, rely=0.30)

        self.entry_num_linha = Entry(self.frame1,
                               bg="#212021", fg="white", font=('segoe print', 12, 'bold'))
        self.entry_num_linha.place(relx=0.45, rely=0.40, relwidth=0.07)

        # label e entry - nome ----------------------------------
        self.lb_mod_bus = Label(self.frame1, text="*Modelo Ônibus:",
                            bg="#962129", fg="black", font=('segoe print', 12,'bold'))
        self.lb_mod_bus.place(relx=0.17, rely=0.60)

        self.entry_mod_bus = Entry(self.frame1,
                               bg="#212021", fg="white", font=('segoe print', 12,'bold'))
        self.entry_mod_bus.place(relx=0.17, rely=0.70, relwidth=0.50)

        self.lb_ano_fab = Label(self.frame1, text="*Ano de fabricação:",
                            bg="#962129", fg="black", font=('segoe print', 12, 'bold'))
        self.lb_ano_fab.place(relx=0.77, rely=0.60)

        self.entry_ano_fab = Entry(self.frame1,
                               bg="#212021", fg="white", font=('segoe print', 12, 'bold'))
        self.entry_ano_fab.place(relx=0.77, rely=0.70, relwidth=0.06)
        
        self.btn = Button(
            self,
            bd=6,
            text='Voltar',
            bg=self.cor_fundo,
            activebackground=self.cor_white,
            font=('segoe print', 12, 'bold'),
            fg="black",
            activeforeground=self.cor_fundo,
            command=self.onClose)
        self.btn.pack()
        self.btn.place(
            relx=0.005,
            rely=0.95,
            relwidth=0.07,
            relheight=0.05
            )

    
    def grid_bus(self):
        self.lista_grid = ttk.Treeview(self.frame2, height=3,
                                    column=('col1', 'col2', 'col3', 'col4','col5'))
        self.lista_grid.heading("#0", text='')  
        self.lista_grid.heading("#1", text='ID MOTORISTA')                            
        self.lista_grid.heading("#2", text='Nº DA PLACA')
        self.lista_grid.heading("#3", text='Nº LINHA ÔNIBUS')
        self.lista_grid.heading("#4", text='MODELO DO ÔNIBUS')
        self.lista_grid.heading("#5", text='ANO DE FABRICAÇÃO')
        



        self.lista_grid.column("#0", width=80)
        self.lista_grid.column("#1", width=100)
        self.lista_grid.column("#2", width=125)
        self.lista_grid.column("#3", width=150)
        self.lista_grid.column("#4", width=130)
        self.lista_grid.column("#5", width=100)
        self.lista_grid.place(relx=0.01, rely=0.06, relwidth=0.97, relheight=0.86)

        self.scrol_lista = Scrollbar(self.frame2, orient='vertical')
        self.lista_grid.configure(yscroll=self.scrol_lista.set)
        self.scrol_lista.place(relx=0.98, rely=0.05, relwidth=0.02, relheight=0.89)
        self.lista_grid.bind("<Double-1>",self.OnDubleClick)

    def Menus(self):
        Menubar = Menu(self)
        self.config(menu=Menubar)
        filemenu = Menu(Menubar)
        

        def Quit(): self.destroy()

        Menubar.add_cascade(label="opções",menu=filemenu)
        

        filemenu.add_command(label="Sair sistema",command=Quit)
        
    def onClose(self):
        self.destroy()
        self.frame_original.show()
            


   