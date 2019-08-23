# -*- coding: utf-8 -*- 
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard
from vk_api.keyboard import VkKeyboardColor
import sqlite3
import random,time


token=''
#Group longpoll token
vk_session = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk_session, '185605972') # 185605972 - GroupID
vk = vk_session.get_api()


conn = sqlite3.connect("mainDB.db") # mainDB.db - name of the DB file
cursor = conn.cursor()
try:
    cursor.execute('''
    CREATE TABLE "main" (
	"id"	INTEGER,
	"PlCard"	INTEGER,
	"PlSumMax"	INTEGER,
	"PlSumMin"	INTEGER,
	"DlCard"	INTEGER,
	"DlSumMax"	INTEGER,
	"DlSumMin"	INTEGER,
	"Lang"	INTEGER,
	"Score"	INTEGER,
	"gameStatus"	INTEGER,
	"doubleStatus"	INTEGER
    ); ''')
#lang: 0-RU 1-EN
except:
    pass

number_of_deck=4
deck = [
    ['2 ♣',2],['2 ♠',2],['2 ❤',2],['2 ♦',2],
    ['3 ♣',3],['3 ♠',3],['3 ❤',3],['3 ♦',3],
    ['4 ♣',4],['4 ♠',4],['4 ❤',4],['4 ♦',4],
    ['5 ♣',5],['5 ♠',5],['5 ❤',5],['5 ♦',5],
    ['6 ♣',6],['6 ♠',6],['6 ❤',6],['6 ♦',6],
    ['7 ♣',7],['7 ♠',7],['7 ❤',7],['7 ♦',7],
    ['8 ♣',8],['8 ♠',8],['8 ❤',8],['8 ♦',8],
    ['9 ♣',9],['9 ♠',9],['9 ❤',9],['9 ♦',9],
    ['10 ♣',10],['10 ♠',10],['10 ❤',10],['10 ♦',10],
    ['J ♣',10],['J ♠',10],['J ❤',10],['J ♦',10],
    ['Q ♣',10],['Q ♠',10],['Q ❤',10],['Q ♦',10],
    ['K ♣',10],['K ♠',10],['K ❤',10],['K ♦',10],
    ['A ♣',11],['A ♠',11],['A ❤',11],['A ♦',11],
]*number_of_deck

def update_value_DB(var,value,from_id):
    cursor.execute('SELECT * FROM main')
    cursor.execute('UPDATE main SET '+str(var)+' = ? WHERE id= ?', (value, from_id,))
    conn.commit()

def take_Value_DB(var,from_id):
    try:
        [x], = cursor.execute('select '+str(var)+' from main where id=?', (from_id,))
        return x
    except:
        return None    

def addNewIdDB(from_id):
    if take_Value_DB('id',from_id)==None:
        cursor.execute('SELECT * FROM main')
        cursor.execute('''INSERT INTO main (id,PlCard,PlSumMax,PlSumMin,DlCard,DlSumMax,DlSumMin,Lang,Score,gameStatus,doubleStatus)
                      values (?,?,?,?,?,?,?,?,?,?,?)''', (from_id, '0','0','0','0','0','0','0','0','0','0')) 
        conn.commit()
    else:
        pass

def lose_message(vk,event,lang,from_id):
    #PlCard,PlSumMax,PlSumMin=take_Value_DB('PlCard',from_id),take_Value_DB('PlSumMax',from_id),take_Value_DB('PlSumMin',from_id)
    #DlCard,DlSumMax,DlSumMin=take_Value_DB('DlCard',from_id),take_Value_DB('DlSumMax',from_id),take_Value_DB('DlSumMin',from_id)
    Score=take_Value_DB('Score',from_id)
    if take_Value_DB('doubleStatus',from_id)==1:
        Score=Score-2
    else:
        Score=Score-1
    update_value_DB('Score',Score,from_id)
    update_value_DB('gameStatus',0,from_id)
    update_value_DB('doubleStatus',0,from_id)
    if lang==0:
        vk.messages.send(peer_id=event.object.peer_id, message='Вы проиграли!',
                                    keyboard=create_keyboard('Главное меню(Сдаться)',from_id), random_id=0)
    elif lang==1:
        vk.messages.send(peer_id=event.object.peer_id, message='You lost!',
                                    keyboard=create_keyboard('Главное меню(Сдаться)',from_id), random_id=0)

