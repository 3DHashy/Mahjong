from ast import expr_context
import math as math
from types import NoneType
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
        #classe de variáveis globais utilizadas em todo o jogo
        x = 0
        y = 1
        z = 1
        selected_x = None
        selected_z = None
        pontuacao = 0
        ganhou = False

        tab = [[
        1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1
        ],[
        0,0,0,0,0,0,0,0,0,0,
        0,1,1,1,1,1,1,1,1,0,
        0,1,1,1,1,1,1,1,1,0,
        0,1,1,1,1,1,1,1,1,0,
        0,1,1,1,1,1,1,1,1,0,
        0,0,0,0,0,0,0,0,0,0
        ],[
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        0,0,1,1,1,1,1,1,0,0,
        0,0,1,1,1,1,1,1,0,0,
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0
        ]]

        borda_E = [[0,10,20,30,40,50],[11,21,31,41],[22,32]]
        borda_D = [[9,19,29,39,49,59],[18,28,38,48],[27,37]]


        difficulty = 4
        name_loop_enabled = True
        menu_enabled = False
        difficulty_enabled = False
        tutorial_enabled = False
        game_enabled = False
        game_started = False
        countdown_enabled = False
        has_pressed = False
        botoes_menu = ["       JOGAR        ","     DIFICULDADE    ","     COMO JOGAR     ","        SAIR        "]
        botoes_dificuldade = ["      INICIANTE     ","     EXPERIENTE     ","        GÊNIO       ","      EINSTEIN      "]
        sym_lib = ['♥','♦','♣','§','☺','♠','•','♂','♀','♪','♫','►','◄','▲','▼','ø','¶','!','@','#','$','%','&','*']
        num_arr = []
        pressed_esc = False


    class gen_f:
        #classes de funções mais gerais, que não necessariamente são ligadas ao jogo (podem ter mais de um uso)
        def get_offset_value(line_num): 
            #dada uma linha, ela retorna um valor de -1 a 1. usada para setar um offset no nome MAHJONG
            v = 90 * line_num 
            return round(math.sin(v * math.pi / 180.0))

        def dots_handler(currentC): 
            #responsável pelo número de pontos (...) no início do jogo e sua movimentação
            return currentC % 4 * '.'

        def getSelectedArr(num):
            #usando o global y, retorna uma array de 0s e 1s. usado para selecionar cada item do MENU
            selectedArr = []
            for i in range(num):
                if i+1 == global_variables.y: 
                    selectedArr.append(1)
                else:
                    selectedArr.append(0)
            return selectedArr

        def find_col(x,y,z):
            #dados o x,y e z de uma peça, acha a cor que o bloco deve ser pintado (0 = branco, 1 = vermelho, 2 = verde (selecionado))
            if global_variables.z == z or global_variables.selected_z == z:
                if 10*(y-1) + x == global_variables.selected_x and global_variables.selected_z == z:
                    return 2
                elif 10*(y-1) + x == global_variables.x and global_variables.z == z:
                    return 1

                    
            return 0
            


        def randomizer(array,tab):
            #procura nils, guarda suas posições, tira os nils, randomiza a array, coloca de volta os nils em suas respectivas posições
            posicoes_sem_carta_array = []
            contador = 0
            try:
                for i in tab:
                    if array[contador] == 'nil':
                        posicoes_sem_carta_array.append(contador)

                    contador += 1
                for i in posicoes_sem_carta_array:
                        array.remove('nil')
            except:
                pass        

            random.shuffle(array)

            for i in range(len(posicoes_sem_carta_array)):
                array.insert(posicoes_sem_carta_array[i],'nil')

        def gerar_array_simbolo_e_numero(array,tab):
            #dada uma array, gera aleatoriamente uma array de números concatenados com símbolos (ex: ['2♫','1ø','4¶']) e dá append na array original
            concat_array = []
            for _ in range(int(len(tab)/2)):
                r_number = randrange(4) + 1
                r_symbol = global_variables.sym_lib[randrange(24)]
                concat = f'{r_number}{r_symbol}'
                concat_array.append(concat)
                concat_array.append(concat)
            array.append(concat_array)


        def print_block(x,y,sym,num,color): 
            #responsável por printar os blocos no jogo e pintá-los
            if color == 1:
                print(Fore.RED)
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

        def compare_block(array_selected,array_cursor,tab_selected,tab_cursor,borda_E_S,borda_D_S,borda_E_C,borda_D_C):
            #responsável por fazer a comparação entre dois blocos e excluí-los se forem idênticos
            x_cursor = global_variables.x
            x_selected = global_variables.selected_x
            def comparar_x_com_valor_borda(array,x,soma):
                #dado um x, a função retorna True ou False dependendo se esse x estiver na borda ou não
                contador_comparar_x_com_valor_borda = 0
                for valor_borda in array:
                    if x == valor_borda:
                        array[contador_comparar_x_com_valor_borda] += soma
                        return True 
                    contador_comparar_x_com_valor_borda += 1      
                return False

            e = comparar_x_com_valor_borda(borda_E_S,global_variables.selected_x,1)
            f = comparar_x_com_valor_borda(borda_D_S,global_variables.selected_x,-1)
            g = comparar_x_com_valor_borda(borda_E_C,global_variables.x,1)
            h = comparar_x_com_valor_borda(borda_D_C,global_variables.x,-1)


            if (array_selected[x_selected] == array_cursor[x_cursor]) and (x_cursor!=x_selected) and (e or f) and (g or h): 
                #no caso de as duas peças estiverem na borda e forem idênticas
                tab_selected[x_selected] = 0
                tab_cursor[x_cursor] = 0
                array_selected[x_selected] = 'nil'
                array_cursor[x_cursor] = 'nil'
                global_variables.selected_x = None

                
                def return_game_ended(tab):
                    #responsável por checar se o jogo já acabou:
                    for elemento in tab:
                        if elemento == 1:
                            return False
                        return True

                #chama a função responsável pela checagem se o jogo acabou
                if return_game_ended(global_variables.tab[0]):
                    global_variables.ganhou = True
                    sp_f.end_game('Win')
                
                #após retirar a carta, o cursor deve mudar para uma carta ou a direita dela (try) ou, se não existir, a esquerda (except)
                try:
                    add = 1
                    while global_variables.tab[global_variables.z -1][global_variables.x+add] == 0:
                        add += 1
                    global_variables.x += add
                    if global_variables.tab[2][global_variables.x] != 0:
                        global_variables.z = 3
                    elif global_variables.tab[1][global_variables.x] != 0:
                        global_variables.z = 2
                    else:
                        global_variables.z = 1
                    
                except:
                    add = 1
                    while global_variables.tab[global_variables.z -1][global_variables.x-add] == 0:
                        add -= 1
                    global_variables.x -= add
                    if global_variables.tab[2][global_variables.x] != 0:
                        global_variables.z = 3
                    elif global_variables.tab[1][global_variables.x] != 0:
                        global_variables.z = 2
                    else:
                        global_variables.z = 1
                

            else:
                #se no caso de as cartas não forem idênticas, seleciona a carta que o cursor está no momento
                global_variables.selected_x = global_variables.x
                global_variables.selected_z = global_variables.z

        def enter_handler():
            #responsável por ditar o que acontece quando o jogador aperta enter, dado onde ele está no jogo no momento
            #se o jogador estiver no MENU:
            if global_variables.menu_enabled: 
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

            #se o jogador estiver na tela de DIFICULDADE:
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

            #se o jogador estiver no JOGO:
            elif global_variables.game_enabled:
                if type(global_variables.selected_x) != NoneType:
                    z_cursor = global_variables.z - 1
                    z_selected = global_variables.selected_z - 1
                    gen_f.compare_block(global_variables.num_arr[z_selected], global_variables.num_arr[z_cursor],global_variables.tab[z_selected],global_variables.tab[z_cursor],global_variables.borda_E[z_selected],global_variables.borda_D[z_selected],global_variables.borda_E[z_cursor],global_variables.borda_D[z_cursor])
                else:
                    global_variables.selected_x = global_variables.x
                    global_variables.selected_z = global_variables.z

                sp_f.game()

        def create_box(texto,color):
            #cria as caixas do menu, diferente das peças do jogo
            if color == 1: 
                print(Fore.RED)
            else:
                print(Fore.WHITE) 
            print(73*' ' + chr(9484) + chr(9472)*20 + chr(9488)) 
            print(73*' ' + chr(9474) + texto + chr(9474)) 
            print(73*' ' + chr(9492) + chr(9472)*20 + chr(9496)) 

    
    class sp_f:
        #classe de funções específicas do jogo
        def start():
            #é a tela que aparece o nome MAHJONG que se mexe
            def name_handler(counter):
                #toda vez que for chamada, printa o nome com um offset variado
                print('\n'*8)
                print(Fore.RED)
                print( " " * (48 + gen_f.get_offset_value(counter  )) + "███╗   ███╗ █████╗ ██╗  ██╗     ██╗ ██████╗ ███╗   ██╗ ██████╗")
                print( " " * (48 + gen_f.get_offset_value(counter+1)) + "████╗ ████║██╔══██╗██║  ██║     ██║██╔═══██╗████╗  ██║██╔════╝")
                print( " " * (48 + gen_f.get_offset_value(counter+2)) + "██╔████╔██║███████║███████║     ██║██║   ██║██╔██╗ ██║██║  ███╗")
                print( " " * (48 + gen_f.get_offset_value(counter+3)) + "██║╚██╔╝██║██╔══██║██╔══██║██   ██║██║   ██║██║╚██╗██║██║   ██║")
                print( " " * (48 + gen_f.get_offset_value(counter+4)) + "██║ ╚═╝ ██║██║  ██║██║  ██║╚█████╔╝╚██████╔╝██║ ╚████║╚██████╔╝")
                print( " " * (48 + gen_f.get_offset_value(counter+5)) + "╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝" )
                print(Fore.WHITE) 
                print('\n'*20)                                                                        
                print('                                                            PRESSIONE ESPAÇO PRA CONTINUAR' + gen_f.dots_handler(counter)) 

        
            def name_loop():
                #função que chama o nome com um offset diferente (counter)
                counter_name_loop = 0
                while global_variables.name_loop_enabled:
                    counter_name_loop += 1
                    time.sleep(0.25)
                    console.clear()
                    name_handler(counter_name_loop)

            #criação de uma thread única para mover o nome
            name_thread = threading.Thread(target=name_loop)
            name_thread.start()

        def menu():
            #tela do menu com 4 botões
            #toda vez que é chamada, dá clear e imprime o menu novamente com cursor (bloco pintado) diferente
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
            #classe de telas do menu, são elas: dificuldade e tutorial
            def difficulty():
                #novamente, dá clear e printa dificuldade (muito parecido com o menu)
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
                #dá clear e printa o tutorial do jogo
                global_variables.tutorial_enabled = True

                #DEBUG
                global_variables.menu_enabled = False
                global_variables.difficulty_enabled = False

                console.clear()
                print("""
                Objetivo do jogo:
                 
                -Combinar todas as peças todas as peças do tabuleiro antes que o tempo acabe.

                Peças Abertas:

                -Diz-se que uma peça está aberta ou exposta se puder ser movida para a esquerda ou para a direita sem perturbar outras peças.

                -Duas peças abertas idênticas podem ser combinadas para liberar um espaço no tabuleiro.

                Como jogar:

                -O jogador deve combinar todas as peças abertas do tabuleiro antes que o tempo acabe.

                -Use as setas do teclado para mover o cursor.

                -Pressione Enter para selecionar duas peças e combiná-las.

                -Ficou preso? pressione R para randomizar as peças do tabuleiro atual.

                -Pressione F para voltar para o menu.

                -Pressione Esc a qualquer momento para sair do jogo.



                PRESSIONE F PARA VOLTAR

                BOM JOGO !!!

                """)


        def game():
            #função do jogo principal, dá clear e printa todas as cartas do jogo toda vez que é chamada
            global_variables.game_enabled = True

            #DEBUG
            global_variables.menu_enabled = False
            global_variables.difficulty_enabled = False
            global_variables.tutorial_enabled = False
            


            console.clear()

            init(160)
            reset(1,2,49, 160)

            if global_variables.game_started == False:
                #gerar todas as camadas do tabuleiro randomizado
                global_variables.game_started = True
                gen_f.gerar_array_simbolo_e_numero(global_variables.num_arr,global_variables.tab[0])
                gen_f.gerar_array_simbolo_e_numero(global_variables.num_arr,global_variables.tab[1])
                gen_f.gerar_array_simbolo_e_numero(global_variables.num_arr,global_variables.tab[2])
                gen_f.randomizer(global_variables.num_arr[0],global_variables.tab[0])
                gen_f.randomizer(global_variables.num_arr[1],global_variables.tab[1])
                gen_f.randomizer(global_variables.num_arr[2],global_variables.tab[2])

            # gera todas as camadas:   
            counter_blockgen = 0
            pos_x = 0
            pos_y = 1
            for block in global_variables.tab[0]:
                if block != 0:
                    pixel_pos_x = (-25 + (160/2) + pos_x * 5)
                    pixel_pos_y = pos_y * 5
                    #o [1:2] pega o símbolo pois a array concatenada tem cada elemento assim '1♠', mesmo princípio com [0:1] (nesse caso, pega o número)
                    gen_f.print_block(pixel_pos_x,pixel_pos_y,global_variables.num_arr[0][counter_blockgen][1:2],global_variables.num_arr[0][counter_blockgen][0:1],gen_f.find_col(pos_x,pos_y,1))

                pos_x += 1
                if pos_x >= 10:
                    pos_x = 0
                    pos_y += 1
                counter_blockgen += 1

            counter_blockgen_2 = 0
            pos_x_2 = 0
            pos_y_2 = 1

            for block in global_variables.tab[1]:
                if block != 0:
                    pixel_pos_x = (-25 + (160/2) + pos_x_2 * 5) -1
                    pixel_pos_y = pos_y_2 * 5 -1
                    gen_f.print_block(pixel_pos_x,pixel_pos_y,global_variables.num_arr[1][counter_blockgen_2][1:2],global_variables.num_arr[1][counter_blockgen_2][0:1],gen_f.find_col(pos_x_2,pos_y_2,2))

                pos_x_2 += 1
                if pos_x_2 >= 10:
                    pos_x_2 = 0
                    pos_y_2 += 1
                counter_blockgen_2 += 1

            counter_blockgen_3 = 0
            pos_x_3 = 0
            pos_y_3 = 1
            
            for block in global_variables.tab[2]:
                if block != 0:
                    pixel_pos_x = (-25 + (160/2) + pos_x_3 * 5) -2
                    pixel_pos_y = pos_y_3 * 5 -2
                    gen_f.print_block(pixel_pos_x,pixel_pos_y,global_variables.num_arr[2][counter_blockgen_3][1:2],global_variables.num_arr[2][counter_blockgen_3][0:1],gen_f.find_col(pos_x_3,pos_y_3,3))

                pos_x_3 += 1
                if pos_x_3 >= 10:
                    pos_x_3 = 0
                    pos_y_3 += 1
                counter_blockgen_3 += 1

            print(Fore.WHITE)
            gotoxy(80-3,35)
            print("Pressione R para randomizar")
            gotoxy(80-3,36)
            print(global_variables.num_arr)

            def countdown():
                #cronometro que fica no canto da tela
                #multiplica pela dificuldade, maior dificuldade = menor tempo
                contador = global_variables.difficulty*240
                if global_variables.countdown_enabled == True:
                    for _ in range(contador*10):
                        print(Fore.WHITE)
                        gotoxy(160-3,1)
                        print("TEMPO: "+str(contador))
                        contador = round(contador - 0.1,1)
                        global_variables.pontuacao = contador * 100
                        time.sleep(0.1)
                        if global_variables.countdown_enabled == False:
                            break
                    if global_variables.ganhou == False:
                        if global_variables.menu_enabled == False:
                            if global_variables.pressed_esc == False:
                                #quando o tempo acabar, o jogador perde
                                sp_f.end_game('Lose')

            #cria uma nova thread para o cronometro somente uma vez
            if global_variables.countdown_enabled == False:
                global_variables.countdown_enabled = True
                countdown_thread = threading.Thread(target=countdown)
                countdown_thread.start()
        
        def end_game(outcome):
            #tela de fim de jogo, depende se o jogador ganhou ou perdeu

            #DEBUG
            global_variables.game_enabled = False
            global_variables.menu_enabled = False
            global_variables.difficulty_enabled = False
            global_variables.tutorial_enabled = False
            global_variables.countdown_enabled = False

            console.clear()

            if outcome == 'Win':
                print('\n'*8)
                print(Fore.GREEN)
                print(30*' ' +'   ▄███████▄    ▄████████    ▄████████    ▄████████ ▀█████████▄     ▄████████ ███▄▄▄▄      ▄████████')
                print(30*' ' +'  ███    ███   ███    ███   ███    ███   ███    ███   ███    ███   ███    ███ ███▀▀▀██▄   ███    ███')
                print(30*' ' +'  ███    ███   ███    ███   ███    ███   ███    ███   ███    ███   ███    █▀  ███   ███   ███    █▀ ')
                print(30*' ' +'  ███    ███   ███    ███  ▄███▄▄▄▄██▀   ███    ███  ▄███▄▄▄██▀   ▄███▄▄▄     ███   ███   ███       ')
                print(30*' ' +'▀█████████▀  ▀███████████ ▀▀███▀▀▀▀▀   ▀███████████ ▀▀███▀▀▀██▄  ▀▀███▀▀▀     ███   ███ ▀███████████')
                print(30*' ' +'  ███          ███    ███ ▀███████████   ███    ███   ███    ██▄   ███    █▄  ███   ███          ███')
                print(30*' ' +'  ███          ███    ███   ███    ███   ███    ███   ███    ███   ███    ███ ███   ███    ▄█    ███')
                print(30*' ' +' ▄████▀        ███    █▀    ███    ███   ███    █▀  ▄█████████▀    ██████████  ▀█   █▀   ▄████████▀ ')
                print(30*' ' +'                            ███    ███                                                              ')
                print('\n')
                print(30*' ' +'                                        VOCÊ GANHOU!!!')
                print(Fore.WHITE)
                print(30*' '+ '                                        '+ f'PONTUAÇÃO: {global_variables.pontuacao}')

            else:
                
                print('\n'*8)
                print(Fore.RED)
                print(43*' '+'  ▄████  ▄▄▄       ███▄ ▄███▓▓█████     ▒█████   ██▒   █▓▓█████  ██▀███  ')
                print(43*' '+' ██▒ ▀█▒▒████▄    ▓██▒▀█▀ ██▒▓█   ▀    ▒██▒  ██▒▓██░   █▒▓█   ▀ ▓██ ▒ ██▒')
                print(43*' '+'▒██░▄▄▄░▒██  ▀█▄  ▓██    ▓██░▒███      ▒██░  ██▒ ▓██  █▒░▒███   ▓██ ░▄█ ▒')
                print(43*' '+'░▓█  ██▓░██▄▄▄▄██ ▒██    ▒██ ▒▓█  ▄    ▒██   ██░  ▒██ █░░▒▓█  ▄ ▒██▀▀█▄  ')
                print(43*' '+'░▒▓███▀▒ ▓█   ▓██▒▒██▒   ░██▒░▒████▒   ░ ████▓▒░   ▒▀█░  ░▒████▒░██▓ ▒██▒')
                print(43*' '+' ░▒   ▒  ▒▒   ▓▒█░░ ▒░   ░  ░░░ ▒░ ░   ░ ▒░▒░▒░    ░ ▐░  ░░ ▒░ ░░ ▒▓ ░▒▓░')
                print(43*' '+'  ░   ░   ▒   ▒▒ ░░  ░      ░ ░ ░  ░     ░ ▒ ▒░    ░ ░░   ░ ░  ░  ░▒ ░ ▒░')
                print(43*' '+'░ ░   ░   ░   ▒   ░      ░      ░      ░ ░ ░ ▒       ░░     ░     ░░   ░ ')
                print(43*' '+'      ░       ░  ░       ░      ░  ░       ░ ░        ░     ░  ░   ░     ')
                print(43*' '+'                                                     ░                   ')
                print(43*' '+'                            VOCÊ PERDEU!!!')
                print(Fore.WHITE)
            

    sp_f.start()


    class callback:
        #classe que é responsável por todo o input do usuário, chamando as funções específicas e gerais

        def press(key):
            #clicou qualquer tecla, ele sai do menu

            if str(key) == 'Key.space':
                if global_variables.has_pressed == False:
                    global_variables.has_pressed == True
                    global_variables.name_loop_enabled = False
                    time.sleep(0.5)
                    menu_thread = threading.Thread(target=sp_f.menu)
                    menu_thread.start()
            
            if str(key) == 'Key.up':
                if global_variables.has_pressed == True:
                    if global_variables.y > 1:
                        global_variables.y -= 1
                    if global_variables.menu_enabled:
                        sp_f.menu()
                    elif global_variables.difficulty_enabled:
                        sp_f.menu_screens.difficulty()
                    elif global_variables.game_enabled:
                        try:
                            if global_variables.tab[2][global_variables.x-10] != 0:
                                global_variables.z = 3
                            else:
                                if global_variables.tab[1][global_variables.x-10] != 0:
                                    global_variables.z = 2
                                else:
                                    if global_variables.tab[0][global_variables.x-10] != 0:
                                        global_variables.z = 1
                        except:
                            pass
                        if global_variables.x > 9:

                            add = 10

                            while global_variables.tab[global_variables.z-1][global_variables.x - add] == 0:
                                if global_variables.x - add > 9:
                                    add += 10
                                else:
                                    add = 0

                            global_variables.x -= add
                            sp_f.game()

            if str(key) == 'Key.down':
                if global_variables.has_pressed == True:
                    if global_variables.y < 4:
                        global_variables.y += 1
                    if global_variables.menu_enabled:
                        sp_f.menu()
                    elif global_variables.difficulty_enabled:
                        sp_f.menu_screens.difficulty()
                    elif global_variables.game_enabled:

                        try:
                            if global_variables.tab[2][global_variables.x+10] != 0:
                                global_variables.z = 3
                            else:
                                if global_variables.tab[1][global_variables.x+10] != 0:
                                    global_variables.z = 2
                                else:
                                    if global_variables.tab[0][global_variables.x+10] != 0:
                                        global_variables.z = 1
                        except:
                            pass
                        if global_variables.x < 50:

                            try:
                                add = 10
                                while global_variables.tab[global_variables.z-1][global_variables.x + add] == 0:
                                    add += 10
                            except:
                                add = 0
                            global_variables.x += add
                            sp_f.game()
            
            if str(key) == 'Key.right':
                if global_variables.has_pressed == True:
                    if global_variables.game_enabled:
                        try:
                            if global_variables.tab[2][global_variables.x+1] != 0:
                                global_variables.z = 3
                            else:
                                if global_variables.tab[1][global_variables.x+1] != 0:
                                    global_variables.z = 2
                                else:
                                    if global_variables.tab[0][global_variables.x+1] != 0:
                                        global_variables.z = 1
                        except:
                            pass
                            
                    if global_variables.x < 59:
                        
                        try:
                            add = 1
                            while global_variables.tab[global_variables.z-1][global_variables.x + add] == 0:
                                add+=1
                        except:
                            add = 0
                        global_variables.x += add
                        sp_f.game()

            if str(key) == 'Key.left':
                if global_variables.has_pressed == True:
                    if global_variables.game_enabled:
                        try:
                            if global_variables.tab[2][global_variables.x-1] != 0:
                                global_variables.z = 3
                            else:
                                if global_variables.tab[1][global_variables.x-1] != 0:
                                    global_variables.z = 2
                                else:
                                    if global_variables.tab[0][global_variables.x-1] != 0:
                                        global_variables.z = 1
                        except:
                            pass

                    if global_variables.x > 0:
                        
                        try:
                            add = -1
                            while global_variables.tab[global_variables.z-1][global_variables.x - add] == 0:
                                add-=1
                        except:
                            add = 0
                        global_variables.x += add
                        sp_f.game()

            if str(key) == 'Key.enter':
                if global_variables.has_pressed == True:
                    gen_f.enter_handler()

            if str(key) == "'f'":
                if global_variables.has_pressed == True:
                    console.clear()
                    sp_f.menu()

            if str(key) == "'r'":
                if global_variables.has_pressed == True:
                    console.clear()
                    gen_f.randomizer(global_variables.num_arr[0],global_variables.tab[0])
                    gen_f.randomizer(global_variables.num_arr[1],global_variables.tab[1])
                    gen_f.randomizer(global_variables.num_arr[2],global_variables. tab[2])

                    sp_f.game()

            if str(key) == "'v'":
                if global_variables.has_pressed == True:
                    sp_f.end_game('Win')
                    global_variables.ganhou = True

            if str(key) == 'Key.esc':
                global_variables.pressed_esc = True
                global_variables.game_enabled = False
                global_variables.menu_enabled = False
                global_variables.difficulty_enabled = False
                global_variables.tutorial_enabled = False
                global_variables.countdown_enabled = False
                global_variables.name_loop_enabled = False
                time.sleep(0.2)
                console.clear()
                quit()


        def release(key):
            pass
        
    
    with Listener(on_press=callback.press, on_release=callback.release) as l:
        l.join()


main()
