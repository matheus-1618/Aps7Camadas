#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
import numpy as np
import sounddevice as sd
from scipy import signal
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from suaBibSignal import *
import peakutils
import time
import soundfile as sf


class Decode:
    def __init__(self) -> None:
        print("--->Inicializando decoder\n")
        self.signal = signalMeu()
        self.fs = 44100
        self.A = 2 
        self.T = 5
        self.t = np.linspace(-self.T/2,self.T/2,self.T*self.fs)
        self.freqs = [[1206,1339,1477,1633],[697,770,852,941]]
        self.teclas = {}
        self.teclas['0'] = [self.freqs[0][1],self.freqs[1][3]]
        self.teclas['1'] = [self.freqs[0][0],self.freqs[1][0]]
        self.teclas['2'] = [self.freqs[0][1],self.freqs[1][0]]
        self.teclas['3'] = [self.freqs[0][2],self.freqs[1][0]]
        self.teclas['4'] = [self.freqs[0][0],self.freqs[1][1]]
        self.teclas['5'] = [self.freqs[0][1],self.freqs[1][1]]
        self.teclas['6'] = [self.freqs[0][2],self.freqs[1][1]]
        self.teclas['7'] = [self.freqs[0][0],self.freqs[1][2]]
        self.teclas['8'] = [self.freqs[0][1],self.freqs[1][2]]
        self.teclas['9'] = [self.freqs[0][2],self.freqs[1][2]]
        self.freqcaptada1,self.freqcaptada2 = 0,0
        
    #funcao para transformas intensidade acustica em dB
    def todB(self,s):
        sdB = 10*np.log10(s)
        return(sdB)

    def main_without(self):
        sd.default.samplerate = self.fs
        sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa

        print("-->Gravação irá se iniciar em 3s...\n")
        #time.sleep(3.3)
    
        #faca um print informando que a gravacao foi inicializada
        #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
        #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
        print("-->Gravação Iniciada\n")
        numAmostras = self.fs * self.T
        audio, samplerate = sf.read('output.wav')
        #audio = sd.rec(int(numAmostras), self.fs, channels=1)
        #sd.wait()
        #audio = audio[:,0]
        print("-->Gravação encerrada\n")
        
        #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
        #grave uma variavel com apenas a parte que interessa (dados)
        print("-->Áudio gravado")
        sd.play(audio, samplerate)
        sd.wait()

        # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!

        # plot do gravico  áudio vs tempo!
        self.signal.plotSin(self.t,audio,"Recebido")
        ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias


        xf, yf = self.signal.calcFFT(audio, samplerate)
        self.signal.plotFFT(audio,samplerate)
        
        #esta funcao analisa o fourier e encontra os picos
        #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
        #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
        #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
        index = peakutils.indexes(yf, thres=0.2, min_dist=10)
        print(xf[index])
        for pico in xf[index]:
            for freq1 in self.freqs[0]:
                if freq1-5 < pico < freq1 + 5:
                    self.freqcaptada1 = freq1
            for freq2 in self.freqs[1]:
                if freq2-5 < pico < freq2 + 5:
                    self.freqcaptada2 = freq2 
    
                    
        print(self.freqcaptada1,self.freqcaptada2)
        for tecla in self.teclas:
            if self.teclas[tecla][0] == self.freqcaptada1 and self.teclas[tecla][1] == self.freqcaptada2:
                print(f'A tecla digitada foi: {tecla}')

    def main(self):
    
        #declare um objeto da classe da sua biblioteca de apoio (cedida)    
        #declare uma variavel com a frequencia de amostragem, sendo 44100
        
        #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
        # os seguintes parametros devem ser setados:
        
        sd.default.samplerate = self.fs
        sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa

        print("-->Gravação irá se iniciar em 3s...\n")
        time.sleep(3.3)
    
        #faca um print informando que a gravacao foi inicializada
        #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
        #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
        print("-->Gravação Iniciada\n")
        numAmostras = self.fs * self.T
        audio = sd.rec(int(numAmostras), self.fs, channels=1)
        sd.wait()
        
        print("-->Gravação encerrada\n")
        audio = audio[:,0]
        #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
        #grave uma variavel com apenas a parte que interessa (dados)
        print("-->Áudio gravado")
        sd.play(audio, self.fs)
        sd.wait()

        # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!

        # plot do gravico  áudio vs tempo!
        self.signal.plotSin(self.t,audio,"Recebido")
        ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias


        xf, yf = self.signal.calcFFT(audio, self.fs)
        self.signal.plotFFT(audio,self.fs)
        
        #esta funcao analisa o fourier e encontra os picos
        #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
        #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
        #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
        index = peakutils.indexes(yf, thres=0.2, min_dist=10)
        for pico in xf[index]:
            for freq1 in self.freqs[0]:
                if freq1-5 < pico < freq1 + 5:
                    self.freqcaptada1 = freq1
            for freq2 in self.freqs[1]:
                if freq2-5 < pico < freq2 + 5:
                    self.freqcaptada2 = freq2 
        
        if self.freqcaptada1 == 0 and self.freqcaptada2 == 0:
            print("Repita gravação, erro na captação")
        
        #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
        #print a tecla.
        #print(self.freqcaptada1,self.freqcaptada2)
        for tecla in self.teclas:
            if self.teclas[tecla][0] == self.freqcaptada1 and self.teclas[tecla][1] == self.freqcaptada2:
                print(f'A tecla digitada foi: {tecla}')
        ## Exibe gráficos
        # plt.show()

if __name__ == "__main__":
    a = Decode()
    a.main()