def win_message(vk,event,lang,from_id):
    #PlCard,PlSumMax,PlSumMin=take_Value_DB('PlCard',from_id),take_Value_DB('PlSumMax',from_id),take_Value_DB('PlSumMin',from_id)
    #DlCard,DlSumMax,DlSumMin=take_Value_DB('DlCard',from_id),take_Value_DB('DlSumMax',from_id),take_Value_DB('DlSumMin',from_id)
    Score=take_Value_DB('Score',from_id)
    if take_Value_DB('doubleStatus',from_id)==1:
        Score=Score+2
    else:
        Score=Score+1
    update_value_DB('Score',Score,from_id)
    update_value_DB('gameStatus',0,from_id)
    update_value_DB('doubleStatus',0,from_id)
    if lang==0:
        vk.messages.send(peer_id=event.object.peer_id, message='Вы выйграли!',
                                     keyboard=create_keyboard('Главное меню(Сдаться)',from_id), random_id=0)
    elif lang==1:
        vk.messages.send(peer_id=event.object.peer_id, message='You win!',
                                     keyboard=create_keyboard('Главное меню(Сдаться)',from_id), random_id=0)

def draw_message(vk,event,lang,from_id):
    update_value_DB('gameStatus',0,from_id)
    update_value_DB('doubleStatus',0,from_id)
    if lang==0:
        vk.messages.send(peer_id=event.object.peer_id, message='Ничья!',
                                     keyboard=create_keyboard('Главное меню(Сдаться)',from_id), random_id=0)
    elif lang==1:
        vk.messages.send(peer_id=event.object.peer_id, message='Push!',
                                     keyboard=create_keyboard('Главное меню(Сдаться)',from_id), random_id=0)
    
def info_message(vk,event,lang,from_id):
    PlCard,PlSumMax,PlSumMin=take_Value_DB('PlCard',from_id),take_Value_DB('PlSumMax',from_id),take_Value_DB('PlSumMin',from_id)
    DlCard,DlSumMax=take_Value_DB('DlCard',from_id),take_Value_DB('DlSumMax',from_id)
    if lang==0:
        vk.messages.send(peer_id=event.object.peer_id, message='Ваши карты: ' + str(PlCard) + ' | Сумма: ' + str(PlSumMax) + '('+ str(PlSumMin) + ')\nКарты дилера: ' + str(DlCard) + ' | Сумма: ' + str(DlSumMax),
                                    random_id=0)
    elif lang==1:
        vk.messages.send(peer_id=event.object.peer_id, message='Your card: ' + str(PlCard) + ' | Amount: ' + str(PlSumMax) + '('+ str(PlSumMin) + ")\nThe dealer's cards: " + str(DlCard) + ' | Amount: ' + str(DlSumMax),
                                   random_id=0)

def first_hand(from_id,vk,lang,event):
    update_value_DB('gameStatus','1',from_id)
    
    c1,c2,c3=(random.randint(0, len(deck)-1)),(random.randint(0, len(deck)-1)),(random.randint(0, len(deck)-1))

    PlCard=deck[c1][0]+' '+deck[c2][0]
    PlSumMax=deck[c1][1]+deck[c2][1]
    if (deck[c1][1]==11) or (deck[c2][1]==11):
        if (PlSumMax)>21: # two ACE
            PlSumMax=12
            PlSumMin=2
        else:
            PlSumMin=PlSumMax-10    
    else:
        PlSumMin=PlSumMax

    DlCard=deck[c3][0]
    DlSumMax=deck[c3][1]
    if deck[c3][1]==11:
        DlSumMin=DlSumMax-10
    else:
        DlSumMin=DlSumMax

    update_value_DB('PlCard',PlCard,from_id)
    update_value_DB('PlSumMax',PlSumMax,from_id)
    update_value_DB('PlSumMin',PlSumMin,from_id)
    update_value_DB('DlCard',DlCard,from_id)
    update_value_DB('DlSumMax',DlSumMax,from_id)
    update_value_DB('DlSumMin',DlSumMin,from_id)

    info_message(vk,event,lang,from_id)

    if PlSumMax==21:
        vk.messages.send(peer_id=event.object.peer_id, message='BLACKJACK!',
                                  keyboard=create_keyboard('Главное меню(Сдаться)',from_id),random_id=0)
        win_message(vk,event,lang,from_id)
        return
    send_message(msg[2][lang],event) # Ещё карту ?    

