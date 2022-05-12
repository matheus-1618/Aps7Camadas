
#importe as bibliotecas
from django.dispatch import Signal
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import soundfile as sf


class Encode:
    def __init__(self) -> None:
        self.signal = signalMeu()
        self.fs = 44100
        self.A = 1 
        self.T = 10
        self.t = np.linspace(-self.T/2,self.T/2,self.T*self.fs)
        print("--->Inicializando encoder\n")
        self.freqs = [[1206,1339,1477,1633],[697,770,852,941]]
        self.tecla_0 = [self.freqs[0][1],self.freqs[1][3]]
        self.tecla_1 = [self.freqs[0][0],self.freqs[1][0]]
        self.tecla_2 = [self.freqs[0][1],self.freqs[1][0]]
        self.tecla_3 = [self.freqs[0][2],self.freqs[1][0]]
        self.tecla_4 = [self.freqs[0][0],self.freqs[1][1]]
        self.tecla_5 = [self.freqs[0][1],self.freqs[1][1]]
        self.tecla_6 = [self.freqs[0][2],self.freqs[1][1]]
        self.tecla_7 = [self.freqs[0][0],self.freqs[1][2]]
        self.tecla_8 = [self.freqs[0][1],self.freqs[1][2]]
        self.tecla_9 = [self.freqs[0][2],self.freqs[1][2]]
        self.feq1 = None 
        self.feq2 = None
        print("--->Aguardando usuário...\n")
        img = mpimg.imread('table.png')
        imgplot = plt.imshow(img)
        plt.show()
        self.get_tecla = int(input("Digite aqui um tecla de 0 a 9 que você quer simular: \n"))
        exec(f'self.feq1,self.feq2 = self.tecla_{self.get_tecla}')
        print(f'Frequencia 1: {self.feq1}')
        print(f'Frequência 2: {self.feq2}')
        self.x1,self.x2,self.s1,self.s2,self.s = None,None,None,None,None
        self.X,self.Y = [], []

#funções a serem utilizadas
    def signal_handler(self,signal, frame):
            print('You pressed Ctrl+C!')
            sys.exit(0)

    #converte intensidade em Db, caso queiram ...
    def todB(self,s):
        sdB = 10*np.log10(s)
        return(sdB)

    def plotSin(self,signaltype:int):
        if signaltype in [1,2]:
            freq = f"'Frequência {signaltype}'"
            print(f"-->Gerando gráfico da frequência {signaltype}\n")
            exec(f'self.signal.plotSin(self.x{signaltype},self.s{signaltype},{freq})')
        else:
            print(f"-->Gerando gráfico da frequência combinada\n")
            self.signal.plotSin(self.x1,self.s,"Frequência combinada")

    def main(self):
        #********************************************instruções*********************************************** 
        # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
        # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
        # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
        # se voce quiser, pode usar a funcao de construção de senoides existente na biblioteca de apoio cedida. Para isso, você terá que entender como ela funciona e o que são os argumentos.
        # essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
        # lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
        # o tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Seja razoável.
        # some as senoides. A soma será o sinal a ser emitido.
        # utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
        # grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
        
        # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
        print("Gerando Tons base")
        print("Executando as senoides (emitindo o som)")
        print("Gerando Tom referente ao símbolo : {}".format(self.get_tecla))
        self.x1,self.s1 = self.signal.generateSin(self.feq1,self.A,self.T,self.fs)
        self.x2,self.s2 = self.signal.generateSin(self.feq2,self.A,self.T,self.fs)
        self.s = self.s1 + self.s2
        self.plotSin(1)
        self.plotSin(2)
        self.plotSin(0)
        sd.play(self.s, self.fs)
        sd.wait()

        X,Y = self.signal.calcFFT(self.s,self.fs)
        Ymax = sorted(Y)[-2:]
        pico1,pico2 = list(Y).index(Ymax[0]),list(Y).index(Ymax[1])
        print(f'Picos são:\nPico 1: {X[pico1]:.1f}\nPico 2: {X[pico2]:.1f}')
        self.signal.plotFFT(self.s,self.fs)
        filename = 'output.wav'
        sf.write(filename, self.s, self.fs)

    

if __name__ == "__main__":
    a = Encode()
    a.main()
