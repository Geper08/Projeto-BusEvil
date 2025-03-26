from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
import pyodbc
import sqlite3
from datetime import datetime



class Motoristas(Toplevel):
    cor_white = '#edf6f9'
    cor_fundo = '#b6e0f8'

    def __init__(self, original):
        self.frame_original = original
        self.tela3()
        self.frames_tela()
        self.grid_motorista()
        self.widgets_frame1()
        self.Menus()
        self.criar_tabela()  # Adiciona a criação da tabela antes de executar seleções
        self.select_lista()
        self.buscar_motorista()

    def tela3(self):
        Toplevel.__init__(self)
        self.config(cursor="target")
        self.title("Tela Motorista")
        self.configure(background='black')
        self.iconbitmap('imagens/umbrella.ico')
        self.geometry("1280x720")
        self.resizable(True, True)
        self.maxsize(width=1280, height=720)
        self.minsize(width=400, height=300)

    def limpar_campos(self):
        self.entry_id_motorista.delete(0, END)
        self.entry_num_cnh.delete(0, END)
        self.entry_nome.delete(0, END)
        self.entry_sobrenome.delete(0, END)
        self.entry_data_nascimento.delete(0, END)

    def db_conect(self):
        self.conexao = sqlite3.connect('meu_banco.db')
        self.cursor = self.conexao.cursor()
        print('Conectado ao banco SQLite3')


    def db_desconect(self):
        self.conexao.close() 
        print("Desconectando ao banco de dados sqlite3")

    def criar_tabela(self):
        self.db_conect()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS motorista (
            id_motorista INTEGER PRIMARY KEY AUTOINCREMENT,
            num_cnh INTEGER NOT NULL,
            nome TEXT NOT NULL,
            sobrenome TEXT NOT NULL,
            data_nascimento DATE NOT NULL);""")  # Alterado para DATE
        self.conexao.commit()
        print("Banco Criado")
        self.db_desconect()



    def capturar_campos(self):
        # Captura os valores dos campos
        self.id_motorista = self.entry_id_motorista.get()
        self.nome = self.entry_nome.get()

        # Verifica se ao menos um campo foi preenchido
        if not self.id_motorista and not self.nome:
            messagebox.showerror("Erro", "Preencha ao menos o campo ID MOTORISTA ou NOME para buscar!")
            return None

        # Define o tipo de busca
        if self.id_motorista:
            self.campo_busca = "id_motorista"
            self.valor_busca = self.id_motorista
        elif self.nome:
            self.campo_busca = "nome"
            self.valor_busca = self.nome



    def add_motorista(self):
        # Obter dados dos campos
        self.capturar_campos()

        # Validação do número da CNH
        if not self.num_cnh.isdigit() or len(self.num_cnh) != 10:
            messagebox.showerror("Erro de Validação", "O Número da CNH deve conter exatamente 10 dígitos numéricos.")
            return  # Sai da função sem salvar

        if self.entry_id_motorista.get() == "":
            msg = "Para cadastrar novo MOTORISTA é necessário \n"
            msg += "preencher o campo  ID MOTORISTA"
            messagebox.showinfo("Cadastro MOTORISTA >> Aviso!!!", msg)
        elif self.entry_nome.get() == "":
            msg = "Para cadastrar novo MOTORISTA é necessário \n"
            msg += "preencher o campo  NOME"
            messagebox.showinfo("Cadastro MOTORISTA >> Aviso!!!", msg)
        elif self.entry_sobrenome.get() == "":
            msg = "Para cadastrar novo Usuário é necessário \n"
            msg += "preencher o campo  SOBRENOME"
            messagebox.showinfo("Cadastro MOTORISTA >> Aviso!!!", msg)
        elif self.entry_data_nascimento.get() == "":
            msg = "Para cadastrar novo Usuário é necessário \n"
            msg += "preencher o campo DATA DE NASCIMENTO"
            messagebox.showinfo("Cadastro MOTORISTA >> Aviso!!!", msg)
        else:
            self.db_conect()
            # Inserindo a data formatada no banco
            self.cursor.execute("""INSERT INTO motorista (num_cnh, nome, sobrenome, data_nascimento)
            VALUES(?,?,?,?)""", (self.num_cnh, self.nome, self.sobrenome, self.data_nascimento))
            self.conexao.commit()
            self.db_desconect()
            self.select_lista()
            self.limpar_campos()

            
    def select_lista(self):
        self.lista_grid.delete(*self.lista_grid.get_children())
        self.db_conect()
        lista = self.cursor.execute("""SELECT id_motorista , num_cnh,  nome, sobrenome, data_nascimento
        FROM motorista ORDER BY id_motorista ASC;""")
        for l in lista:
            self.lista_grid.insert("",END,values=l)
        self.db_desconect()
    
    def buscar_motorista(self):
        self.db_conect()
        self.lista_grid.delete(*self.lista_grid.get_children())
        
        self.entry_nome.insert(END, '%')
        nome = self.entry_nome.get()
        self.cursor.execute(
            """ SELECT id_motorista, num_cnh, nome, sobrenome, data_nascimento FROM motorista
            WHERE nome LIKE '%s' ORDER BY id_motorista ASC""" % nome)
        buscanome = self.cursor.fetchall()
        for i in buscanome:
            self.lista_grid.insert("", END, values=i)
        self.limpar_campos()
        self.db_desconect()
        
    def OnDubleClick(self, event):
        self.limpar_campos()
        self.lista_grid.selection()

        for x in self.lista_grid.selection():
            col1,col2,col3,col4,col5 = self.lista_grid.item(x,'values')
            self.entry_id_motorista.insert(END, col1)
            self.entry_num_cnh.insert(END, col2)
            self.entry_nome.insert(END, col3)
            self.entry_sobrenome.insert(END, col4)
            self.entry_data_nascimento.insert(END, col5)

    def deleta_motorista(self, event):
        self.capturar_campos()
        self.db_conect()
        self.cursor.execute("""DELETE FROM motorista WHERE id_motorista = ?""",(self.id_motorista,))
        self.conexao.commit()
        self.db_desconect()
        self.limpar_campos()
        self.select_lista()

    def alterar_motorista(self):
        self.capturar_campos()
        self.db_conect()
        self.cursor.execute("""UPDATE motorista SET  num_cnh = ?, nome = ?, sobrenome = ?, data_nascimento = ?
        WHERE id_motorista = ?;
        """,(self.num_cnh, self.nome,self.sobrenome,self.data_nascimento,self.id_motorista))
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
        
        self.modelo  = PhotoImage(file='imagens/motoristazombie.png')
        self.img1 = Label(self.frame1, image=self.modelo, bd=0, highlightbackground="black", highlightthickness=1)
        self.img1.place(relx=0.010, rely=0.040)
        
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
        
        self.bt_buscar = Button(self.frame1, text="Buscar Nome", bd=6, 
                                bg="#062617", fg="#9e0b13", activebackground='red', activeforeground="yellow", font=('segoe print', 12, 'bold'), command=self.buscar_motorista)
        self.bt_buscar.place(relx=0.38, rely=0.1, relwidth=0.12, relheight=0.15)
        # botão Novo
        self.bt_novo = Button(self.frame1, text="Inserir", bd=6,
                               bg="#062617", fg="#9e0b13", activebackground='red', activeforeground="yellow", font=('segoe print', 12, 'bold'),command=self.add_motorista)
        self.bt_novo.place(relx=0.58, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão Altera
        self.bt_alterar = Button(self.frame1, text="Alterar", bd=6,
                                bg="#062617", fg="#9e0b13", activebackground='red', activeforeground="yellow", font=('segoe print', 12, 'bold'),command=self.alterar_motorista)
        self.bt_alterar.place(relx=0.69, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão Apagar
        self.bt_apagar = Button(self.frame1, text="Apagar", bd=6,
                                bg="#062617", fg="#9e0b13", activebackground='red', activeforeground="yellow", font=('segoe print', 12, 'bold'),command=self.deleta_motorista)
        self.bt_apagar.place(relx=0.80, rely=0.1, relwidth=0.1, relheight=0.15)



        # label e entry - codigo -----------------------------
    
        
        self.lb_id_motorista = Label(self.frame1, text="*ID Motorista:",
                           bg="#962129", fg="black", font=('segoe print', 11, 'bold'))
        self.lb_id_motorista.place(relx=0.05, rely=0.30)

        self.entry_id_motorista = Entry(self.frame1, 
                                bg="#212021", fg="white", font=('segoe print', 11, 'bold'))
        self.entry_id_motorista.place(relx=0.05, rely=0.40, relwidth=0.08)

        # label e entry - nome ----------------------------------
        self.lb_nome = Label(self.frame1, text="*Nome:",
                            bg="#962129", fg="black", font=('segoe print', 11, 'bold'))
        self.lb_nome.place(relx=0.05, rely=0.50)

        self.entry_nome = Entry(self.frame1,
                                bg="#212021", fg="white", font=('segoe print', 11, 'bold'))
        self.entry_nome.place(relx=0.05, rely=0.60, relwidth=0.4)

        self.lb_sobrenome = Label(self.frame1, text="*Sobrenome:",
                            bg="#962129", fg="black", font=('segoe print', 11,'bold'))
        self.lb_sobrenome.place(relx=0.5, rely=0.50)#0.75 0.85

        self.entry_sobrenome = Entry(self.frame1,
                                bg="#212021", fg="white", font=('segoe print', 11,'bold'))
        self.entry_sobrenome.place(relx=0.5, rely=0.60, relwidth=0.4)

        # label e entry - Telfone--------------------------
        self.lb_num_cnh = Label(self.frame1, text="*Número da CNH:",
                               bg="#962129", fg="black", font=('segoe print', 11, 'bold'))
        self.lb_num_cnh.place(relx=0.05, rely=0.75)

        self.entry_num_cnh = Entry(self.frame1,
                                bg="#212021", fg="white", font=('segoe print', 11, 'bold'))
        self.entry_num_cnh.place(relx=0.05, rely=0.85, relwidth=0.15)

        self.lb_data_nascimento = Label(self.frame1, text="*Data de Nascimento:",
                            bg="#962129", fg="black", font=('segoe print', 11, 'bold'))
        self.lb_data_nascimento.place(relx=0.5, rely=0.75)

        self.entry_data_nascimento = DateEntry(self.frame1, locale='pt_BR', date_pattern='dd/mm/y',
                                bg="#212021", fg="white", font=('segoe print', 11, 'bold'))
        self.entry_data_nascimento.place(relx=0.5, rely=0.85, relwidth=0.12)
        
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

    def grid_motorista(self):
        self.lista_grid = ttk.Treeview(self.frame2, height=3,
                                    column=('col1', 'col2', 'col3', 'col4','col5'))
        self.lista_grid.heading("#0", text='')                             
        self.lista_grid.heading("#1", text='ID MOTORISTA')
        self.lista_grid.heading("#2", text='NÚMERO CNH')
        self.lista_grid.heading("#3", text='NOME')
        self.lista_grid.heading("#4", text='SOBRENOME')
        self.lista_grid.heading("#5", text='DATA NASCIMENTO')



        self.lista_grid.column("#0", width=0)
        self.lista_grid.column("#1", width=40)
        self.lista_grid.column("#2", width=10)
        self.lista_grid.column("#3", width=200)
        self.lista_grid.column("#4", width=125)
        self.lista_grid.column("#5", width=125)
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

            


