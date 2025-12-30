from typing import List, Iterable, Optional
import random

# card constants
RANKS = "23456789TJQKA"
SUITS = "cdhs"

# canonical 52 card deck
ALL_CARDS = [r + s for r in RANKS for s in SUITS]


def is_valid_card(card: str) -> bool:
    if not isinstance(card, str) or len(card) != 2:
        return False
    return card[0] in RANKS and card[1] in SUITS


def card_to_index(card: str) -> int:
    if not is_valid_card(card):
        raise ValueError(f"invalid card: {card}")
    return RANKS.index(card[0]) * 4 + SUITS.index(card[1])


def index_to_card(index: int) -> str:
    if index < 0 or index >= 52:
        raise IndexError("card index out of range")
    rank = RANKS[index // 4]
    suit = SUITS[index % 4]
    return rank + suit


class Deck:
    def __init__(self, cards: Optional[Iterable[str]] = None, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()
        self._base = list(cards) if cards is not None else ALL_CARDS.copy()
        self.cards = self._base.copy()
        self.shuffle()

    def reset(self, shuffle: bool = True) -> None:
        self.cards = self._base.copy()
        if shuffle:
            self.shuffle()

    def shuffle(self) -> None:
        self.rng.shuffle(self.cards)

    def remove(self, cards: Iterable[str]) -> None:
        for c in cards:
            if c not in self.cards:
                raise ValueError(f"card not in deck: {c}")
            self.cards.remove(c)

    def draw(self, n: int = 1) -> List[str]:
        if n < 0:
            raise ValueError("n must be non negative")
        if n > len(self.cards):
            raise ValueError("not enough cards")
        out = []
        for _ in range(n):
            out.append(self.cards.pop(0))
        return out

    def peek(self, n: int = 1) -> List[str]:
        return self.cards[:n]

    def copy(self) -> "Deck":
        d = Deck(cards=self._base, rng=self.rng)
        d.cards = self.cards.copy()
        return d

    def __len__(self) -> int:
        return len(self.cards)

    def __contains__(self, card: str) -> bool:
        return card in self.cards


def to_treys_card(card: str):
    try:
        from treys import Card
    except Exception as exc:
        raise ImportError("treys is required") from exc
    return Card.new(card)


def to_treys_cards(cards: Iterable[str]) -> List:
    return [to_treys_card(c) for c in cards]


if __name__ == "__main__":
    d = Deck()
    print(d.peek(5))
    d.remove(["Ah", "Kd"])
    print(len(d))
    print(d.draw(2))
