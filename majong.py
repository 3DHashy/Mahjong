#from operator import truediv
#from turtle import back
import console
from console import *
import time
from colorama import Back,Fore,Style
import math as math
from pynput.keyboard import Key, Listener
import threading

number_of_buttons = 4 #total number of buttons on the y axis, to be changed when not in menu
run = True #handles whether name_handler will run or not
debounce = False #did player click? starts with false, changed on line 106
ctrKey = 1 #counts how many keys have been pressed since the starting of the program, used in line 105 & 134
CURRENT_SELECTED_Y = 1 #counter for the current button/card selected
main_menu_enabled = False #changes to True if player is seeing main menu line 59
difficulty_enabled = False
diff_num = 1


def main_game():
    console.clear()
    #tab = [
    #1,1,1,1,1,1,1,1,1,1,
    #1,1,1,1,1,1,1,1,1,1,
    #0,0,1,1,1,1,1,1,0,0,
    #0,0,1,2,2,2,2,1,0,0,
    #0,0,1,2,3,3,2,1,0,0,
    #0,0,1,2,3,3,2,1,0,0,
    #0.0,1,2,2,2,2,1,0,0,
    #0,0,1,1,1,1,1,1,0,0,
    #1,1,1,1,1,1,1,1,1,1,
    #1,1,1,1,1,1,1,1,1,1,
    #]
    tab = [
    1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,
    0,0,1,1,1,1,1,1,0,0,
    0,0,1,2,2,2,2,1,0,0,
    0,0,1,2,3,3,2,1,0,0,
    0.0,1,2,2,2,2,1,0,0,
    0,0,1,1,1,1,1,1,0,0,
    1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,
    ]
    LIMIT_X = 160
    LIMIT_Y = 0
    sym_lib = ['♥','♦','♣','§','☺','♠','•','♂','♀','♪','♫','►','◄','▲','▼','ø','¶','!','@','#','$','%','&','*']

    init(LIMIT_X)
    reset(1,2,LIMIT_Y -1, LIMIT_X)

    def printPeca(x,y,sym,num,color):
        if color == 1:
            print(Fore.LIGHTYELLOW_EX)
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

    
#    for i in tab:
#        if i == 0:
#            pass
#        if
    def create_blocks():
        x_b = -25
        y_b = 1
        ctr = 0
        b_arr = []

        for i in tab:
            if x_b <= 20:
                if tab[ctr] == 0:
                    x_b += 5 
                else:
                    peca = {'x':((LIMIT_X/2) + x_b) ,'y': y_b, 'sym': '♥','num':x_b , 'color':0}
                    b_arr.append(peca)
                    printPeca(peca['x'],peca['y'],peca['sym'],peca['num'],peca['color'])
                    x_b += 5
                    
            else:
                y_b += 5
                x_b = -25
            ctr+=1
        print(b_arr)
                
            

#        for i in b_arr:
#            printPeca(i['x'],i['y'],i['sym'],i['num'],i['color'])


    create_blocks()
    #peca = {'x':(LIMIT_X/2) -5, 'y':1, 'img':sym_lib[0], 'num': 6, 'color':0}
    #printPeca(peca['x'],peca['y'],peca['img'],peca['num'],peca['color'])

    #definir tabuleiro
    #gerar peças nos espaços livres duas em duas
    #definir peças livres e ocupadas

    


def get_offset_value(line_num): #given a line, it'll return an offset ranging from -1 to 1 and used on the name_handler function
    v = 90 * line_num #multiplies line_num by 90 to get the next sin value
    return round(math.sin(v * math.pi / 180.0)) #returns sin of v, ranging from -1 to 1

def dots_handler(currentC): #handles the dots below the mahjong main title
    return currentC % 4 * '.' #returns a different amount of dots depending on the current counter number


def name_handler(counter): #handles all the name changing every time it is called
            print('\n'*8) #prints 8 empty lines above the mahjong main title
            print(Fore.LIGHTRED_EX) #sets the colors of all lines below to red
            print( " " * (48 + get_offset_value(counter  )) + "███╗   ███╗ █████╗ ██╗  ██╗     ██╗ ██████╗ ███╗   ██╗ ██████╗")
            print( " " * (48 + get_offset_value(counter+1)) + "████╗ ████║██╔══██╗██║  ██║     ██║██╔═══██╗████╗  ██║██╔════╝")
            print( " " * (48 + get_offset_value(counter+2)) + "██╔████╔██║███████║███████║     ██║██║   ██║██╔██╗ ██║██║  ███╗")
            print( " " * (48 + get_offset_value(counter+3)) + "██║╚██╔╝██║██╔══██║██╔══██║██   ██║██║   ██║██║╚██╗██║██║   ██║")
            print( " " * (48 + get_offset_value(counter+4)) + "██║ ╚═╝ ██║██║  ██║██║  ██║╚█████╔╝╚██████╔╝██║ ╚████║╚██████╔╝")
            print( " " * (48 + get_offset_value(counter+5)) + "╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝" )
            print(Fore.WHITE) #sets the colors of all lines below to white
            print('\n'*20) #prints 20 empty lines below                                                                                    
            print('                                                            PRESSIONE ESPAÇO PRA CONTINUAR' + dots_handler(counter)) 



