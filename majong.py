from operator import truediv
from turtle import back
import console
import time
from colorama import Back,Fore,Style
import math as math
from pynput.keyboard import Key, Listener






debounce = False
def main(): #função de começar o jogo, toda vez que for chamada, volta pro menu principal

    botoesMenu = ["JOGAR","DIFICULDADE","TUTORIAL","SAIR"]

    tempo = 0
    debounce = False
    while debounce == False:

        def nome(tempo):

            def valorOffset(linha):
                valor = 90 * linha
                return round(math.sin(valor * math.pi / 180.0))

            def criarPontinhos(a):
                return a % 4 * '.'



            console.clear()
            print('\n'*8)
            print(Fore.LIGHTRED_EX + " " * (48 + valorOffset(tempo)) + "███╗   ███╗ █████╗ ██╗  ██╗     ██╗ ██████╗ ███╗   ██╗ ██████╗")
            print( " " * (48 + valorOffset(tempo+1)) + "████╗ ████║██╔══██╗██║  ██║     ██║██╔═══██╗████╗  ██║██╔════╝")
            print( " " * (48 + valorOffset(tempo+2)) +"██╔████╔██║███████║███████║     ██║██║   ██║██╔██╗ ██║██║  ███╗")
            print( " " * (48 + valorOffset(tempo+3)) + "██║╚██╔╝██║██╔══██║██╔══██║██   ██║██║   ██║██║╚██╗██║██║   ██║")
            print( " " * (48 + valorOffset(tempo+4)) + "██║ ╚═╝ ██║██║  ██║██║  ██║╚█████╔╝╚██████╔╝██║ ╚████║╚██████╔╝")
            print( " " * (48 + valorOffset(tempo+5)) + "╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝" )
            print(Fore.WHITE)
            print('\n'*20)                                                                                    
            print('                                                            PRESSIONE QUALQUER TECLA PRA CONTINUAR' + criarPontinhos(tempo))
        
        
        nome(tempo)
        tempo += 1



    
        def criarQuadrado(texto):
            print(chr(9484) + chr(9472)*11 + chr(9488))
            print(chr(9474) + texto + chr(9474))
            print(chr(9492) + chr(9472)*11 + chr(9496))


        time.sleep(0.25)

    def getKey(key):
        if key:
            debounce == True

    with Listener(on_press = getKey) as listener:   
        listener.join()

main()