def Double(from_id,vk,lang,event):
    gameStatus=take_Value_DB('gameStatus',from_id)
    if gameStatus==0:
        vk.messages.send(peer_id=event.object.peer_id, message=msg[3][lang],
                                    random_id=0)
        return
    doubleStatus=take_Value_DB('doubleStatus',from_id)
    if doubleStatus==1:
        vk.messages.send(peer_id=event.object.peer_id, message=msg[9][lang],
                                    random_id=0)
        return
    update_value_DB('doubleStatus',1,from_id)
    Hit(from_id,vk,lang,event)
    if take_Value_DB('gameStatus',from_id)==1:
        Stand(from_id,vk,lang,event)
    else:
        pass    
    
def Hit(from_id,vk,lang,event):
    
    gameStatus=take_Value_DB('gameStatus',from_id)
    if gameStatus==0:
        vk.messages.send(peer_id=event.object.peer_id, message=msg[3][lang],
                                    random_id=0)
        return
    PlCard,PlSumMax,PlSumMin=take_Value_DB('PlCard',from_id),take_Value_DB('PlSumMax',from_id),take_Value_DB('PlSumMin',from_id)
    #DlCard,DlSumMax,DlSumMin=take_Value_DB('DlCard',from_id),take_Value_DB('DlSumMax',from_id),take_Value_DB('DlSumMin',from_id)


    c=random.randint(0, len(deck)-1)

    PlCard=PlCard+' '+deck[c][0]

    if lang==0:
        vk.messages.send(peer_id=event.object.peer_id, message='Вы получаете: ' + str(deck[c][0]),
                                   keyboard=create_keyboard('without double',from_id),random_id=0)
    elif lang==1:
        vk.messages.send(peer_id=event.object.peer_id, message='You get: ' + str(deck[c][0]),
                                    keyboard=create_keyboard('without double',from_id),random_id=0)

    if deck[c][1]==11:
        if (PlSumMax+11)>21:
            PlSumMax+=1
            PlSumMin+=1
        else:
            PlSumMax+=11
            PlSumMin+=1
    else:
        PlSumMax+=deck[c][1]
        PlSumMin+=deck[c][1]          

    
    if PlSumMax>21:
        if PlSumMin<=21:
            PlSumMax=PlSumMin
        else:
            #gg
            update_value_DB('PlCard',PlCard,from_id)
            update_value_DB('PlSumMax',PlSumMax,from_id)
            update_value_DB('PlSumMin',PlSumMin,from_id)
            info_message(vk,event,lang,from_id)

            lose_message(vk,event,lang,from_id)
            vk.messages.send(peer_id=event.object.peer_id, message=msg[4][lang],
                                    random_id=0)
            return

    update_value_DB('PlCard',PlCard,from_id)
    update_value_DB('PlSumMax',PlSumMax,from_id)
    update_value_DB('PlSumMin',PlSumMin,from_id)
    info_message(vk,event,lang,from_id)

