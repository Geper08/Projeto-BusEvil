from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Canvas
from tkcalendar import DateEntry
from datetime import *
import sqlite3

class Usuarios(Toplevel):
    
    cor_white = '#edf6f9'
    cor_fundo = '#b6e0f8'

    def __init__(self, original):
        self.frame_original = original
        self.tela2()
        self.frames_tela()
        self.grid_usuario()
        self.widgets_frame1()
        self.Menus()
        
        self.criar_tabela()  # Adiciona a criação da tabela antes de executar seleções
        self.select_lista()
        self.buscar_usuario()


    def tela2(self):
        Toplevel.__init__(self)
        self.config(cursor="target")
        self.title("Tela Usuário")
        self.configure(background='black')
        self.iconbitmap('imagens/umbrella.ico')
        self.geometry("1280x720")
        self.resizable(True, True)
        self.maxsize(width=1280, height=720)
        self.minsize(width=400, height=300)
        

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
        CREATE TABLE IF NOT EXISTS usuario (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            sobrenome TEXT NOT NULL,
            email TEXT NOT NULL,
            bairro TEXT NOT NULL,
            data_nascimento TEXT NOT NULL);""")
        self.conexao.commit()
        print("banco Criado")
        self.db_desconect()

    def capturar_campos(self):
        self.id_usuario = self.entry_id_usuario.get()
        self.nome = self.entry_nome.get()
        self.sobrenome = self.entry_sobrenome.get()
        self.email = self.entry_email.get()
        self.bairro = self.entry_bairro.get()
        self.data_nascimento = self.entry_data_nascimento.get()
        
        
        
        
    def limpar_campos(self):  
        self.entry_id_usuario.delete(0, END)
        self.entry_nome.delete(0, END)
        self.entry_sobrenome.delete(0, END)
        self.entry_email.delete(0, END)
        self.entry_bairro.delete(0, END)
        self.entry_data_nascimento.delete(0, END)
        
    

    def add_usuario(self):
        # obter dados dos campos
        self.capturar_campos()
        if self.entry_id_usuario.get() == "":
            msg = "Para cadastrar novo USUÁRIO é necessário \n"
            msg += "preencher o campo ID"
            messagebox.showinfo("Cadastro USUÁRIOs >> Aviso!!!", msg)
        elif self.entry_nome.get() == "":
            msg = "Para cadastrar novo USUÁRIO é necessário \n"
            msg += "preencher o campo NOME"
            messagebox.showinfo("Cadastro USUÁRIO >> Aviso!!!", msg)
        elif self.entry_sobrenome.get() == "":
            msg = "Para cadastrar novo USUÁRIO é necessário \n"
            msg += "preencher o campo SOBRENOME"
            messagebox.showinfo("Cadastro USUÁRIOs >> Aviso!!!", msg)
        elif self.entry_email.get() == "":
            msg = "Para cadastrar novo USUÁRIO é necessário \n"
            msg += "preencher o campo E-MAIL"
            messagebox.showinfo("Cadastro USUÁRIOs >> Aviso!!!", msg)
        elif self.entry_bairro.get() == "":
            msg = "Para cadastrar novo USUÁRIO é necessário \n"
            msg += "preencher o campo um BAIRRO"
            messagebox.showinfo("Cadastro Usuários >> Aviso!!!", msg)
        elif self.entry_data_nascimento.get() == "":
            msg = "Para cadastrar novo Usuário é necessário \n"
            msg += "preencher o campo DATA DE NASCIMENTO"
            messagebox.showinfo("Cadastro MOTORISTA >> Aviso!!!", msg)
        else:
            
            self.db_conect()
            self.comando = f"""INSERT INTO usuario (nome, sobrenome, email, bairro, data_nascimento) 
                VALUES("{self.nome}", "{self.sobrenome}", "{self.email}", "{self.bairro}", "{self.data_nascimento}")"""
            self.cursor.execute(self.comando)
            self.conexao.commit()
            self.db_desconect()
            self.select_lista()
            self.limpar_campos()

    def select_lista(self):
        self.lista_grid.delete(*self.lista_grid.get_children())
        self.db_conect()
        lista = self.cursor.execute("""SELECT id_usuario, nome, sobrenome, email, bairro, data_nascimento
            FROM usuario ORDER BY id_usuario ASC;""")
        for l in lista:
            self.lista_grid.insert('', END, values=l)
        self.db_desconect()
    
        
    def buscar_usuario(self):
        self.db_conect()
        self.lista_grid.delete(*self.lista_grid.get_children())
        
        self.entry_nome.insert(END, '%')
        nome = self.entry_nome.get()
        self.cursor.execute(
            """ SELECT id_usuario, nome, sobrenome, email, bairro, data_nascimento FROM usuario
            WHERE nome LIKE '%s' ORDER BY id_usuario ASC""" % nome)
        buscanome = self.cursor.fetchall()
        for i in buscanome:
            self.lista_grid.insert("", END, values=i)
        self.limpar_campos()
        self.db_desconect()
        

    def OnDubleClick(self, event):
        self.limpar_campos()
        self.lista_grid.selection()

        for x in self.lista_grid.selection():
            col1, col2, col3, col4, col5, col6 = self.lista_grid.item(
                x, 'values')
            self.entry_id_usuario.insert(END, col1)
            self.entry_nome.insert(END, col2)
            self.entry_sobrenome.insert(END, col3)
            self.entry_email.insert(END, col4)
            self.entry_bairro.insert(END, col5)
            self.entry_data_nascimento.insert(END, col6)
            

    def deleta_usuario(self):
        self.capturar_campos()
        self.db_conect()
        self.cursor.execute("""DELETE FROM usuario WHERE id_usuario = ?""",(self.id_usuario))
        self.conexao.commit()
        self.db_desconect()
        self.limpar_campos()
        self.select_lista()

    def alterar_usuario(self):
        self.capturar_campos()
        self.db_conect()
        self.cursor.execute("""UPDATE usuario SET nome = ?, sobrenome = ?, email = ? , bairro = ?, data_nascimento = ?
            WHERE id_usuario = ?;
            """, (self.nome, self.sobrenome, self.email, self.bairro, self.data_nascimento, self.id_usuario))
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
        

        self.modelo = PhotoImage(file='imagens/redqueen.png')
        self.img1 = Label(self.frame1, image=self.modelo, bd=0,
                          highlightbackground="black", highlightthickness=1)
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
        
        self.bt_buscar = Button(self.frame1, text="Buscar Nome", bd=6, 
                                bg="#062617", fg="#9e0b13", activebackground='red', activeforeground="yellow", font=('segoe print', 12, 'bold'), command=self.buscar_usuario)
        self.bt_buscar.place(relx=0.38, rely=0.1, relwidth=0.12, relheight=0.15)

        # botão Novo
        self.bt_novo = Button(self.frame1, text="Inserir", bd=6,
                              bg="#062617", fg="#9e0b13", activebackground='red', activeforeground="yellow", font=('segoe print', 12, 'bold'), command=self.add_usuario)
        self.bt_novo.place(relx=0.58, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão Altera
        self.bt_alterar = Button(self.frame1, text="Alterar", bd=6,
                                 bg="#062617", fg="#9e0b13", activebackground='red', activeforeground="yellow", font=('segoe print', 12, 'bold'), command=self.alterar_usuario)
        self.bt_alterar.place(relx=0.69, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão Apagar
        self.bt_apagar = Button(self.frame1, text="Apagar", bd=6,
                                bg="#062617", fg="#9e0b13", activebackground='red', activeforeground="yellow", font=('segoe print', 12, 'bold'), command=self.deleta_usuario)
        self.bt_apagar.place(relx=0.80, rely=0.1, relwidth=0.1, relheight=0.15)

        # label e entry - codigo -----------------------------
        
        
        self.lb_id_usuario = Label(self.frame1, text="*ID:",
                          bg="#962129", fg="black", font=('segoe print', 12, 'bold'))
        self.lb_id_usuario.place(relx=0.05, rely=0.35)

        self.entry_id_usuario = Entry(self.frame1,
                             bg="#212021", fg="white", font=('segoe print', 12, 'bold'))
        self.entry_id_usuario.place(relx=0.05, rely=0.45, relwidth=0.08)

        # label e entry - nome ----------------------------------
        self.lb_nome = Label(self.frame1, text="*Nome:",
                            bg="#962129", fg="black", font=('segoe print', 12, 'bold'))
        self.lb_nome.place(relx=0.05, rely=0.55)

        self.entry_nome = Entry(self.frame1,
                               bg="#212021", fg="white", font=('segoe print', 12, 'bold'))
        self.entry_nome.place(relx=0.05, rely=0.65, relwidth=0.4)

        # label e entry - Telfone--------------------------
        self.lb_sobrenome = Label(self.frame1, text="*Sobrenome:",
                                 bg="#962129", fg="black", font=('segoe print', 12, 'bold'))
        self.lb_sobrenome.place(relx=0.05, rely=0.75)

        self.entry_sobrenome = Entry(self.frame1,
                                    bg="#212021", fg="white", font=('segoe print', 12, 'bold'))
        self.entry_sobrenome.place(relx=0.05, rely=0.85, relwidth=0.4)

        self.lb_email = Label(self.frame1, text="*E-mail:",
                              bg="#962129", fg="black", font=('segoe print', 12, 'bold'))
        self.lb_email.place(relx=0.5, rely=0.35)  # 0.75 0.85

        self.entry_email = Entry(self.frame1,
                                 bg="#212021", fg="white", font=('segoe print', 12, 'bold'))
        self.entry_email.place(relx=0.5, rely=0.45, relwidth=0.4)

        # label e entry - Cidade -----------------------
        self.lb_bairro = Label(self.frame1, text="*Bairro:",
                               bg="#962129", fg="black", font=('segoe print', 12, 'bold'))
        self.lb_bairro.place(relx=0.5, rely=0.55)

        self.entry_bairro = Entry(self.frame1,
                                  bg="#212021", fg="white", font=('segoe print', 12, 'bold'))
        self.entry_bairro.place(relx=0.5, rely=0.65, relwidth=0.4)

        self.lb_data_nascimento = Label(self.frame1, text="*Data de Nascimento:",
                                       bg="#962129", fg="black", font=('segoe print', 12, 'bold'))
        self.lb_data_nascimento.place(relx=0.5, rely=0.75)

        self.entry_data_nascimento = Entry(self.frame1, 
                                              bg="#212021", fg="white", font=('segoe print', 12, 'bold'))
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

    def grid_usuario(self):
        self.lista_grid = ttk.Treeview(self.frame2, height=3,
                                       column=("col1", "col2", "col3", "col4", "col5", "col6"))
        self.lista_grid.heading("#0", text="")
        self.lista_grid.heading("#1", text="ID")
        self.lista_grid.heading("#2", text="NOME")
        self.lista_grid.heading("#3", text="SOBRENOME")
        self.lista_grid.heading("#4", text="EMAIL")
        self.lista_grid.heading("#5", text="BAIRRO")
        self.lista_grid.heading("#6", text="DATA NASCIMENTO")

        self.lista_grid.column("#0", width=0)
        self.lista_grid.column("#1", width=40)
        self.lista_grid.column("#2", width=10)
        self.lista_grid.column("#3", width=200)
        self.lista_grid.column("#4", width=125)
        self.lista_grid.column("#5", width=125)
        self.lista_grid.column("#6", width=125)
      

    
        self.lista_grid.place(relx=0.01, rely=0.06,
                              relwidth=0.97, relheight=0.86)

        self.scrol_lista = Scrollbar(self.frame2, orient='vertical')
        self.lista_grid.configure(yscroll=self.scrol_lista.set)
        self.scrol_lista.place(relx=0.98, rely=0.05,
                               relwidth=0.02, relheight=0.89)
        self.lista_grid.bind("<Double-1>", self.OnDubleClick)

    def Menus(self):
        Menubar = Menu(self)
        self.config(menu=Menubar)
        filemenu = Menu(Menubar)

        def Quit(): self.destroy()

        Menubar.add_cascade(label="opções", menu=filemenu)

        filemenu.add_command(label="Sair sistema", command=Quit)

    def onClose(self):
        self.destroy()
        self.frame_original.show()
