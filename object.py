from datetime import datetime


#Classe que representa eventos de uma maquininha
class Object:

    #Inicializa os atributos do objeto com -1
    ID = -1
    PRECO = -1
    EVENTO = -1
    DATA_INICIAL = -1
    DATA_FINAL = -1

    #Construtor da classe que instancia um objeto
    def __init__(self, line):
        if(line[0] != 'NULL'):
            self.ID = int(line[0])

        if(line[1] != 'NULL'):
            #Trata quando o preço é vazio (Evento Desativação)
            if line[1] == '':
                self.PRECO = 'NULL'
            else:
                self.PRECO = round(float(line[1]),2)

        if(line[2] != 'NULL'):
            #Remove os espaços em branco antes e após a string
            line[2] = line[2].strip()

            #Verifica o nome do evento e define uma identificação numérica para o mesmo
            if line[2] == 'Ativação':
                self.EVENTO = 1
            if line[2] == 'Desativação':
                self.EVENTO = 2
            if line[2] == 'Mudança de Preço':
                self.EVENTO = 3
            if line[2] == 'Período Promocional':
                self.EVENTO = 4

        if(line[3] != 'NULL'):
            #Transforma a data no time datetime
            self.DATA_INICIAL = datetime.strptime(line[3], '%d-%m-%Y').date()

        if(line[4] != 'NULL'):
            #Trata quando a data final é vazia
            if (line[4] == ''):
                self.DATA_FINAL = 'NULL'
            else:
                self.DATA_FINAL = datetime.strptime(line[4], '%d-%m-%Y').date()

    def getDataInicio(self):
        return self.DATA_INICIAL

    def getID(self):
        return self.ID

    #Método que calcula o range entre datas do período de ativação, e a soma de seu respectivo valor gerando o faturamento de um evento
    def rangeDataAtivacao(self,dtInicial, dtFinal, valor):
        primeiroDiaMes = datetime.strptime('01-01-2021', '%d-%m-%Y').date()

        # Se o número do dia da data inicial for diferente de "01", acrescenta 1 ao range
        if (dtInicial != primeiroDiaMes):

            #Verifica o range entre datas e soma o preço para cada dia
            diferencaDias = abs((dtFinal - dtInicial).days) + 1
            valorMaquininha = round(((valor * diferencaDias) / 30), 2)
            return valorMaquininha
        else:

            #Verifica o range entre datas e soma o preço para cada dia
            diferencaDias = abs((dtFinal - dtInicial).days)
            valorMaquininha = round(((valor * diferencaDias) / 30), 2)
            return valorMaquininha

    #Método que calcula o range entre as datas dos eventos, e a soma do seu respectivo valor gerando o faturamento de um evento
    def faturamento(self, dtInicial, dtFinal, valorAtual):
        diferencaDias = abs((dtFinal - dtInicial).days)
        faturamentoParcial = diferencaDias * valorAtual
        return faturamentoParcial