from tkinter import *
from usuario import Usuarios
from motorista import Motoristas
from onibus import Onibus
from cartao import Cartoes
from encerrar import TelaEncerrar

class MenuTela:
        
    
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_tela()
        self.widgets_frame2()
        self.widgets_frame3()
        self.Menus()
        root.mainloop()

    def tela(self):
        self.root.config(cursor="target")
        self.root.iconbitmap('imagens/umbrella.ico')
        self.root.title("Menu EvilCard - Bem Vindo!!!")
        self.root.configure(background='#272c38')
        self.root.geometry("1366x768")
        self.root.resizable(True, True)
        self.root.maxsize(width=1366, height=768)
        self.root.minsize(width=400, height=300)
        
    list= ["target"]
        
        


    def frames_tela(self):
        self.frame1 = Frame(self.root, bd=4, bg="#272c38",
                            )
        self.frame1.place(relx=0.003, rely=0.001, relwidth=0.99, relheight=0.99)
        
        self.frame2 = Frame(self.root, bd=4, bg="#272c38",
                            )
        self.frame2.place(relx=0.006, rely=0.01, relwidth=0.4, relheight=0.05)
        
        
        
        
        self.modelo = PhotoImage(file='imagens/fundore.png')
        self.img1 = Label(
            self.frame1,
            image=self.modelo,
            bd=0
            )
        self.img1.place(
                relx=0.0,
                rely=0.0)
        
        
    def widgets_frame2(self):
        
            
        
        self.bt_limpar = Button(self.frame1, text="Menu Usuário", bd=6,
                                    bg="#062617", fg="#9e0b13", activebackground='red', activeforeground="yellow", font=('segoe print', 15, 'bold'), command=self.clica_entrar)
        self.bt_limpar.place(relx=0.21, rely=0.07, relwidth=0.2, relheight=0.10)

            # Botão Altera
        self.bt_alterar = Button(self.frame1, text="Menu Motorista", bd=6,
                                    bg="#062617", fg="#9e0b13", activebackground='red', activeforeground="yellow", font=('segoe print', 15, 'bold'), command=self.clica_entrar2)
        self.bt_alterar.place(relx=0.21, rely=0.19, relwidth=0.2, relheight=0.10)

            # Botão Apagar
        self.bt_apagar = Button(self.frame1, text="Menu Ônibus", bd=6,
                                     bg="#062617", fg="#9e0b13", activebackground='red', activeforeground="yellow", font=('segoe print', 15, 'bold'), command=self.clica_entrar3)
        self.bt_apagar.place(relx=0.21, rely=0.31, relwidth=0.2, relheight=0.10)
        
          # Botão Apagar
        self.bt_apagar = Button(self.frame1, text="Menu Cartão", bd=6,
                                     bg="#062617", fg="#9e0b13", activebackground='red', activeforeground="yellow", font=('segoe print', 15, 'bold'), command=self.clica_entrar4)
        self.bt_apagar.place(relx=0.21, rely=0.43, relwidth=0.2, relheight=0.10)
        
        self.bt_apagar = Button(self.frame1, text="Sair do sistema", bd=6,
                                     bg="#062617", fg="#9e0b13", activebackground='red', activeforeground="yellow", font=('segoe print', 15, 'bold'), command=self.clica_entrar5)
        self.bt_apagar.place(relx=0.21, rely=0.55, relwidth=0.2, relheight=0.10)
        
    def widgets_frame3(self):
        welcome = Label(
            self.frame2,
            text='Projeto CadUni! Escolha uma opção:',
            font=('segoe print', 12),
            bg='#272c38',
            fg='#9e0b13')
        welcome.place(relx=0.001, rely=0.01, relwidth=1, relheight=1)
 


    def Menus(self):
        Menubar = Menu(self.root)
        self.root.config(menu=Menubar)
        filemenu = Menu(Menubar)

        def Quit(): self.root.destroy()
        Menubar.add_cascade(label="opções", menu=filemenu)
        filemenu.add_command(label="Sair sistema", command=Quit)

    def clica_entrar(self):  # comando btn
        self.hide()
        self.subFrame = Usuarios(self)
    def clica_entrar2(self):  # comando btn
        self.hide()
        self.subFrame = Motoristas(self)
    def clica_entrar3(self):  # comando btn
        self.hide()
        self.subFrame = Onibus(self)
    def clica_entrar4(self):  # comando btn
        self.hide()
        self.subFrame = Cartoes(self)
    def clica_entrar5(self):  # comando btn
        self.hide()
        self.subFrame = TelaEncerrar(self)

    def hide(self):  # esconde o root
        self.root.withdraw()

    def show(self):  # Mostra o root novamente
        self.root.update()
        self.root.deiconify()
        

root=Tk()
MenuTela()
