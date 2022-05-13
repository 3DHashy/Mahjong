from turtle import back
import console
import time
from pynput.keyboard import Key, Listener
from colorama import Back,Fore,Style
import math as math

console.clear()



def comecarJogo():
    i = 1
    sum = 1
    botoesMenu = ["JOGAR","DIFICULDADE","TUTORIAL","SAIR"]
    def ondaNome(offset):
        console.clear()
        print('\n')
        print('\n')
        print('\n')
        print('\n') 
        print(Fore.LIGHTRED_EX + " " * (48 + offset ) + "███╗   ███╗ █████╗ ██╗  ██╗     ██╗ ██████╗ ███╗   ██╗ ██████╗")
        print( " " * (48 + offset * 2) + "████╗ ████║██╔══██╗██║  ██║     ██║██╔═══██╗████╗  ██║██╔════╝")
        print( " " * (48 + offset * 2) +"██╔████╔██║███████║███████║     ██║██║   ██║██╔██╗ ██║██║  ███╗")
        print( " " * (48 + offset * 2) + "██║╚██╔╝██║██╔══██║██╔══██║██   ██║██║   ██║██║╚██╗██║██║   ██║")
        print( " " * (48 + offset) + "██║ ╚═╝ ██║██║  ██║██║  ██║╚█████╔╝╚██████╔╝██║ ╚████║╚██████╔╝")
        print( " " * (48 + offset) + "╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝" )
        print(Fore.WHITE)
        print('\n')
        print('\n')
        print('\n')
        print('\n')                                                                                         
        print('                                                            PRESSIONE QUALQUER TECLA PRA CONTINUAR')
    
    def criarQuadrado(texto):
        print(chr(9484) + chr(9472)*11 + chr(9488))
        print(chr(9474) + texto + chr(9474))
        print(chr(9492) + chr(9472)*11 + chr(9496))

    #for i in range(botoesMenu):
        # criarQuadrado(i)
    while True:
        #i = int(abs(2 * math.sin(x * math.pi / 180.0 )))

        if i == -2 or i == 2:
            sum = sum * (-1)
        i = i + sum
        ondaNome(i)
        time.sleep(0.25)


comecarJogo()

#def getKey(key):
    #print(key)



#with Listener(on_press = getKey) as listener:   
    #listener.join()
