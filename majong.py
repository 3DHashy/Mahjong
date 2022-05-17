#from operator import truediv
#from turtle import back
import console
import time
from colorama import Back,Fore,Style
import math as math
from pynput.keyboard import Key, Listener
import threading

def get_offset_value(lineNum):
    v = 90 * lineNum
    return round(math.sin(v * math.pi / 180.0))

def dots_handler(currentC):
    return currentC % 4 * '.'


def name_handler(counter):
           print('\n'*8)
           print(Fore.LIGHTRED_EX)
           print( " " * (48 + get_offset_value(counter  )) + "███╗   ███╗ █████╗ ██╗  ██╗     ██╗ ██████╗ ███╗   ██╗ ██████╗")
           print( " " * (48 + get_offset_value(counter+1)) + "████╗ ████║██╔══██╗██║  ██║     ██║██╔═══██╗████╗  ██║██╔════╝")
           print( " " * (48 + get_offset_value(counter+2)) + "██╔████╔██║███████║███████║     ██║██║   ██║██╔██╗ ██║██║  ███╗")
           print( " " * (48 + get_offset_value(counter+3)) + "██║╚██╔╝██║██╔══██║██╔══██║██   ██║██║   ██║██║╚██╗██║██║   ██║")
           print( " " * (48 + get_offset_value(counter+4)) + "██║ ╚═╝ ██║██║  ██║██║  ██║╚█████╔╝╚██████╔╝██║ ╚████║╚██████╔╝")
           print( " " * (48 + get_offset_value(counter+5)) + "╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝" )
           print(Fore.WHITE)
           print('\n'*20)                                                                                    
           print('                                                            PRESSIONE QUALQUER TECLA PRA CONTINUAR' + dots_handler(counter))


def main():
    #Draw start screen: Mahjong + Press any key to continue
    run = True
    WAIT_TIME = 0.25

    def name_loop():
        ctr = 0
        while run:
            time.sleep(WAIT_TIME)
            console.clear()
            name_handler(ctr)

            ctr += 1


    name_thread = threading.Thread(target=name_loop)
    name_thread.start()


    def press(key):
        run = False
    
    def release(key):
        pass

    with Listener(on_press=press, on_release=release) as l:
        l.join()




    run = False
    


main()

#debounce = False
#def main(): #função de começar o jogo, toda vez que for chamada, volta pro menu principal
#
#    botoesMenu = ["JOGAR","DIFICULDADE","TUTORIAL","SAIR"]
#
#    tempo = 0
#    debounce = False
#    while debounce == False:
#
#        def nome(tempo):
#
#            def valorOffset(linha):
#                valor = 90 * linha
#                return round(math.sin(valor * math.pi / 180.0))
#
#            def criarPontinhos(a):
#                return a % 4 * '.'
#
#
#
#            console.clear()
#            print('\n'*8)
#            print(Fore.LIGHTRED_EX + " " * (48 + valorOffset(tempo)) + "███╗   ███╗ █████╗ ██╗  ██╗     ██╗ ██████╗ ███╗   ██╗ ██████╗")
#            print( " " * (48 + valorOffset(tempo+1)) + "████╗ ████║██╔══██╗██║  ██║     ██║██╔═══██╗████╗  ██║██╔════╝")
#            print( " " * (48 + valorOffset(tempo+2)) +"██╔████╔██║███████║███████║     ██║██║   ██║██╔██╗ ██║██║  ███╗")
#            print( " " * (48 + valorOffset(tempo+3)) + "██║╚██╔╝██║██╔══██║██╔══██║██   ██║██║   ██║██║╚██╗██║██║   ██║")
#            print( " " * (48 + valorOffset(tempo+4)) + "██║ ╚═╝ ██║██║  ██║██║  ██║╚█████╔╝╚██████╔╝██║ ╚████║╚██████╔╝")
#            print( " " * (48 + valorOffset(tempo+5)) + "╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝" )
#            print(Fore.WHITE)
#            print('\n'*20)                                                                                    
#            print('                                                            PRESSIONE QUALQUER TECLA PRA CONTINUAR' + criarPontinhos(tempo))
#        
#        
#        nome(tempo)
#        tempo += 1
#
#
#
#    
#        def criarQuadrado(texto):
#            print(chr(9484) + chr(9472)*11 + chr(9488))
#            print(chr(9474) + texto + chr(9474))
#            print(chr(9492) + chr(9472)*11 + chr(9496))
#
#
#        time.sleep(0.25)
#
#    def press(key):
#        print(key)
#    
#    def release(key):
#        if key == Key.enter:
#            debounce = True
#            return False
#
#    with Listener(on_press = press, on_release=release) as listener:   
#        listener.join()
#
#main()
