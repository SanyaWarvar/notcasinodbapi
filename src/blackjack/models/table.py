from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from src.blackjack.models.card import Card
from src.blackjack.models.hand import Hand
from src.blackjack.utils import get_full_deck
from src.database import Base
from src.users.models import User


class Table:
    main_hand: Hand
    dealer_hand: Hand
    bet: int
    deck: List[Card]

    def __init__(self,bet, player_cards=None, dealer_cards=None, deck=None):
        if deck is None:
            deck = get_full_deck()

        if player_cards is None:
            player_cards = []

        if dealer_cards is None:
            dealer_cards = []

        self.main_hand = Hand(player_cards)
        self.dealer_hand = Hand(dealer_cards)
        self.deck = deck
        self.bet = bet

        if len(self.main_hand.cards) == 0:
            self.main_hand.add_card(self.deck)
            self.main_hand.add_card(self.deck)

        if len(self.dealer_hand.cards) == 0:
            self.dealer_hand.add_card(self.deck)

    def dealer_turn(self):
        self.main_hand.can_add = False
        while self.dealer_hand.amount < 17:
            self.dealer_hand.add_card(self.deck)
        self.dealer_hand.can_add = False

    def check_win(self, hand: Hand) -> str:
        player_amount = hand.amount
        dealer_amount = self.dealer_hand.amount

        if player_amount <= 21 and (dealer_amount < player_amount or dealer_amount > 21):
            return "win"
        elif player_amount == dealer_amount:
            return "push"
        return "lose"

    def result(self) -> int:
        res = self.check_win(self.main_hand)

        total_amount = 0

        if self.main_hand.is_bj:
            total_amount += round(self.bet * 1.5)
            return total_amount

        if self.main_hand.is_double:
            self.bet *= 2

        if res == "win":
            total_amount += self.bet
        if res == "lose":
            total_amount -= self.bet

        return total_amount


class Tables(Base):
    __tablename__ = "tables"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.id), unique=True, nullable=False)
    main_hand = Column(String)
    dealer_hand = Column(String)
    bet = Column(Integer, nullable=False)
    deck = Column(String, nullable=False)
    is_double = Column(Boolean, default=False)
