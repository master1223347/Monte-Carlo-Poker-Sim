#!/usr/bin/env python3
# scripts/run_ev.py
# simple CLI to run equity and EV Monte Carlo for a given poker state
import sys
from pathlib import Path
import argparse
import time

# ensure project src is importable when running the script in-place
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

#IGNORE ANY RUFF ERRORS 
from src.state import PokerState
from src.equity import monte_carlo_equity
from src.ev import monte_carlo_ev


def parse_cards_arg(s: str):
    # accept empty string as no cards
    if s is None:
        return []
    s = s.strip()
    if s == "":
        return []
    return s.split()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run Monte Carlo equity and EV for a poker state")
    parser.add_argument("hero", help='Hero hole cards as two cards in quotes, e.g. "Ah Kh"')
    parser.add_argument("-b", "--board", default="", help='Community cards space separated, e.g. "Qs Jh 2c"')
    parser.add_argument("--pot", type=float, default=0.0, help="Current pot size")
    parser.add_argument("--to_call", type=float, default=0.0, help="Amount required to call")
    parser.add_argument("--stack", type=float, default=100.0, help="Hero stack size")
    parser.add_argument("-n", "--num_opponents", type=int, default=1, help="Number of opponents")
    parser.add_argument("-s", "--sims", type=int, default=5000, help="Monte Carlo simulations")
    parser.add_argument("--seed", type=int, default=None, help="Optional RNG seed")
    args = parser.parse_args(argv)

    hero_cards = parse_cards_arg(args.hero)
    board_cards = parse_cards_arg(args.board)

    # build and validate state via PokerState
    state = PokerState.from_strings(
        hero_hand=" ".join(hero_cards),
        board=" ".join(board_cards),
        pot=args.pot,
        to_call=args.to_call,
        stack=args.stack,
        num_opponents=args.num_opponents,
        street="preflop" if len(board_cards) == 0 else ("flop" if len(board_cards) == 3 else ("turn" if len(board_cards) == 4 else "river"))
    )

    print("Running Monte Carlo with the following state:")
    print(state)
    print(f"sims={args.sims} num_opponents={args.num_opponents} seed={args.seed}")
    print()

    # run equity first (pure win/tie probability)
    t0 = time.perf_counter()
    equity = monte_carlo_equity(
        hero_hand=state.hero_hand,
        board=state.board,
        num_opponents=state.num_opponents,
        sims=args.sims,
        rng=args.seed,
    )
    t1 = time.perf_counter()

    # run EV (money expectation given pot and to_call)
    ev = monte_carlo_ev(
        hero_hand=state.hero_hand,
        board=state.board,
        pot=state.pot,
        to_call=state.to_call,
        stack=state.stack,
        num_opponents=state.num_opponents,
        sims=args.sims,
        rng=args.seed,
    )
    t2 = time.perf_counter()

    print(f"equity (win+0.5*tie): {equity:.4f}    (computed in {t1-t0:.2f}s)")
    print(f"ev (per-hand average if you call now): {ev:.4f}    (computed in {t2-t1:.2f}s)")
    print()
    print("Interpretation:")
    print(" - equity is probability of winning the showdown (ties half credit).")
    print(" - ev is expected money change if you put in to_call and proceed to showdown assuming no further betting.")
    print()
    print("Notes:")
    print(" - Raise logic and opponent folding behavior are not modeled here.")
    print(" - Use larger sims for more stable estimates (but it will be slower).")


if __name__ == "__main__":
    main()