def Stand(from_id,vk,lang,event):
    gameStatus=take_Value_DB('gameStatus',from_id)
    if gameStatus==0:
        vk.messages.send(peer_id=event.object.peer_id, message=msg[3][lang],
                                    random_id=0)
        return
    PlSumMax=take_Value_DB('PlSumMax',from_id)
    DlCard,DlSumMax,DlSumMin=take_Value_DB('DlCard',from_id),take_Value_DB('DlSumMax',from_id),take_Value_DB('DlSumMin',from_id)

    c=random.randint(0, len(deck)-1)

    if lang==0:
        vk.messages.send(peer_id=event.object.peer_id, message='Дилер получает: ' + str(deck[c][0]),
                                    random_id=0)
    elif lang==1:
        vk.messages.send(peer_id=event.object.peer_id, message='The dealer gets: ' + str(deck[c][0]),
                                    random_id=0)

    
    DlCard=DlCard + ' ' + deck[c][0]
    
    if deck[c][1]==11:
        if (DlSumMax+11)>21:
            DlSumMax=DlSumMax+1
            DlSumMin=DlSumMin+1
        else:
            DlSumMax=DlSumMax+11
            DlSumMin=DlSumMin+1
    else:
        DlSumMax=DlSumMax+deck[c][1]
        DlSumMin=DlSumMin+deck[c][1]  

    update_value_DB('DlSumMax',DlSumMax,from_id)
    update_value_DB('DlSumMin',DlSumMin,from_id)
    update_value_DB('DlCard',DlCard,from_id)
    #info_message(vk,event,lang,from_id)

    if DlSumMax>21:
        if DlSumMin<=21:
            DlSumMax=DlSumMin

            update_value_DB('DlSumMax',DlSumMax,from_id)
            info_message(vk,event,lang,from_id)
        else:
            info_message(vk,event,lang,from_id)
            win_message(vk,event,lang,from_id)
            vk.messages.send(peer_id=event.object.peer_id, message=msg[5][lang],
                                    random_id=0)
            return

    if DlSumMax>PlSumMax:
        info_message(vk,event,lang,from_id)
        lose_message(vk,event,lang,from_id)
        vk.messages.send(peer_id=event.object.peer_id, message=msg[6][lang],
                                random_id=0)
        return

    if DlSumMax>16:
        if DlSumMax==PlSumMax:
            info_message(vk,event,lang,from_id)
            draw_message(vk,event,lang,from_id)   
            return
        elif DlSumMax<PlSumMax:
            info_message(vk,event,lang,from_id)
            win_message(vk,event,lang,from_id)
            vk.messages.send(peer_id=event.object.peer_id, message=msg[7][lang],
                                    random_id=0)
            return       
    Stand(from_id,vk,lang,event)

keymsg=[
    ['Раздать карты','Deal'],#0
    ['Правила','Rules'],#1
    ['Счёт','Score'],#2
    ['Изменить язык','Change language'],#3
    ['Ещё','Hit'],#4
    ['Хватит','Stand'],#5
    ['Играть снова','Play again'],#6
    ['Главное меню(Сдаться)','Main menu(Surrender)'],#7
    ['Удвоить ставку','Double']#8
]

def create_keyboard(request,from_id):
    keyboard = VkKeyboard(one_time=False)
    lang = take_Value_DB('Lang',from_id)
    if (request == "Начать") or (request == 'Start') or (request == "начать") or (request == "start") or (request == "Изменить язык") or (request == "Change language"):
        keyboard.add_button('Русский', color=VkKeyboardColor.DEFAULT)
        keyboard.add_line()
        keyboard.add_button('English', color=VkKeyboardColor.DEFAULT)
        keyboard = keyboard.get_keyboard()
        return keyboard
    elif (request == 'Русский') or (request == 'English') or (request == 'Главное меню(Сдаться)') or (request == 'Main menu(Surrender)'):
        keyboard.add_button(keymsg[0][lang], color=VkKeyboardColor.POSITIVE) #['Раздать карты'','Deal'],
        keyboard.add_line()
        keyboard.add_button(keymsg[1][lang], color=VkKeyboardColor.DEFAULT) #['Правила','Rules'],
        keyboard.add_line()
        keyboard.add_button(keymsg[2][lang], color=VkKeyboardColor.DEFAULT) #['Счёт','Score'],
        keyboard.add_button(keymsg[3][lang], color=VkKeyboardColor.DEFAULT) #['Изменить язык','Change language'],
        keyboard = keyboard.get_keyboard()
        return keyboard
    elif (request == 'Раздать карты') or (request == 'Deal'):    
        keyboard.add_button(keymsg[4][lang], color=VkKeyboardColor.POSITIVE) #['Ещё','Hit']
        keyboard.add_button(keymsg[5][lang], color=VkKeyboardColor.POSITIVE) #['Хватит','Stand'],
        keyboard.add_line()
        keyboard.add_button(keymsg[8][lang], color=VkKeyboardColor.PRIMARY) #['Удвоить ставку','Double']
        keyboard.add_line()
        keyboard.add_button(keymsg[7][lang], color=VkKeyboardColor.NEGATIVE)#['Главное меню(Сдаться)','Main menu(Surrender)']
        keyboard = keyboard.get_keyboard()
        return keyboard
    elif request == 'without double':
        keyboard.add_button(keymsg[4][lang], color=VkKeyboardColor.POSITIVE) #['Ещё','Hit']
        keyboard.add_button(keymsg[5][lang], color=VkKeyboardColor.POSITIVE) #['Хватит','Stand'],
        keyboard.add_line()
        keyboard.add_button(keymsg[7][lang], color=VkKeyboardColor.NEGATIVE)#['ГГлавное меню(Сдаться)','Main menu(Surrender)u']
        keyboard = keyboard.get_keyboard()
        return keyboard  

