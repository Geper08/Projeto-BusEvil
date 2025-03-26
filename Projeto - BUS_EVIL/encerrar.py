from tkinter import *



class TelaEncerrar(Toplevel):
    
    cor_white = '#edf6f9'
    cor_fundo = '#b6e0f8'

    def __init__(self, original):
        self.frame_original = original
        self.tela2()
        self.frames_tela()
        self.widgets_frame1()
        self.Menus()
        

    def tela2(self):
        Toplevel.__init__(self)
        self.config(cursor="target")
        self.title("Sair sistema (>>Clique em Opções -> Sair sistema<<)")
        self.configure(background='#272c38')
        self.iconbitmap('imagens/umbrella.ico')
        self.geometry("1280x720")
        self.resizable(True, True)
        self.maxsize(width=1280, height=720)
        self.minsize(width=400, height=300)
        
   

    def frames_tela(self):
        self.frame1 = Frame(self, bd=3, bg="#272c38",
                            )
        self.frame1.place(relx=0.002, rely=0.00, relwidth=0.99, relheight=0.99)
        
        self.frame2 = Frame(self, bd=4, bg="#272c38",
                            )
        self.frame2.place(relx=0.006, rely=0.01, relwidth=0.6, relheight=0.05)
        
        
        
        self.modelo = PhotoImage(file='imagens/fundoencerra.png')
        self.img1 = Label(
            self.frame1,
            image=self.modelo,
            bd=0
            )
        self.img1.place(
                relx=0.0,
                rely=0.0)


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
        
    def widgets_frame1(self):
        welcome = Label(
            self.frame2,
            text='Corra você também para a BusEvil...',
            font=('segoe print', 20),
            bg='#272c38',
            fg='#9e0b13')
        welcome.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)

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
