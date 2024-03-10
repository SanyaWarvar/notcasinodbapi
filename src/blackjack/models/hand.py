from src.blackjack.models.card import Card
from typing import List
from random import choice


class Hand:
    cards: List[Card]
    is_double: bool
    is_bj: bool
    can_add: bool
    amount: int

    def __init__(self, cards=None, is_double=False, can_add=True):
        if cards is None:
            cards = []

        self.cards = cards
        self.is_double = is_double
        self.can_add = can_add

    def add_card(self, deck):
        if self.amount > 21:
            self.can_add = False

        if not self.can_add:
            return

        new_card = choice(deck)
        deck.remove(new_card)
        self.cards.append(new_card)

    def double(self, deck):
        if len(self.cards) != 2 and self.can_add:
            return

        self.add_card(deck)
        self.can_add = False
        self.is_double = True

    @property
    def amount(self):
        aces_num = 0
        amount = 0
        for card in self.cards:
            amount += card.value
            if card.value == 11:
                aces_num += 1

        while amount > 21 and aces_num > 0:
            amount -= 10
            aces_num -= 1
        return amount

    @property
    def is_bj(self):
        if len(self.cards) == 2 and self.amount == 21:
            return True
        return False
