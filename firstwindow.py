from tkinter import *
from tkinter import ttk
import mysql.connector
import os


class FuncoesDosBotoes:
    def armazenar_variaveis(self):
        self.titulo = self.titulo_entry.get()
        self.autor = self.autor_entry.get()
        self.genero = self.genero_entry.get()
        self.codigo = self.codigo_entry.get()
    
    def limpar_tela(self):
        self.codigo_entry.delete(0, END)
        self.titulo_entry.delete(0, END)
        self.autor_entry.delete(0, END)
        self.genero_entry.delete(0, END)

    def add_livro(self):
        self.armazenar_variaveis()
        self.comando = """INSERT INTO acervo(s_titulo_acervo, s_autor_acervo, s_genero_acervo, i_quantidade_acervo) VALUES (%s, %s, %s, %s)"""
        self.dados = (self.titulo, self.autor, self.genero, 1)
        conex.cursor().execute(self.comando, self.dados)
        conex.cursor().close()
        self.limpar_tela()
        self.mostrar_livros()

    def mostrar_livros(self):
        self.clientList.delete(*self.clientList.get_children())
        self.instrucao = 'SELECT i_id_acervo,s_titulo_acervo, s_autor_acervo, s_genero_acervo FROM acervo;'
        self.cursor = conex.cursor()
        self.cursor.execute(self.instrucao)
        self.lista = self.cursor.fetchall()
        #Usando o loop for para exibir o conteúdo na tela
        #estudar mais sobre Treeview e seus métodos
        for i in self.lista:
            #o primeiro parâmetro é o id do parent do item da lista(quando inserimos itens na lista sem especificar um id, um id padrão é criado. o primeiro item recebe I001 e assim por diante). Nesse caso, ao colocar "" como id do parent, estamos inserindo o item no root da lista.
            #o segundo é em que posição da lista ele vai ser posicionado dentro do seu parent. se for "", ele será posicionado dentro da lista como um todo.
            #o terceiro é o valor do item a ser inserido na lista, nesse caso, é cada linha da tabela acervo no banco de dados.
            self.clientList.insert('', END, value=i)
        self.cursor.close()
        conex.commit()

    def OnDoubleClick(self, evt):
        self.limpar_tela()
        #retorna o id do(s) item(ns) selecionados
        self.clientList.selection()

        for n in self.clientList.selection():
            #desempacota os valores dos itens, ou seja, cada 'col' receberá um item de um índice. Portanto, col1 = valor do item de índice 0 e assim por diante. a função item nos permite acessar itens da lista. o primeiro parâmetro é o id que foi obtido por 'self.clientList.selection()' e o segundo parâmetro é o que você deseja acessar. Caso queira acessar somente o conteúdo do item, você pode usar 'text' no lugar de 'values'. Values é mais amplo que text, ele engloba data de registro, numero, textos e por aí vai, enquanto text é somente texto.
            col1, col2, col3, col4 = self.clientList.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.titulo_entry.insert(END, col2)
            self.autor_entry.insert(END, col3)
            self.genero_entry.insert(END, col4)
    
    def deletar_livro(self):
        self.armazenar_variaveis()
        self.cursor = conex.cursor()
        self.cursor.execute("""DELETE FROM acervo WHERE i_id_acervo = %s""", (self.clientList.item(self.clientList.selection(), 'values')[0],))
        conex.commit()
        self.cursor.close()
        self.limpar_tela()
        self.mostrar_livros()

    def buscar_livro(self):
        self.armazenar_variaveis()
        self.cursor = conex.cursor()
        self.cursor.execute(f"""SELECT i_id_acervo, s_titulo_acervo, s_autor_acervo, s_genero_acervo FROM acervo WHERE i_id_acervo = %s OR s_titulo_acervo = %s OR s_autor_acervo = %s OR s_genero_acervo = %s;""", (self.codigo_entry.get(), self.titulo, self.autor, self.genero))
        
        self.linhas = self.cursor.fetchall()
        for id in self.clientList.get_children():
            self.clientList.delete(id)
        for linha in self.linhas:
            self.clientList.insert('', END, value=linha)
        conex.commit()
        self.cursor.close()
        self.limpar_tela()
    
    def alterar_livro(self):
        self.armazenar_variaveis()
        self.cursor = conex.cursor()
        self.cursor.execute("""UPDATE acervo SET s_titulo_acervo = %s, s_autor_acervo = %s, s_genero_acervo = %s WHERE i_id_acervo = %s""", (self.titulo, self.autor, self.genero, self.codigo,))
        conex.commit()
        self.cursor.close()
        self.buscar_livro()
        self.limpar_tela()
        self.mostrar_livros()
 
