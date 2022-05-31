

import math as math
from select import select
from colorama import Fore
import time
import console
from console import *
import threading
from pynput.keyboard import Listener
import random as random
from random import randrange

def main():
    class global_variables:
        blocos = []
        x = 0
        y = 1
        selected_x = None

        tab = [
        1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1
        ]

        borda_L_E = [0,10,20,30,40,50]
        borda_L_D = [9,19,29,39,49,59]

        difficulty = 4
        name_loop_enabled = True
        menu_enabled = False
        difficulty_enabled = False
        tutorial_enabled = False
        game_enabled = False
        game_started = False
        countdown_enabled = False
        WAIT_TIME = 0.25
        has_pressed = False
        botoes_menu = ["       JOGAR        ","     DIFICULDADE    ","     COMO JOGAR     ","        SAIR        "]
        botoes_dificuldade = ["      INICIANTE     ","     EXPERIENTE     ","        GENIO       ","      EINSTEIN      "]
        sym_lib = ['♥','♦','♣','§','☺','♠','•','♂','♀','♪','♫','►','◄','▲','▼','ø','¶','!','@','#','$','%','&','*']
        num_arr , sym_arr = [] , []
        barrinhas = 120
        countdown_counter = 0


    class gen_f:

        def get_offset_value(line_num): #given a line, it'll return an offset ranging from -1 to 1 and used on the name_handler function
            v = 90 * line_num #multiplies line_num by 90 to get the next sin value
            return round(math.sin(v * math.pi / 180.0)) #returns sin of v, ranging from -1 to 1

        def dots_handler(currentC): #handles the dots below the mahjong main title
            return currentC % 4 * '.' #returns a different amount of dots depending on the current counter number

        def getSelectedArr(num): #given the length of an array of buttons, returns array of 0s and 1s depending on CURRENT_SELECTED_Y
            selectedArr = []
            for i in range(num):
                if i+1 == global_variables.y: 
                    selectedArr.append(1)
                else:
                    selectedArr.append(0)
            return selectedArr

        def find_col(x,y):
            if 10*(y-1) + x == global_variables.selected_x:
                return 2
            elif 10*(y-1) + x == global_variables.x:
                return 1
            else:
                return 0


        def randomizer():
            #procurar nil
            #guardar posição nil
            #tirar nil
            #shuffle
            #adicionar nil insert()
            posicoes_sem_carta_array = []
            contador = 0
            try:
                for i in global_variables.tab:
                    if global_variables.num_arr[contador] == 'nil':
                        posicoes_sem_carta_array.append(contador)

                    contador += 1
                for i in posicoes_sem_carta_array:
                        global_variables.num_arr.remove('nil')
            except:
                pass        

            random.shuffle(global_variables.num_arr)

            for i in range(len(posicoes_sem_carta_array)):
                global_variables.num_arr.insert(posicoes_sem_carta_array[i],'nil')

        def gerar_array_simbolo_e_numero():
            for i in range(int(len(global_variables.tab)/2)):
                r_number = randrange(4) + 1
                r_symbol = global_variables.sym_lib[randrange(24)]
                concat = f'{r_number}{r_symbol}'
                global_variables.num_arr.append(concat)
                global_variables.num_arr.append(concat)

        def print_block(x,y,sym,num,color): 

            if color == 1:
                print(Fore.LIGHTYELLOW_EX)
            elif color == 2:
                print(Fore.LIGHTGREEN_EX)
            else:
                print(Fore.WHITE)
            gotoxy(x,y)
            print(chr(9484) + chr(9472)*3 + chr(9488))
            gotoxy(x,y+1)
            print(chr(9474) + str(num) + '  ' + chr(9474))
            gotoxy(x,y+2)
            print(chr(9474) +' '+  str(sym) +' '+ chr(9474))
            gotoxy(x,y+3)
            print(chr(9474) + '  ' + str(num) + chr(9474))
            gotoxy(x,y+4)
            print(chr(9492) + chr(9472)*3 + chr(9496))

        def compare_block():
            a = global_variables.x
            b = global_variables.selected_x
            def comparar_x_com_valor_borda(array,x,soma):
                contador_comparar_x_com_valor_borda = 0
                for valor_borda in array:
                    if x == valor_borda:
                        array[contador_comparar_x_com_valor_borda] += soma
                        return True 
                    contador_comparar_x_com_valor_borda += 1      
                return False


            if (global_variables.num_arr[b] == global_variables.num_arr[a]) and (a!=b) and (comparar_x_com_valor_borda(global_variables.borda_L_E,global_variables.x,1) or comparar_x_com_valor_borda(global_variables.borda_L_D,global_variables.x,-1)) and (comparar_x_com_valor_borda(global_variables.borda_L_E,global_variables.selected_x,1) or comparar_x_com_valor_borda(global_variables.borda_L_D,global_variables.selected_x,-1)): 
                global_variables.tab[b] = 0
                global_variables.tab[a] = 0
                global_variables.num_arr[b] = 'nil'
                global_variables.num_arr[a] = 'nil'
                global_variables.selected_x = None
                
                try:
                    add = 1
                    while global_variables.tab[global_variables.x+add] == 0:
                        add += 1
                    global_variables.x += add
                except:
                    add = 1
                    while global_variables.tab[global_variables.x-add] == 0:
                        add -= 1
                    global_variables.x -= add
            else:
                global_variables.selected_x = global_variables.x

        def enter_handler():
            if global_variables.menu_enabled: #if player is looking at main menu, the array will have 4 elements
                arr = gen_f.getSelectedArr(4)
                if arr == [1,0,0,0]:
                    sp_f.game()
                elif arr == [0,1,0,0]:
                    global_variables.y = 1
                    sp_f.menu_screens.difficulty()
                elif arr == [0,0,1,0]:
                    sp_f.menu_screens.tutorial()
                elif arr == [0,0,0,1]:
                    console.clear()
                    quit()

            elif global_variables.difficulty_enabled:
                arr = gen_f.getSelectedArr(4)
                if arr == [1,0,0,0]:
                    global_variables.difficulty = 4
                    sp_f.menu()
                elif arr == [0,1,0,0]:
                    global_variables.difficulty = 3
                    sp_f.menu()
                elif arr == [0,0,1,0]:
                    global_variables.difficulty = 2
                    sp_f.menu()
                elif arr == [0,0,0,1]:
                    global_variables.difficulty = 1
                    sp_f.menu()
            elif global_variables.game_enabled:
                if global_variables.selected_x:
                    gen_f.compare_block()
                else:
                    global_variables.selected_x = global_variables.x

                sp_f.game()

        def create_box(texto,color): #creates a square from a given text
            if color == 1: #if selected, changes color to yellow
                print(Fore.LIGHTYELLOW_EX)
            else:
                print(Fore.WHITE) #else changes color back to white
            print(73*' ' + chr(9484) + chr(9472)*20 + chr(9488)) #top
            print(73*' ' + chr(9474) + texto + chr(9474)) #middle + text
            print(73*' ' + chr(9492) + chr(9472)*20 + chr(9496)) #bottom

    
    class sp_f:
        def start():

            def name_handler(counter): #handles all the name changing every time it is called
                print('\n'*8) #prints 8 empty lines above the mahjong main title
                print(Fore.LIGHTRED_EX) #sets the colors of all lines below to red
                print( " " * (48 + gen_f.get_offset_value(counter  )) + "███╗   ███╗ █████╗ ██╗  ██╗     ██╗ ██████╗ ███╗   ██╗ ██████╗")
                print( " " * (48 + gen_f.get_offset_value(counter+1)) + "████╗ ████║██╔══██╗██║  ██║     ██║██╔═══██╗████╗  ██║██╔════╝")
                print( " " * (48 + gen_f.get_offset_value(counter+2)) + "██╔████╔██║███████║███████║     ██║██║   ██║██╔██╗ ██║██║  ███╗")
                print( " " * (48 + gen_f.get_offset_value(counter+3)) + "██║╚██╔╝██║██╔══██║██╔══██║██   ██║██║   ██║██║╚██╗██║██║   ██║")
                print( " " * (48 + gen_f.get_offset_value(counter+4)) + "██║ ╚═╝ ██║██║  ██║██║  ██║╚█████╔╝╚██████╔╝██║ ╚████║╚██████╔╝")
                print( " " * (48 + gen_f.get_offset_value(counter+5)) + "╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝" )
                print(Fore.WHITE) #sets the colors of all lines below to white
                print('\n'*20) #prints 20 empty lines below                                                                                    
                print('                                                            PRESSIONE ESPAÇO PRA CONTINUAR' + gen_f.dots_handler(counter)) 

        
            def name_loop():
                counter_name_loop = 0
                while global_variables.name_loop_enabled:
                    counter_name_loop += 1
                    time.sleep(global_variables.WAIT_TIME)
                    console.clear()
                    name_handler(counter_name_loop) #CHAMA A FUNÇÃO NAME HANDLER DENTRO DO SPECIFIC_FUNCTIONS

            name_thread = threading.Thread(target=name_loop)
            name_thread.start()

        def menu():

            global_variables.menu_enabled = True
            
            #DEBUG
            global_variables.game_enabled = False
            global_variables.difficulty_enabled = False
            global_variables.tutorial_enabled = False
            global_variables.has_pressed = True
            global_variables.countdown_enabled = False


            console.clear()
            print('\n'*15)
            counter_menu = 0

            for botao in global_variables.botoes_menu:
                gen_f.create_box(botao,gen_f.getSelectedArr(4)[counter_menu])
                counter_menu += 1


        class menu_screens:
            def difficulty():
                global_variables.difficulty_enabled = True

                #DEBUG
                global_variables.menu_enabled = False
                global_variables.tutorial_enabled = False


                console.clear()
                print('\n'*15)
                counter_difficulty = 0
                for botao in global_variables.botoes_dificuldade:
                    gen_f.create_box(botao,gen_f.getSelectedArr(4)[counter_difficulty])
                    counter_difficulty += 1

            def tutorial():
                global_variables.tutorial_enabled = True

                #DEBUG
                global_variables.menu_enabled = False
                global_variables.difficulty_enabled = False

                console.clear()
                print("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")


        def game():
            global_variables.game_enabled = True

            #DEBUG
            global_variables.menu_enabled = False
            global_variables.difficulty_enabled = False
            global_variables.tutorial_enabled = False
            


            console.clear()

            init(160)
            reset(1,2,49, 160)

            if global_variables.game_started == False: #gerar tabuleiro randomizado
                global_variables.game_started = True
                gen_f.gerar_array_simbolo_e_numero()
                gen_f.randomizer()
                
            counter_blockgen = 0
            pos_x = 0
            pos_y = 1
            for block in global_variables.tab:
                if block != 0:
                    pixel_pos_x = (-25 + (160/2) + pos_x * 5)
                    pixel_pos_y = pos_y * 5
                    gen_f.print_block(pixel_pos_x,pixel_pos_y,global_variables.num_arr[counter_blockgen][1:2],global_variables.num_arr[counter_blockgen][0:1],gen_f.find_col(pos_x,pos_y))

                pos_x += 1
                if pos_x >= 10:
                    pos_x = 0
                    pos_y += 1
                counter_blockgen += 1

            def countdown():
                contador = global_variables.difficulty*60
                for i in range(contador):
                    gotoxy(160-3,1)
                    print(contador)
                    contador -= 1
                    time.sleep(1)
                    if global_variables.countdown_enabled == False:
                        break

            if global_variables.countdown_enabled == False:
                global_variables.countdown_enabled = True
                countdown_thread = threading.Thread(target=countdown)
                countdown_thread.start()

            

    sp_f.start()


    class callback:
        def press(key):
            if global_variables.has_pressed == False:
                global_variables.has_pressed == True
                global_variables.name_loop_enabled = False
                time.sleep(0.5)
                menu_thread = threading.Thread(target=sp_f.menu)
                menu_thread.start()
            
            if str(key) == 'Key.up':
                if global_variables.y > 1:
                    global_variables.y -= 1
                if global_variables.menu_enabled:
                    sp_f.menu()
                elif global_variables.difficulty_enabled:
                    sp_f.menu_screens.difficulty()
                elif global_variables.game_enabled:
                    if global_variables.x > 9:
                        
                        add = 10
                    
                        while global_variables.tab[global_variables.x - add] == 0:
                            if global_variables.x - add > 9:
                                add += 10
                            else:
                                add = 0

                        global_variables.x -= add
                        sp_f.game()

            if str(key) == 'Key.down':
                if global_variables.y < 4:
                    global_variables.y += 1
                if global_variables.menu_enabled:
                    sp_f.menu()
                elif global_variables.difficulty_enabled:
                    sp_f.menu_screens.difficulty()
                elif global_variables.game_enabled:
                    if global_variables.x < 50:
                        
                        try:
                            add = 10
                            while global_variables.tab[global_variables.x + add] == 0:
                                add += 10
                        except:
                            add = 0
                        global_variables.x += add
                        sp_f.game()
            
            if str(key) == 'Key.right':
                if global_variables.game_enabled:
                    if global_variables.x < 59:
                        add = 1
                        while global_variables.tab[global_variables.x+add] == 0:
                            add+=1
                        global_variables.x += add
                        sp_f.game()

            if str(key) == 'Key.left':
                if global_variables.game_enabled:
                    if global_variables.x > 0:
                        add = 1
                        while global_variables.tab[global_variables.x-add] == 0:
                            add+=1
                        global_variables.x -= add
                        sp_f.game()

            if str(key) == 'Key.enter':
                gen_f.enter_handler()

            if str(key) == "'f'":
                console.clear()
                sp_f.menu()

            if str(key) == "'r'":
                console.clear()
                gen_f.randomizer()
                sp_f.game()

            if str(key) == 'Key.esc':
                console.clear()
                quit()

        def release(key):
            pass
        
    
    with Listener(on_press=callback.press, on_release=callback.release) as l:
        l.join()


main()
