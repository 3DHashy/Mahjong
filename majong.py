#from operator import truediv
#from turtle import back
from select import select
import console
import time
from colorama import Back,Fore,Style
import math as math
from pynput.keyboard import Key, Listener
import threading

number_of_buttons = 4
run = True
debounce = False
ctrKey = 1
CURRENT_SELECTED_Y = 1

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

def criarQuadrado(texto,cor):
    if cor == 1:
        print(Fore.YELLOW)
    else:
        print(Fore.WHITE)
    print(73*' ' + chr(9484) + chr(9472)*20 + chr(9488))
    print(73*' ' + chr(9474) + texto + chr(9474))
    print(73*' ' + chr(9492) + chr(9472)*20 + chr(9496))

def getColor(num):
    global CURRENT_SELECTED_Y
    selectedArr = []
    for i in range(num):
        if i+1 == CURRENT_SELECTED_Y:
            selectedArr.append(1)
        else:
            selectedArr.append(0)
    return selectedArr

def main_menu():
    console.clear()
    botoes_menu = ["       JOGAR        ","    DIFICULDADE     ","     COMO JOGAR     ","        SAIR        "]
    print('\n'*15)
    counter = 0
    for x in botoes_menu:
        criarQuadrado(x,getColor(4)[counter])
        counter += 1



def main():
    #Draw start screen: Mahjong + Press any key to continue

    WAIT_TIME = 0.25

    def name_loop():
        ctr = 0
        global run
        while run:
            ctr += 1
            time.sleep(WAIT_TIME)
            console.clear()
            name_handler(ctr)

            


    name_thread = threading.Thread(target=name_loop)
    name_thread.start()


    def press(key):
        global debounce
        global ctrKey
        global CURRENT_SELECTED_Y
        if debounce == False and ctrKey >= 1:
            debounce = True
            global run
            run = False
            time.sleep(0.5)
            menu_thread = threading.Thread(target=main_menu)
            menu_thread.start()

        if str(key) == 'Key.up':
            if CURRENT_SELECTED_Y > 1:
                CURRENT_SELECTED_Y -= 1
                main_menu()


        if str(key) == 'Key.down':
            global number_of_buttons
            if CURRENT_SELECTED_Y < number_of_buttons:
                CURRENT_SELECTED_Y += 1
            
            main_menu()
        if str(key) == 'Key.esc':
            quit()
        
        
        ctrKey += 1
    
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
