from tkinter import *
from tkinter import ttk
import sqlite3
from tkcalendar import DateEntry
from tkinter import messagebox





class Cartoes(Toplevel):
    cor_white = '#edf6f9'
    cor_fundo = '#b6e0f8'
    
    def __init__(self, original):
        self.frame_original = original
        self.tela5()
        self.frames_tela()
        self.grid_cartao()
        self.widgets_frame1()
        self.Menus()
        self.criar_tabela()
        self.select_lista()
        self.buscar_cartao()

    def tela5(self):
        Toplevel.__init__(self)
        self.config(cursor="target")
        self.title("Tela Cartão")
        self.configure(background='black')
        self.iconbitmap('imagens/umbrella.ico')
        self.geometry("1280x720")
        self.resizable(True, True)
        self.maxsize(width=1280, height=720)
        self.minsize(width=400, height=300)


    def limpar_campos(self): 
        self.entry_id_cartao.delete(0, END)
        self.entry_id_proprietario.delete(0, END)
        self.entry_qtde_credito.delete(0, END)
        self.entry_tipo_cartao.delete(0, END)
        self.entry_data_emissao.delete(0, END)
        
    def db_conect(self):
        self.conexao = sqlite3.connect('BDCadUni.db')
        self.cursor = self.conexao.cursor()
        print("conectando ao banco de dados")
        
    def db_desconect(self):
        self.conexao.close();print("Desconectando ao banco de dados")
        
   
    def capturar_campos(self):
        self.id_cartao = self.entry_id_cartao.get()
        self.id_proprietario = self.entry_id_proprietario.get()
        self.qtde_credito = self.entry_qtde_credito.get()
        self.tipo_cartao = self.entry_tipo_cartao.get()
        self.data_emissao = self.entry_data_emissao.get_date()
    def add_cartao(self):
        #obter dados dos campos
        self.capturar_campos()
        if self.entry_id_cartao.get() == "":
            msg = "Para cadastrar novo CARTÃO é necessário \n"
            msg += "preencher o campo ID DO CARTÃO"
            messagebox.showinfo("Cadastro CARTÃO >> Aviso!!!", msg)
        elif self.entry_id_proprietario.get() == "":
            msg = "Para cadastrar novo Usuário é necessário \n"
            msg += "preencher o campo ID DO PROPRIETÁRIO"
            messagebox.showinfo("Cadastro CARTÃO >> Aviso!!!", msg)
        elif self.entry_qtde_credito.get() == "":
            msg = "Para cadastrar novo CARTÃO é necessário \n"
            msg += "preencher o campo QUANTIDADE DE CRÉDITO (R$)"
            messagebox.showinfo("Cadastro CARTÃOs >> Aviso!!!", msg)
        elif self.entry_tipo_cartao.get() == "":
            msg = "Para cadastrar novo CARTÃO é necessário \n"
            msg += "preencher o campo TIPO DO CARTÃO"
            messagebox.showinfo("Cadastro CARTÃO >> Aviso!!!", msg)
        else:
            self.db_conect()
            self.cursor.execute("""INSERT INTO geovani_martins_pereira.cartoes (id_cartao, qtde_credito, tipo_cartao, data_emissao) 
            VALUES(?,?,?,?)""",(self.id_cartao, self.qtde_credito, self.tipo_cartao, self.data_emissao))
            self.conexao.commit()
            self.db_desconect()
            self.select_lista()
        self.limpar_campos()
        
    def select_lista(self):
        self.lista_grid.delete(*self.lista_grid.get_children())
        self.db_conect()
        lista = self.cursor.execute("""SELECT id_cartao, id_proprietario, qtde_credito, tipo_cartao, data_emissao
        FROM geovani_martins_pereira.cartoes ORDER BY id_proprietario ASC;""")
        for l in lista:
            self.lista_grid.insert("",END,values=l)
        self.db_desconect()
        
    def buscar_cartao(self):
        self.db_conect()
        self.lista_grid.delete(*self.lista_grid.get_children())
        
        self.entry_id_proprietario.insert(END, '%')
        id_proprietario = self.entry_id_proprietario.get()
        self.cursor.execute(
            """ SELECT id_cartao, id_proprietario, qtde_credito, tipo_cartao, data_emissao  FROM geovani_martins_pereira.cartoes
            WHERE id_proprietario LIKE '%s' ORDER BY id_proprietario ASC""" % id_proprietario)
        buscanome = self.cursor.fetchall()
        for i in buscanome:
            self.lista_grid.insert("", END, values=i)
        self.limpar_campos()
        self.db_desconect()
    
    def OnDubleClick(self,event):
        self.limpar_campos()
        self.lista_grid.selection()

        for x in self.lista_grid.selection():
            col1,col2,col3,col4,col5 = self.lista_grid.item(x,'values')
            self.entry_id_cartao.insert(END, col1)
            self.entry_id_proprietario.insert(END, col2)
            self.entry_qtde_credito.insert(END, col3)
            self.entry_tipo_cartao.insert(END, col4)
            self.entry_data_emissao.insert(END, col5)
            

    def deleta_cartao(self):
        self.capturar_campos()
        self.db_conect()
        self.cursor.execute("""DELETE FROM geovani_martins_pereira.cartoes WHERE id_cartao = ?""",(self.id_cartao))
        self.conexao.commit()
        self.db_desconect()
        self.limpar_campos()
        self.select_lista()

    def alterar_cartao(self):
        self.capturar_campos()
        self.db_conect()
        self.cursor.execute("""UPDATE geovani_martins_pereira.cartoes SET id_proprietario = ?, qtde_credito = ?, tipo_cartao = ?, data_emissao = ?
        WHERE id_cartao = ?;
        """,(self.id_cartao, self.id_proprietario, self.qtde_credito,self.tipo_cartao,self.data_emissao,self.id_sistema))
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
        
        self.modelo  = PhotoImage(file='imagens/carduser.png')
        self.img1 = Label(self.frame1, image=self.modelo, bd=0, highlightbackground="black", highlightthickness=1)
        self.img1.place(relx=0.010, rely=0.030)
        
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
        
        self.bt_buscar = Button(self.frame1, text="Buscar usuário", bd=6, 
                                bg="#062617", fg="#9e0b13", activebackground='red', activeforeground="yellow", font=('segoe print', 12, 'bold'), command=self.buscar_cartao)
        self.bt_buscar.place(relx=0.38, rely=0.1, relwidth=0.12, relheight=0.15)
        

        self.listaCartoes=["Comum", "Vale-transporte", "Estudante", "Idoso"]

        self.lb_typecard = Label(self.frame1, text="*Tipo do Cartão:",bg="#962129", fg="black", font=('segoe print', 12, 'bold'))
        self.lb_typecard.pack()
        self.lb_typecard.place(relx=0.65, rely=0.35, relwidth=0.2)

        self.entry_tipo_cartao= ttk.Combobox(self.frame1,values=self.listaCartoes)
        self.entry_tipo_cartao.set("Escolha um tipo*")
        self.entry_tipo_cartao.pack()
        self.entry_tipo_cartao.place(relx=0.7, rely=0.45, relwidth=0.1, relheight=0.1)

        
        # botão Novo
        self.bt_novo = Button(self.frame1, text="Inserir", bd=6,
                               bg="#062617", fg="#9e0b13", font=('segoe print', 12, 'bold'),command=self.add_cartao)
        self.bt_novo.place(relx=0.58, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão Altera
        self.bt_alterar = Button(self.frame1, text="Alterar", bd=6,
                                bg="#062617", fg="#9e0b13", font=('segoe print', 12, 'bold'),command=self.alterar_cartao)
        self.bt_alterar.place(relx=0.69, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão Apagar
        self.bt_apagar = Button(self.frame1, text="Apagar", bd=6,
                                bg="#062617", fg="#9e0b13", font=('segoe print', 12, 'bold'),command=self.deleta_cartao)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        # label e entry - codigo -----------------------------
       
        
        self.lb_id_cartao = Label(self.frame1, text="*ID do Cartão:",
                            bg="#962129", fg="black", font=('segoe print', 12, 'bold'))
        self.lb_id_cartao.place(relx=0.30, rely=0.30)

        self.entry_id_cartao = Entry(self.frame1, 
                                bg="#212021", fg="white", font=('segoe print', 12, 'bold'))
        self.entry_id_cartao.place(relx=0.30, rely=0.40, relwidth=0.08)

        self.lb_id_proprietario = Label(self.frame1, text="*ID do Propietário:",
                            bg="#962129", fg="black", font=('segoe print', 12, 'bold'))
        self.lb_id_proprietario.place(relx=0.30, rely=0.50)

        self.entry_id_proprietario = Entry(self.frame1, 
                               bg="#212021", fg="white", font=('segoe print', 12, 'bold'))
        self.entry_id_proprietario.place(relx=0.30, rely=0.60, relwidth=0.08)

        # label e entry - nome ----------------------------------
        self.lb_qtde_credito = Label(self.frame1, text="*Quantidade de créditos:",
                            bg="#962129", fg="black", font=('segoe print', 12, 'bold'))
        self.lb_qtde_credito.place(relx=0.30, rely=0.70)

        self.entry_qtde_credito = Entry(self.frame1,
                                bg="#212021", fg="white", font=('segoe print', 12, 'bold'))
        self.entry_qtde_credito.place(relx=0.30, rely=0.80, relwidth=0.08)

        self.lb_data_emissao = Label(self.frame1, text="Data de Emissão:",
                            bg="#962129", fg="black", font=('segoe print', 12, 'bold'))
        self.lb_data_emissao.place(relx=0.7, rely=0.75)

        self.entry_data_emissao = DateEntry(self.frame1, locale='pt_BR', date_pattern='dd/mm/y',
                                bg="#962129", fg="black", font=('segoe print', 12, 'bold'))
        self.entry_data_emissao.place(relx=0.7, rely=0.85, relwidth=0.12)
        
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


    def grid_cartao(self):
        self.lista_grid = ttk.Treeview(self.frame2, height=3,
                                    column=('col1', 'col2', 'col3', 'col4','col5','col6'))
        self.lista_grid.heading("#0", text='')
        self.lista_grid.heading("#1", text='ID SISTEMA')                              
        self.lista_grid.heading("#2", text='ID CARTÃO')
        self.lista_grid.heading("#3", text='ID PROPRIETÁRIO')
        self.lista_grid.heading("#4", text='QTD CRÉDITO')
        self.lista_grid.heading("#5", text='TIPO CARTÃO')
        self.lista_grid.heading("#6", text='DATA EMISSÃO')



        self.lista_grid.column("#0", width=0)
        self.lista_grid.column("#1", width=100)
        self.lista_grid.column("#2", width=100)
        self.lista_grid.column("#3", width=125)
        self.lista_grid.column("#4", width=125)
        self.lista_grid.column("#5", width=125)
        self.lista_grid.column("#6", width=125)
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


   