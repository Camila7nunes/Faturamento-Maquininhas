from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

#Classe responsável por gerar o resultado visual
class Interface:

    def __init__(self, saidaDados):

        #Listas que vão armazenar o ID e os valores faturados das maquininhas respectivamente
        maquininhas = []
        valoresFaturados = []

        #Criação da janela onde será inserida as informações
        janela = Tk()
        janela.title("Faturamento Mês de Janeiro")

        #Criação da tabela gráfica que "retorna" as informações do faturamento das maquininhas
        tree = ttk.Treeview(janela, selectmode="browse", column=("column1", "column2"), show="headings")

        #Define as colunas da tabela
        tree.column("column1", width=30, minwidth=50, stretch=NO)
        tree.heading("#1", text="Id")
        tree.column("column2", width=200, minwidth=50, stretch=NO)
        tree.heading("#2", text="Valor Faturamento")

        #Define o tamanho da janela onde será inserida as informações
        janela.geometry('900x900')

        #Define que a janela deve ser expansível
        tree.pack(fill=BOTH, expand=True)

        # Lê os dados do arquivo de saída
        for dados in saidaDados:

            #Remove quebras de linha
            dados = dados.replace("\n", "")
            #Separa o resultado de cada maquininha
            dados = dados.split(";")

            #Listas recebem seus respectivos dados
            maquininhas.append(dados[0])
            valoresFaturados.append(float(dados[1]))

            #Insere dados na tabela
            tree.insert("", END, values=dados)

        #Criação do gráfico de barras
        fig6, ax1 = plt.subplots()

        #Gráfico recebe os valores a serem projetados
        ax1.bar(maquininhas, valoresFaturados)
        ax1.set_ylabel("Valores do faturamento")
        ax1.set_xlabel("ID das maquininhas")
        ax1.set_title("Faturamento Mês de Janeiro")

        #Cria um objeto Canvas e o insere na janela principal
        canvas = FigureCanvasTkAgg(fig6, master=janela)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True)

        #Plota o resultado
        janela.state('zoomed')
        janela.mainloop()