class Application(FuncoesDosBotoes):
    def __init__(self):
        self.janela = Tk()
        self.tela()
        self.frames_da_tela()
        self.criar_botoes()
        self.lista_frame2()
        self.mostrar_livros()
        self.janela.mainloop()

    def tela(self):
        self.janela.title('CADASTRO DE MEMBROS')
        self.janela.geometry('500x600')
        self.janela.config(background='#0081DE')
        self.janela.resizable(True, True)
        self.janela.maxsize(width=600, height=700 )
        self.janela.minsize(width=350, height=400)

    def frames_da_tela(self):
        self.frame_1 = Frame(self.janela, highlightthickness=3, highlightbackground='#0D0D0D')
        self.frame_1.place(relx=0.020, rely=0.016, relwidth=0.96, relheight=0.46)

        self.frame_2 = Frame(self.janela, highlightthickness=3, highlightbackground='#0D0D0D')
        self.frame_2.place(relx=0.020, rely=0.52, relwidth=0.96, relheight=0.46)

    def criar_botoes(self):
        #Criando o botão limpar
        self.bt_limpar = Button(self.frame_1, text='Limpar', bd=0.5, fg='white', bg='#001242', font=('monospace', 7, 'bold'), command=self.limpar_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)
        #Criando  o botão buscar
        self.bt_buscar = Button(self.frame_1, text='Buscar', bd=0.5, fg='white', bg='#001242', font=('monospace', 7, 'bold'), command=self.buscar_livro)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)
        #Criando o botão Novo
        self.bt_novo = Button(self.frame_1, text='Novo', bd=0.5, fg='white', bg='#001242', font=('monospace', 7, 'bold'), command=self.add_livro)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)
        #Criando o botão alterar
        self.bt_alterar = Button(self.frame_1, text='Alterar', bd=0.5, fg='white', bg='#001242', font=('monospace', 7, 'bold'), command=self.alterar_livro)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)
        #Criando o botão Apagar
        self.bt_apagar = Button(self.frame_1, text='Apagar', bd=0.5, fg='white', bg='#001242', font=('monospace', 7, 'bold'), command=self.deletar_livro)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)
        #Criando a Label do código
        self.lb_codigo = Label(self.frame_1, text='Código')
        self.lb_codigo.place(relx=0.05, rely=0.05)
        #Criando a caixa de entrada do código
        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.05, rely=0.16, relwidth=0.085, relheight=0.07)
        #criando a Label do nome
        self.lb_titulo = Label(self.frame_1, text='Título')
        self.lb_titulo.place(relx=0.05, rely=0.24)
        #Criando a caixa de entrada do nome
        self.titulo_entry = Entry(self.frame_1)
        self.titulo_entry.place(relx=0.05, rely=0.34, relwidth=0.75, relheight=0.07)
        #Criando label do telefone
        self.lb_autor = Label(self.frame_1, text='Autor')
        self.lb_autor.place(relx=0.05, rely=0.44)
        #criando a caixa de entrada do telefone
        self.autor_entry = Entry(self.frame_1)
        self.autor_entry.place(relx=0.05, rely=0.54, relwidth=0.4, relheight=0.07)
        #Criando a label da cidade
        self.lb_genero = Label(self.frame_1, text='Gênero')
        self.lb_genero.place(relx=0.54, rely=0.44)
        #Criando a caixa de entrada da cidade
        self.genero_entry = Entry(self.frame_1)
        self.genero_entry.place(relx=0.54, rely=0.54)

    def lista_frame2(self):
        self.clientList = ttk.Treeview(self.frame_2, height=3, column=('col1', 'col2', 'col3', 'col4'))
        self.clientList.heading('#0', text='')
        self.clientList.heading('#1', text='código')
        self.clientList.heading('#2', text='título')
        self.clientList.heading('#3', text='Autor')
        self.clientList.heading('#4', text='Gênero')
        
        self.clientList.column('#0', width=0, stretch=NO)
        self.clientList.column('#1', width=50, stretch=YES)
        self.clientList.column('#2', width=150)
        self.clientList.column('#3', width=100)
        self.clientList.column('#4', width=150)
        
        self.clientList.place(relx=0.01, rely=0.10, relwidth=0.95, relheight=0.85)
        
        self.scrollbarra = Scrollbar(self.frame_2, orient='vertical')
        self.clientList.config(yscroll=self.scrollbarra.set)
        self.scrollbarra.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.clientList.bind("<Double-1>", self.OnDoubleClick)


conex = mysql.connector.connect(
    host='localhost',
    user='root',
    password=os.getenv('senha'),
    port='3306',
    database='meusql',
)


selecao = Application()

# ttk é como se fosse o tk, porém estilizado
# configurações feitas entre widgets como o padding são feitas no .pack() 
#color: #591824; 
#color: #2A3740; 
#color: #8C6E64; 
#color: #A68D85; 
#color: #0D0D0D;



