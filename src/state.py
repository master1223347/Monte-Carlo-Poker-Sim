from dataclasses import dataclass, field, replace
from typing import List, Optional, Set
from .cards import is_valid_card


_VALID_STREETS = {"preflop", "flop", "turn", "river"}


def _parse_cards_arg(cards) -> List[str]:
    # accept list of strings or a single space separated string
    if cards is None:
        return []
    if isinstance(cards, str):
        parts = cards.strip().split()
        return [p for p in parts if p]
    if isinstance(cards, (list, tuple)):
        return list(cards)
    raise TypeError("cards must be list[str] or space separated str")


@dataclass
class PokerState:
    # hero_hand must be two distinct card strings like ["Ah", "Kd"]
    hero_hand: List[str] = field(default_factory=list)
    # board is 0 to 5 card strings like ["Qh", "Jh", "2c"]
    board: List[str] = field(default_factory=list)
    # chip counts and pot as floats (can be int values too)
    pot: float = 0.0
    to_call: float = 0.0
    stack: float = 0.0
    # number of opponents at table (excluding hero)
    num_opponents: int = 1
    # street name: preflop, flop, turn, river
    street: str = "preflop"

    def __post_init__(self):
        # normalize inputs that might be given as strings
        self.hero_hand = _parse_cards_arg(self.hero_hand)
        self.board = _parse_cards_arg(self.board)

        # basic structural validation
        if len(self.hero_hand) != 2:
            raise ValueError("hero_hand must contain exactly 2 cards")
        if not (0 <= len(self.board) <= 5):
            raise ValueError("board must have between 0 and 5 cards")
        if self.num_opponents < 1:
            raise ValueError("num_opponents must be >= 1")
        if self.street not in _VALID_STREETS:
            raise ValueError(f"street must be one of {_VALID_STREETS}")

        # card format validation and duplicate detection
        seen: Set[str] = set()
        for c in self.hero_hand + self.board:
            if not is_valid_card(c):
                raise ValueError(f"invalid card: {c}")
            if c in seen:
                raise ValueError(f"duplicate card found: {c}")
            seen.add(c)

        # numeric normalization and sanity checks
        try:
            self.pot = float(self.pot)
            self.to_call = float(self.to_call)
            self.stack = float(self.stack)
        except Exception:
            raise ValueError("pot, to_call, and stack must be numeric")

        if self.pot < 0 or self.to_call < 0 or self.stack < 0:
            raise ValueError("pot, to_call, and stack must be non negative")
        if self.to_call > self.stack:
            # you can't be asked to call more than your stack in this simplified model
            raise ValueError("to_call cannot exceed stack in this model")

    @classmethod
    def from_strings(
        cls,
        hero_hand: str,
        board: Optional[str] = None,
        pot: float = 0.0,
        to_call: float = 0.0,
        stack: float = 0.0,
        num_opponents: int = 1,
        street: str = "preflop",
    ):
        # convenience constructor accepting space separated card strings
        return cls(
            hero_hand=hero_hand,
            board=board or "",
            pot=pot,
            to_call=to_call,
            stack=stack,
            num_opponents=num_opponents,
            street=street,
        )

    def known_cards(self) -> Set[str]:
        # set of cards known to the simulator
        return set(self.hero_hand) | set(self.board)

    def missing_board_cards(self) -> int:
        # how many community cards remain to be dealt this hand
        return 5 - len(self.board)

    def clone_with(self, **kwargs):
        # immutable style updater returning a new PokerState with fields replaced
        return replace(self, **kwargs)

    def to_dict(self) -> dict:
        # lightweight serializable representation
        return {
            "hero_hand": list(self.hero_hand),
            "board": list(self.board),
            "pot": self.pot,
            "to_call": self.to_call,
            "stack": self.stack,
            "num_opponents": self.num_opponents,
            "street": self.street,
        }

    def __repr__(self) -> str:
        return (
            f"PokerState(hero_hand={self.hero_hand}, board={self.board}, "
            f"pot={self.pot}, to_call={self.to_call}, stack={self.stack}, "
            f"num_opponents={self.num_opponents}, street='{self.street}')"
        )