rules=['''
    Правила довольно просты.\n
    •Вам нужно набрать больше очков чем дилер, но не больше чем 21 очко, иначе вы проиграете.\n
    •Карты "2-10" оцениваются как своё значение. ("2" - это 2, "10" - это 10)\n
    •Карты "J,Q,K" оцениваются как 10.\n
    •Туз(A) оценивается как 1 или 11, в зависимости от ситуации.\n
    •"Удвоить ставку" - ваша ставка удваивается и вы получаете карту. Больше карт в этой партии вы получить не можете.\n''',
    '''
    The rules are quite simple.\n
    •You need to score more points than the dealer, but not more than 21 points, otherwise you lose.\n
    •The cards "2-10" cards are evaluated as their value. ("2" is 2, "10" is 10)\n
    •The cards "J,Q,K" are evaluated as 10.\n
    •ACE(A) is rated as 1 or 11, depending on the situation.\n
    •"Double" - your bet is doubled and you get a card. More cards in this party you can not get.\n
    '''
]
        
msg = [
    ['Ок, начнём!','Ok, lets go!'],
    ['Ваш счёт: ','Your score: '],
    ['Ещё карту ?','More card ?'],
    ['Игра не была создана, начните новую игру.','The game was not created, start a new game.'],
    ['Вы набрали больше 21 очка.','You scored more than 21 points.'],
    ['Дилер набрал больше 21 очка.','The dealer scored more than 21 points.'], #5
    ['Дилер набрал больше вас.','The dealer scored more than you.'], #6
    ['Вы набрали больше очков чем Дилер!','You scored more points than the Dealer!'],#7
    ['Предыдущая игра не была закончена. Хотите начать новую',''],#8
    ['Вы можете удвоить ставку только после первой раздачи!','You can double your bet only after the first hand!']#9
]

def send_message(text,event):
    request = event.obj.text
    from_id = event.obj.from_id
    keyboard = create_keyboard(request,from_id)

    vk.messages.send(peer_id=event.object.peer_id, message=text, keyboard=keyboard, random_id=0)

def main():
    while True:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                request = event.obj.text        # Message text
                from_id = event.obj.from_id     # User ID
                print(from_id, request)
                addNewIdDB(from_id) # add new user in DB
                lang = take_Value_DB('Lang',from_id)
                if event.from_user: # В лс боту
                    if (request == "Начать") or (request == 'Start') or (request == "начать") or (request == "start") or (request == "Изменить язык") or (request == "Change language"):
                        send_message('Выберите язык.\nSelect your language.',event)

                    elif request == 'Русский':
                        update_value_DB('Lang',0,from_id)
                        #keyboard = create_keyboard(request,from_id)
                        send_message('Начнём!',event)
                    
                    elif (request == 'Главное меню(Сдаться)') or (request == 'Main menu(Surrender)'):
                        lose_message(vk,event,lang,from_id)

                    elif (request == 'English') or (request == 'Main menu(Surrender)'):
                        update_value_DB('Lang',1,from_id)
                        #keyboard = create_keyboard(request,from_id)
                        send_message('Ok, lets go!',event)   

                    elif (request == 'Раздать карты') or (request == 'Deal') or (request == 'Играть снова') or (request == 'Play again'):
                        first_hand(from_id,vk,lang,event)  

                    elif (request == 'Счёт') or (request == 'Score'):
                        send_message(f"{msg[1][lang]} {take_Value_DB('Score',from_id)}",event) 

                    elif (request == 'Правила') or (request == 'Rules'):
                        send_message(rules[lang],event)  

                    elif (request == 'Ещё') or (request == 'Hit'):                     
                        Hit(from_id,vk,lang,event)

                    elif (request == 'Хватит') or (request == 'Stand'):    
                        Stand(from_id,vk,lang,event)

                    elif (request == 'Удвоить ставку') or (request == 'Double'):    
                        Double(from_id,vk,lang,event)
                    lang = take_Value_DB('Lang',from_id)
main()