def getSelectedArr(num): #given the length of an array of buttons, returns array of 0s and 1s depending on CURRENT_SELECTED_Y
    global CURRENT_SELECTED_Y 
    selectedArr = []
    for i in range(num):
        if i+1 == CURRENT_SELECTED_Y: 
            selectedArr.append(1)
        else:
            selectedArr.append(0)
    return selectedArr




def create_box(texto,color): #creates a square from a given text
    if color == 1: #if selected, changes color to yellow
        print(Fore.LIGHTYELLOW_EX)
    else:
        print(Fore.WHITE) #else changes color back to white
    print(73*' ' + chr(9484) + chr(9472)*20 + chr(9488)) #top
    print(73*' ' + chr(9474) + texto + chr(9474)) #middle + text
    print(73*' ' + chr(9492) + chr(9472)*20 + chr(9496)) #bottom

def main_menu(): #everytime this function is called, it'll clear the console and print the main menu
    global main_menu_enabled #imports global variable main_menu_enabled to handle changes
    main_menu_enabled = True
    global difficulty_enabled
    difficulty_enabled = False
    console.clear() #clears
    botoes_menu = ["       JOGAR        ","     DIFICULDADE    ","     COMO JOGAR     ","        SAIR        "]
    print('\n'*15) #15 clear lines
    counter = 0 #starts from the first term of the menu
    for x in botoes_menu: #for each button in botoes_menu add a new button and pass color
        create_box(x,getSelectedArr(4)[counter])
        counter += 1

def difficulty():
    console.clear()

    global difficulty_enabled
    difficulty_enabled = True
    global main_menu_enabled
    main_menu_enabled = False

    dificuldade_arr = ["      INICIANTE     ","     EXPERIENTE     ","        GENIO       ","      EINSTEIN      "]
    print('\n'*15)
    counter_dif = 0
    for x in dificuldade_arr:
        create_box(x,getSelectedArr(4)[counter_dif])
        counter_dif += 1



def enter_handler(): #handles every enter key press
    global main_menu_enabled
    if main_menu_enabled: #if player is looking at main menu, the array will have 4 elements
        arr = getSelectedArr(4)
        if arr == [1,0,0,0]:
            main_game()
        elif arr == [0,1,0,0]:
            global CURRENT_SELECTED_Y
            CURRENT_SELECTED_Y = 1
            difficulty()
        elif arr == [0,0,1,0]:
            print('clicou como jogar')
            console.clear()
            print("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
        elif arr == [0,0,0,1]:
            console.clear()
            quit()

    elif difficulty:
        arr = getSelectedArr(4)
        global diff_num
        if arr == [1,0,0,0]:
            diff_num = 1
            main_menu()
        elif arr == [0,1,0,0]:
            diff_num = 2
            main_menu()
        elif arr == [0,0,1,0]:
            diff_num = 3
            main_menu()
        elif arr == [0,0,0,1]:
            diff_num = 4
            main_menu()

def main(): #draws start screen: Mahjong + Press any key to continue, handles kb presses
    

    WAIT_TIME = 0.25

    def name_loop():
        ctr = 0
        global run
        while run: #main name loop
            ctr += 1
            time.sleep(WAIT_TIME)
            console.clear()
            name_handler(ctr)



    #creating new thread for name loop
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
                if main_menu_enabled:
                    main_menu()
                elif difficulty_enabled:
                    difficulty()
                


        if str(key) == 'Key.down':
            global number_of_buttons
            if CURRENT_SELECTED_Y < number_of_buttons:
                CURRENT_SELECTED_Y += 1
                if main_menu_enabled:
                    main_menu()
                elif difficulty_enabled:
                    difficulty()

        if str(key) == 'Key.enter':
            enter_handler()


        if str(key) == 'Key.esc':
            console.clear()
            quit()
        
        if str(key) == "'f'":
            console.clear()
            main_menu()
        
        ctrKey += 1
    
    def release(key):
        pass

    with Listener(on_press=press, on_release=release) as l:
        l.join()



    


main()
