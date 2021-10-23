from object import Object
from interface import Interface
import csv
from datetime import datetime

listaObject = []

#Função que faz a leitura dos dados
def buildObject():
    has_header = True
    with open('./arquivosTeste/eventosTeste.csv', newline='', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        #Se houver cabeçalho, ignora e passa para a próxima linha
        if(has_header):
            next(reader, None)
        for row in reader:
            #Lê cada linha do arquivo e adiciona na lista
            s = Object(list(row))
            listaObject.append(s)
buildObject()


saidaDados = []
listaId = []

#Ordena os eventos de cada maquininha baseado na data inicial dos eventos
listaObject = sorted(listaObject, key=Object.getDataInicio)
listaObject = sorted(listaObject, key=Object.getID)

#Pega todos os ID's distintos da maquininha
for x in listaObject:
    if not x.ID in listaId:
     listaId.append(x.ID)

for id in listaId:

    #Inicializa variaveis
    data_inicio = ''
    data_fim = datetime.strptime('31-01-2021', '%d-%m-%Y').date()
    id_maq = -1
    preco = 0.00
    valorMaquininha = 0.00
    data_inicial_promo = data_inicio
    data_final_promo = ''

    # Processa uma maquininha a cada iteração
    for obj in listaObject:
        if obj.ID == id:

            id_maq = obj.ID
            #Se o evento for do tipo ATIVAÇÃO, armazena as informações nas variáveis
            if (obj.EVENTO == 1):
                valorAnterior = round(valorMaquininha,2)
                data_inicio = obj.DATA_INICIAL
                preco = obj.PRECO

                #Calcula o faturamento do periodo de ativação
                valorMaquininha = obj.rangeDataAtivacao(data_inicio,data_fim,preco)

                #Se já houve uma desativamento
                if(data_final_promo != ''):
                    #Calcula o faturamento do novo período de ativação
                    faturamentoParcial = obj.faturamento(data_final_promo,data_fim,preco)
                    valorMaquininha = round(((valorAnterior + faturamentoParcial) / 30), 2)

                #Armazena o tipo do evento atual, para verificar posteriormente qual o evento anterior
                eventoAnterior = obj.EVENTO

            #Se o vento for do tipo DESATIVAÇÃO
            elif (obj.EVENTO == 2):
                #Se não houver uma ativação, verifica próximo evento
                if (data_inicio == ''):
                    continue

                #Se ocorreu um período promocional antes da desativação
                if (eventoAnterior == 4):

                    #Calcula o faturamento da ativação até o período promocional, pois período promocional tem prioridade
                    faturamentoParcial = obj.faturamento(data_inicial_promo,obj.DATA_INICIAL,preco)

                    #Incrementa o faturamento da maquininha
                    valorMaquininha += round(faturamentoParcial,2)

                #Se o evento anterior for ATIVAÇÃO
                if (eventoAnterior == 1):

                    #A data final da ativação se torna a inicial do evento seguinte (desativação)
                    data_fim = obj.DATA_INICIAL

                    #Calcula o faturamento da ativação até a desativação, e a maquininha recebe o valor inicial do faturamento
                    valorMaquininha = round((obj.faturamento(data_inicio,data_fim,preco)/30),2)

                #Armazena o tipo do evento atual, para verificar posteriormente qual o evento anterior
                eventoAnterior = obj.EVENTO

            #Se o evento for do tipo MUDANÇA DE PREÇO
            elif (obj.EVENTO == 3):

                #Se não houver uma ativação, verifica próximo evento
                if (data_inicio == ''):
                    continue

                #Se não houver uma ativação após desativação, verifica próximo evento
                if (eventoAnterior == 2):
                    continue

                #Se o evento anterior for do tipo mudança de preço
                if (eventoAnterior == 3):

                    #Calcula o faturamento do range do evento anterior até o atual e soma o faturamento parcial já existente
                    faturamentoParcial = obj.faturamento(obj.DATA_INICIAL,data_inicio,preco) + parcial

                    #Calcula o faturamento do range do evento atual até o fim do mês
                    faturamentoParcial += obj.faturamento(obj.DATA_INICIAL,data_fim,obj.PRECO)

                    #Maquininha recebe o valor do faturamento
                    valorMaquininha = round((faturamentoParcial/30),2)

                #Se o evento anterior for do tipo período promocional
                if(eventoAnterior == 4):

                    #Calcula o faturamento do range do periodo promocional até o fim do mês, pois não há mais eventos após o período promocional
                    faturamentoParcial = obj.faturamento(data_final_promo,data_fim,obj.PRECO) + valorMaquininha

                    #Maquininha recebe o valor do faturamento
                    valorMaquininha = round((faturamentoParcial/30),2)

                if(eventoAnterior == 1):

                    #Calcula faturamento da data de ativação até a mudança de preço
                    faturamentoParcial = obj.faturamento(data_inicio,obj.DATA_INICIAL,preco)

                    #Armazena valor do faturamento parcial para ser acessado posteriormente
                    parcial = faturamentoParcial

                    #Variavel "preco" recebe o valor do evento atual (mudança de preço)
                    preco = obj.PRECO

                    #Variavel "data_inicio" recebe a data inicial do evento atual (mudança de preço)
                    data_inicio = obj.DATA_INICIAL

                    #Calcula o faturamento do range do fim da mudança de preço até o fim do mês (caso não haja eventos posteriores)
                    diferencaDias = abs((data_fim - obj.DATA_INICIAL).days)+1
                    faturamentoParcial += (diferencaDias*preco)

                    #Maquininha recebe o valor do faturamento
                    valorMaquininha = round((faturamentoParcial/30),2)

                #Armazena o tipo do evento atual, para verificar posteriormente qual o evento anterior
                eventoAnterior = obj.EVENTO

            #Se o evento for do tipo PERÍODO PROMOCIONAL
            elif (obj.EVENTO == 4):

                #Se não houver uma ativação, verifica próximo evento
                if (data_inicio == ''):
                    continue

                #Armazena a data inicial e final do periodo promocional
                data_inicial_promo = obj.DATA_INICIAL
                data_final_promo = obj.DATA_FINAL

                #Se o evento anterior é uma mudança de preço, e sua data inicial é anterior a data inicial do periodo promocional
                if (data_inicial_promo > data_inicio and eventoAnterior ==3):

                    #Calcula o range de datas do periodo promocional
                    diferencaDias = abs((data_inicial_promo - data_final_promo).days)+1

                    #Decrementa o valor do fatumento do periodo promocional e recebe o faturamento total da maquininha
                    valorMaquininha = round((faturamentoParcial - (diferencaDias*preco)),2)
                    #valorMaquininha += diferencaDias*obj.PRECO
                    valorMaquininha = round((valorMaquininha/30),2)

                #Se o evento anterior foi uma ativação e sua data é anterior ao periodo promocional
                if (data_inicial_promo > data_inicio and eventoAnterior == 1):

                    #Calcula o faturamento do range da data inicial de ativação até o Periodo Promocional
                    faturamentoParcial = obj.faturamento(data_inicio,data_inicial_promo,preco)

                    #Calcula o range de datas do periodo promocional
                    diferencaDias = abs((data_final_promo - data_inicial_promo).days)+1

                    #Calcula a soma dos faturamentos parciais
                    faturamentoParcial += (diferencaDias*obj.PRECO)

                    #Maquininha recebe valor do faturamento
                    valorMaquininha = round((faturamentoParcial),2)

                    # Armazena o tipo do evento atual, para verificar posteriormente qual o evento anterior
                    eventoAnterior = obj.EVENTO
                    preco = obj.PRECO

    #Adiciona o resultado em uma lista
    saidaDados.append(str(id_maq) + ";" + str(valorMaquininha) + "\n")

#Armazena o resultado em um arquivo csv
cabecalho = "id;valor_faturado\n"
arq = open("faturamentos.csv", "w")
arq.write(cabecalho)
arq.writelines(saidaDados)
arq.close()

#Plot gráficos para melhor visualização dos resultados
interface = Interface(saidaDados)
