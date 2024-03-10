from typing import List
from src.blackjack.models.card import Card


def get_full_deck() -> List[Card]:
    full_deck: List[Card] = []

    for nominal in [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]:
        for suit in ["C", "D", "H", "S"]:
            amount: int = 10
            if isinstance(nominal, int):
                amount = nominal
            if nominal == "A":
                amount = 11
            full_deck.append(Card(f"{nominal}{suit}", amount))

    return full_deck
