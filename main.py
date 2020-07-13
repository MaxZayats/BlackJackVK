import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard
from vk_api.keyboard import VkKeyboardColor
import sqlite3
import random
from scripts import game


token='b9f04afbbb5c0fdd16a40a65776069c44d0f713e8d73384471b2c6510b5cf7bd10d28fc19e412b9ad4975' #Group longpoll token
vk_session = vk_api.VkApi(token=token)

longpoll = VkBotLongPoll(vk_session, '185605972') # 185605972 - GroupID
vk = vk_session.get_api()

players={}

conn = sqlite3.connect("mainDB.db") # mainDB.db - name of the DB file
cursor = conn.cursor()

NUM_OF_GAMES_TO_SHFL = 15 # количество игр для перетасовки


def create_keyboard(key):
    keyboard = VkKeyboard(one_time=False)
    if key == 'Меню':
        keyboard.add_button('Раздать Карты', payload='1', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Правила', payload='2', color=VkKeyboardColor.DEFAULT)
        keyboard.add_line()
        keyboard.add_button('Список Лидеров', payload='2', color=VkKeyboardColor.DEFAULT)
        return keyboard.get_keyboard()
    elif key == 'Раздать Карты':    
        keyboard.add_button('Ещё', payload='1', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Хватит', payload='1', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Удвоить Ставку', payload='1', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Главное Меню(Сдаться)', payload='1', color=VkKeyboardColor.NEGATIVE)
        return keyboard.get_keyboard()
    elif key == 'Ещё' or key == 'Хватит' or key == 'Удвоить Ставку':
        keyboard.add_button('Ещё', payload='1', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Хватит', payload='1', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Главное Меню(Сдаться)', payload='1', color=VkKeyboardColor.NEGATIVE)
        return keyboard.get_keyboard()
    elif key == 'empty':
        return '{"buttons":[],"one_time":true}'


def first_hand(user_id,peer_id):
    players[user_id].get_first_hand()

    vk.messages.send(peer_id=peer_id,
        message=f"Ваши карты: {' '.join(players[user_id].player_hand)} | Cумма: {str(players[user_id].player_sum) + players[user_id].second_pl_sum}\n"+
                f"Карты дилера: {' '.join(players[user_id].dealer_hand)} | Сумма: {str(players[user_id].dealer_sum) + players[user_id].second_dl_sum}",
        keyboard=create_keyboard('Раздать Карты'), random_id=0)

    if players[user_id].player_sum == 21:
        vk.messages.send(peer_id=peer_id, message='BLACKJACK!\nВы выиграли!', keyboard=create_keyboard('Меню'), random_id=0)
        players[user_id].close_game()
        update_score(user_id, 1)
    else:
        vk.messages.send(peer_id=peer_id, message='Ещё карту ?', random_id=0)


def more(user_id,peer_id):
    players[user_id].get_cards('player', 1) # Get card for player

    vk.messages.send(peer_id=peer_id, message=f'Вы получаете: {players[user_id].player_hand[-1]}',
        keyboard=create_keyboard('Ещё'), random_id=0)

    vk.messages.send(peer_id=peer_id,
        message=f"Ваши карты: {' '.join(players[user_id].player_hand)} | Cумма: {str(players[user_id].player_sum) + players[user_id].second_pl_sum}\n"+
                f"Карты дилера: {' '.join(players[user_id].dealer_hand)} | Сумма: {str(players[user_id].dealer_sum) + players[user_id].second_dl_sum}",
        random_id=0)
    
    if players[user_id].player_sum > 21:
        vk.messages.send(peer_id=peer_id, message='Вы набрали больше 21 очка.\nВы проиграли.',
            keyboard=create_keyboard('Меню'), random_id=0)
        players[user_id].close_game()
        update_score(user_id, -1)
    elif players[user_id].player_sum == 21:
        vk.messages.send(peer_id=peer_id, message='Вы набрали 21 очко.\nДилер берёт карты...', random_id=0)      
        stand(user_id,peer_id)
    else: # If player has less than 21
        vk.messages.send(peer_id=peer_id, message='Ещё карту ?', random_id=0)


def stand(user_id,peer_id):
    while True:
        players[user_id].get_cards('dealer', 1) # Get card for player dealer

        vk.messages.send(peer_id=peer_id, message=f'Дилер получает: {players[user_id].dealer_hand[-1]}',
            keyboard=create_keyboard('Хватит'), random_id=0)

        if players[user_id].dealer_sum > 21:
            vk.messages.send(peer_id=peer_id,
                message=f"Ваши карты: {' '.join(players[user_id].player_hand)} | Cумма: {str(players[user_id].player_sum)}\n"+
                        f"Карты дилера: {' '.join(players[user_id].dealer_hand)} | Сумма: {str(players[user_id].dealer_sum)}",
                random_id=0)
            vk.messages.send(peer_id=peer_id, message='Дилер набрал больше 21 очка.\nВы выиграли!',
                keyboard=create_keyboard('Меню'), random_id=0)
            players[user_id].close_game()
            update_score(user_id, 1)
            return

        if players[user_id].dealer_sum >= 17:
            vk.messages.send(peer_id=peer_id,
                message=f"Ваши карты: {' '.join(players[user_id].player_hand)} | Cумма: {str(players[user_id].player_sum)}\n"+
                        f"Карты дилера: {' '.join(players[user_id].dealer_hand)} | Сумма: {str(players[user_id].dealer_sum)}",
                random_id=0)
            break
    
    if players[user_id].dealer_sum < players[user_id].player_sum:
        vk.messages.send(peer_id=peer_id, message='Вы набрали больше чем дилер.\nВы выиграли!',
            keyboard=create_keyboard('Меню'), random_id=0)
        update_score(user_id, 1)
    elif players[user_id].dealer_sum > players[user_id].player_sum:
        vk.messages.send(peer_id=peer_id, message='Дилер набрал больше вас.\nВы проиграли!',
            keyboard=create_keyboard('Меню'), random_id=0)
        update_score(user_id, -1)
    elif players[user_id].dealer_sum == players[user_id].player_sum:
        vk.messages.send(peer_id=peer_id, message='Дилер набрал такое же количество очков, что и вы.\nНичья!',
            keyboard=create_keyboard('Меню'), random_id=0)
    
    players[user_id].close_game()


def double(user_id,peer_id):
    vk.messages.send(peer_id=peer_id, message='Ставка удвоена !', random_id=0)

    players[user_id].get_cards('player', 1)
    
    vk.messages.send(peer_id=peer_id, message=f'Вы получаете: {players[user_id].player_hand[-1]}',
        keyboard=create_keyboard('Удвоить Ставку'), random_id=0)

    vk.messages.send(peer_id=peer_id,
        message=f"Ваши карты: {' '.join(players[user_id].player_hand)} | Cумма: {str(players[user_id].player_sum)}\n"+
                f"Карты дилера: {' '.join(players[user_id].dealer_hand)} | Сумма: {str(players[user_id].dealer_sum) + players[user_id].second_dl_sum}",
        random_id=0)

    if players[user_id].player_sum > 21:
        vk.messages.send(peer_id=peer_id, message='Вы набрали больше 21 очка.\nВы проиграли.', keyboard=create_keyboard('Меню'), random_id=0)
        players[user_id].close_game()
        update_score(user_id, -2)
        return

    #Like stand() func
    while True:
        players[user_id].get_cards('dealer', 1)

        vk.messages.send(peer_id=peer_id, message=f'Дилер получает: {players[user_id].dealer_hand[-1]}', random_id=0)
        if players[user_id].dealer_sum >= 17:
            vk.messages.send(peer_id=peer_id,
                message=f"Ваши карты: {' '.join(players[user_id].player_hand)} | Cумма: {str(players[user_id].player_sum)}\n"+
                        f"Карты дилера: {' '.join(players[user_id].dealer_hand)} | Сумма: {str(players[user_id].dealer_sum)}",
                random_id=0)
            break
    
    if players[user_id].dealer_sum > 21:
        vk.messages.send(peer_id=peer_id, message='Дилер набрал больше 21 очка.\nВы выиграли!', keyboard=create_keyboard('Меню'), random_id=0)
        update_score(user_id, 2)
    elif players[user_id].dealer_sum < players[user_id].player_sum:
        vk.messages.send(peer_id=peer_id, message='Вы набрали больше чем дилер.\nВы выиграли!', keyboard=create_keyboard('Меню'), random_id=0)
        update_score(user_id, 2)
    elif players[user_id].dealer_sum > players[user_id].player_sum:
        vk.messages.send(peer_id=peer_id, message='Дилер набрал больше вас.\nВы проиграли!', keyboard=create_keyboard('Меню'), random_id=0)
        update_score(user_id, -2)
    elif players[user_id].dealer_sum == players[user_id].player_sum:
        vk.messages.send(peer_id=peer_id, message='Дилер набрал такое же количество очков, что и вы.\nНичья!', keyboard=create_keyboard('Меню'), random_id=0)

    players[user_id].close_game()


def split():
    pass


def update_score(user_id, value):
    row = cursor.execute('SELECT * FROM score WHERE id = ?', (user_id,)).fetchone()
    if row:
        cursor.execute('UPDATE score SET score = score + ? WHERE id = ?', (value, user_id,))
    else:
        name = vk.users.get(user_ids=user_id)[0]
        name = name['first_name'] +' '+ name['last_name']
        cursor.execute('INSERT INTO score (id, name, score) values(?,?,?)', (user_id, name, value))
    conn.commit()


def get_leaders(user_id):
    user_data = cursor.execute('SELECT * FROM score WHERE id = ?',(user_id,)).fetchone()
    if user_data == None:
        name = vk.users.get(user_ids=user_id)[0]
        name = name['first_name'] +' '+ name['last_name']
        cursor.execute('INSERT INTO score (id, name, score) values(?,?,?)', (user_id, name, 0))
        user_data = (str(user_id), name, 0)
    
    top_players_data = cursor.execute('SELECT * FROM score ORDER BY score DESC').fetchall()
    user_place = top_players_data.index(user_data) + 1
    text = ''
    place = 1
    for top_player_data in top_players_data[0:10]:
        text += f'{place}. {top_player_data[1]} | Очков: {top_player_data[2]}\n'
        place += 1
    text += f'\nВы:\n{user_place}. {user_data[1]} | Очков: {user_data[2]}'
    
    return text


def main():
    while True:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                payload = event.obj.payload
                message = event.obj.text.title()
                peer_id = event.object.peer_id
                user_id = event.obj.from_id
                if event.from_user:

                    if payload == '{"command":"start"}':
                        vk.messages.send(peer_id=peer_id, message='Удачной игры!',
                            keyboard=create_keyboard('Меню'), random_id=0)

                    elif payload == None:
                        if message == 'Меню':
                            vk.messages.send(peer_id=peer_id, message='Главное меню.\nУдачной игры!',
                                keyboard=create_keyboard('Меню'), random_id=0)
                        else:        
                            vk.messages.send(peer_id=peer_id, message='Бот воспринимает команды только с кнопок.\n'+
                                'Напишите "Меню" для выхода в главное меню.', random_id=0)   

                    elif payload == '1':
                        # Перетасовываем колоду по истерчению NUM_OF_GAMES_TO_SHFL раздач, либо создаём нового пользователя
                        try:
                            if players[user_id].number_of_game > NUM_OF_GAMES_TO_SHFL:
                                random.shuffle(players[user_id].deck)
                                players[user_id].number_of_game = 0
                                players[user_id].top_card = 0
                                vk.messages.send(peer_id=peer_id, message='Колода была перетасована!', random_id=0)
                        except:
                            players.update({user_id:game.player()})

                        if players[user_id].game_is_open == False:
                            if message == 'Раздать Карты':
                                first_hand(user_id,peer_id)
                            else:
                                vk.messages.send(peer_id=peer_id,
                                    message='Игра не была создана, чтобы выполнить это действие.\nНапишите "Меню" для выхода в главное меню.',
                                    random_id=0)

                        elif players[user_id].game_is_open == True:
                            if message == 'Ещё':
                                more(user_id,peer_id)    
                            elif message == 'Хватит':
                                stand(user_id,peer_id) 
                            elif message == 'Удвоить Ставку':
                                double(user_id,peer_id) 
                            elif message == 'Главное Меню(Сдаться)':
                                vk.messages.send(peer_id=peer_id, message='Вы сдались!\nГлавное меню.',
                                    keyboard=create_keyboard('Меню'), random_id=0)
                                players[user_id].close_game()
                                update_score(user_id, -1)
                            else:
                                vk.messages.send(peer_id=peer_id,
                                    message='Игра не была создана, чтобы выполнить это действие.\nНапишите "Меню" для выхода в главное меню.',
                                    random_id=0)

                    elif payload == '2':
                        if message == 'Список Лидеров':
                            vk.messages.send(peer_id=peer_id, message=f'Список лидеров:\n{get_leaders(user_id)}',
                                random_id=0)
                        elif message == 'Правила':
                            vk.messages.send(peer_id=peer_id, message='Правила довольно просты.\n\n'+
                                '•Вам нужно набрать больше очков чем дилер, но не более 21 очка, иначе вы проиграете.\n\n'+
                                '•Карты "2-10" оцениваются как своё значение. ("2" - это 2, "10" - это 10)\n\n'+
                                '•Карты "J,Q,K" оцениваются как 10.\n\n'+
                                '•Туз(A) оценивается как 1 или 11, в зависимости от ситуации.\n\n'+
                                '•"Удвоить ставку" - ваша ставка удваивается и вы получаете карту. Больше карт в этой партии вы получить не можете.',
                            random_id=0)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e) 
        main()
