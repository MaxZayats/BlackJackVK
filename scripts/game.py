import random


number_of_deck = 6
main_deck = [
    ('2 ♣', 2), ('2 ♠', 2), ('2 ❤', 2), ('2 ♦', 2),
    ('3 ♣', 3), ('3 ♠', 3), ('3 ❤', 3), ('3 ♦', 3),
    ('4 ♣', 4), ('4 ♠', 4), ('4 ❤', 4), ('4 ♦', 4),
    ('5 ♣', 5), ('5 ♠', 5), ('5 ❤', 5), ('5 ♦', 5),
    ('6 ♣', 6), ('6 ♠', 6), ('6 ❤', 6), ('6 ♦', 6),
    ('7 ♣', 7), ('7 ♠', 7), ('7 ❤', 7), ('7 ♦', 7),
    ('8 ♣', 8), ('8 ♠', 8), ('8 ❤', 8), ('8 ♦', 8),
    ('9 ♣', 9), ('9 ♠', 9), ('9 ❤', 9), ('9 ♦', 9),
    ('10 ♣', 10), ('10 ♠', 10), ('10 ❤', 10), ('10 ♦', 10),
    ('J ♣', 10), ('J ♠', 10), ('J ❤', 10), ('J ♦', 10),
    ('Q ♣', 10), ('Q ♠', 10), ('Q ❤', 10), ('Q ♦', 10),
    ('K ♣', 10), ('K ♠', 10), ('K ❤', 10), ('K ♦', 10),
    ('A ♣', 11), ('A ♠', 11), ('A ❤', 11), ('A ♦', 11),
]*number_of_deck


class player():
    def __init__(self):
        self.deck = main_deck.copy()
        random.shuffle(self.deck)
        self.top_card = 0
        self.player_hand = []
        self.dealer_hand = []
        self.player_sum = 0
        self.dealer_sum = 0
        self.second_pl_sum = ''
        self.second_dl_sum = ''
        self.number_of_game = 0
        self.game_is_open = False
        self.dealer_second_card = False

    def get_cards(self, key, amount):
        """Функция получения карт для игрока или дилера"""
        if key == 'player':
            hand = self.player_hand
            sum_ = self.player_sum
            second_sum = self.second_pl_sum
        elif key == 'dealer':
            hand = self.dealer_hand
            sum_ = self.dealer_sum
            second_sum = self.second_dl_sum

        for _ in range(amount):
            if self.dealer_second_card and key == 'dealer':
                card = self.deck[3]
                self.top_card -= 1
                self.dealer_second_card = False
            else:
                card = self.deck[self.top_card]
            hand.append(card[0])
            sum_ += card[1]
            if card[0][0] == 'A' or second_sum != '':
                second_sum = f'({sum_ - 10})'
            self.top_card += 1

        if sum_ > 21 and second_sum != '':
            # Если кто-то набрал больше 21, но у него есть Туз(Ace)
            sum_ -= 10
            second_sum = ''
        elif sum_ == 21:
            second_sum = ''

        if key == 'player':
            self.player_hand = hand
            self.player_sum = sum_
            self.second_pl_sum = second_sum
        elif key == 'dealer':
            self.dealer_hand = hand
            self.dealer_sum = sum_
            self.second_dl_sum = second_sum

    def get_first_hand(self):
        self.game_is_open = True
        self.get_cards('dealer', 1)
        self.get_cards('player', 2)
        # Резервация карты для дилера
        self.dealer_second_card = True
        self.top_card += 1

    def close_game(self):
        self.game_is_open = False
        self.player_hand = []
        self.dealer_hand = []
        self.player_sum = 0
        self.dealer_sum = 0
        self.second_pl_sum = ''
        self.second_dl_sum = ''
        self.number_of_game += 1
        self.dealer_second_card = False
