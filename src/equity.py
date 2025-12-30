from typing import List, Optional
import random

from .cards import Deck, is_valid_card
try:
    from treys import Evaluator, Card
except Exception as exc:
    raise ImportError("treys is required. Install with `pip install treys`.") from exc

EVALUATOR = Evaluator()


def _make_rng(rng) -> random.Random:
    # accept None, int seed, or random.Random
    if rng is None:
        return random.Random()
    if isinstance(rng, random.Random):
        return rng
    if isinstance(rng, int):
        return random.Random(rng)
    raise TypeError("rng must be None, int seed, or random.Random")


def _validate_inputs(hero_hand: List[str], board: Optional[List[str]], num_opponents: int, sims: int) -> None:
    # basic argument validation
    if not isinstance(hero_hand, (list, tuple)) or len(hero_hand) != 2:
        raise ValueError("hero_hand must be a list of exactly two card strings")
    for c in hero_hand:
        if not is_valid_card(c):
            raise ValueError(f"invalid hero card: {c}")
    if board is None:
        board = []
    if not isinstance(board, (list, tuple)):
        raise ValueError("board must be a list of card strings")
    if len(board) > 5:
        raise ValueError("board cannot have more than 5 cards")
    for c in board:
        if not is_valid_card(c):
            raise ValueError(f"invalid board card: {c}")
    if num_opponents < 1:
        raise ValueError("num_opponents must be >= 1")
    if sims <= 0:
        raise ValueError("sims must be positive")


def monte_carlo_equity(
    hero_hand: List[str],
    board: Optional[List[str]] = None,
    num_opponents: int = 1,
    sims: int = 5000,
    rng: Optional[object] = None,
) -> float:
    # return hero equity as (wins + 0.5 * ties) / sims
    _validate_inputs(hero_hand, board, num_opponents, sims)
    board = board or []
    rng_obj = _make_rng(rng)

    wins = 0
    ties = 0

    # do sims iterations, creating a fresh shuffled deck each sim seeded by the same RNG stream
    for _ in range(sims):
        deck = Deck(rng=rng_obj)  # deck uses rng_obj for shuffling
        # remove known cards
        try:
            deck.remove(hero_hand + board)
        except ValueError:
            # duplicate or invalid removal will raise; propagate with clearer message
            raise ValueError("duplicate or invalid known card detected in hero_hand or board")

        # draw opponent hole cards
        opp_hands_raw = deck.draw(2 * num_opponents)
        # build opponent hands as list of pairs
        opp_hands = [opp_hands_raw[i : i + 2] for i in range(0, len(opp_hands_raw), 2)]

        # draw remaining board cards
        remaining = 5 - len(board)
        future_board_raw = deck.draw(remaining) if remaining > 0 else []
        full_board = list(board) + future_board_raw

        # convert to treys integers for evaluation
        hero_cards_t = [Card.new(c) for c in hero_hand]
        board_t = [Card.new(c) for c in full_board]
        hero_score = EVALUATOR.evaluate(board_t, hero_cards_t)

        opp_scores = []
        for opp in opp_hands:
            opp_cards_t = [Card.new(c) for c in opp]
            opp_scores.append(EVALUATOR.evaluate(board_t, opp_cards_t))

        best_opp = min(opp_scores)

        if hero_score < best_opp:
            wins += 1
        elif hero_score == best_opp:
            ties += 1
        # else hero loses; no counter needed

    return (wins + 0.5 * ties) / sims


if __name__ == "__main__":
    # quick manual check: AA vs random preflop should be strong
    hero = ["As", "Ah"]
    eq = monte_carlo_equity(hero_hand=hero, board=[], num_opponents=1, sims=2000, rng=42)
    print("AA vs 1 random opponent equity ~", eq)
