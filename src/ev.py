from typing import List, Optional

from .cards import Deck, is_valid_card
from .equity import _make_rng
try:
    from treys import Evaluator, Card
except Exception as exc:
    raise ImportError("treys is required. Install with `pip install treys`.") from exc

EVALUATOR = Evaluator()


def _validate_inputs(hero_hand: List[str], board: Optional[List[str]], num_opponents: int, sims: int) -> None:
    if not isinstance(hero_hand, (list, tuple)) or len(hero_hand) != 2:
        raise ValueError("hero_hand must be two cards")
    for c in hero_hand:
        if not is_valid_card(c):
            raise ValueError(f"invalid hero card: {c}")
    board = board or []
    if len(board) > 5:
        raise ValueError("board too long")
    for c in board:
        if not is_valid_card(c):
            raise ValueError(f"invalid board card: {c}")
    if num_opponents < 1:
        raise ValueError("num_opponents must be >= 1")
    if sims <= 0:
        raise ValueError("sims must be positive")


def monte_carlo_ev(
    hero_hand: List[str],
    board: Optional[List[str]] = None,
    pot: float = 0.0,
    to_call: float = 0.0,
    stack: float = 0.0,
    num_opponents: int = 1,
    sims: int = 5000,
    rng: Optional[object] = None,
) -> float:
    _validate_inputs(hero_hand, board, num_opponents, sims)
    board = board or []
    rng_obj = _make_rng(rng)

    ev_sum = 0.0

    for _ in range(sims):
        deck = Deck(rng=rng_obj)
        try:
            deck.remove(hero_hand + board)
        except ValueError:
            raise ValueError("duplicate or invalid known card")

        opp_raw = deck.draw(2 * num_opponents)
        opp_hands = [opp_raw[i : i + 2] for i in range(0, len(opp_raw), 2)]

        remaining = 5 - len(board)
        future_board = deck.draw(remaining) if remaining > 0 else []
        full_board = list(board) + future_board

        hero_cards_t = [Card.new(c) for c in hero_hand]
        board_t = [Card.new(c) for c in full_board]
        hero_score = EVALUATOR.evaluate(board_t, hero_cards_t)

        opp_scores = []
        for opp in opp_hands:
            opp_cards_t = [Card.new(c) for c in opp]
            opp_scores.append(EVALUATOR.evaluate(board_t, opp_cards_t))

        best_opp = min(opp_scores)

        if hero_score < best_opp:
            payoff = pot
        elif hero_score == best_opp:
            payoff = pot * 0.5
        else:
            payoff = 0.0

        ev_sum += payoff - to_call

    return ev_sum / sims


if __name__ == "__main__":
    hero = ["As", "Ah"]
    ev = monte_carlo_ev(
        hero_hand=hero,
        board=[],
        pot=10.0,
        to_call=5.0,
        stack=100.0,
        num_opponents=1,
        sims=2000,
        rng=42,
    )
    print("EV:", ev)
