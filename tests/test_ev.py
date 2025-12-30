# tests/test_ev.py
# pytest tests for the monte carlo EV engine
from src.ev import monte_carlo_ev

import sys
from pathlib import Path
import pytest

# make project importable
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))



def test_aa_preflop_positive_ev():
    # AA vs one random opponent with pot > to_call should have positive EV
    ev = monte_carlo_ev(
        hero_hand=["As", "Ah"],
        board=[],
        pot=10.0,
        to_call=5.0,
        stack=100.0,
        num_opponents=1,
        sims=3000,
        rng=42,
    )
    assert ev > 0.0


def test_ev_within_theoretical_bounds():
    # EV should be between -to_call and pot - to_call
    pot = 10.0
    to_call = 5.0
    ev = monte_carlo_ev(
        hero_hand=["Ks", "Qs"],
        board=["2c", "7d", "9h"],
        pot=pot,
        to_call=to_call,
        stack=100.0,
        num_opponents=1,
        sims=2000,
        rng=7,
    )
    lower = -to_call - 1e-8
    upper = pot - to_call + 1e-8
    assert lower <= ev <= upper


def test_zero_pot_and_zero_to_call_returns_zero_ev():
    ev = monte_carlo_ev(
        hero_hand=["2s", "7d"],
        board=[],
        pot=0.0,
        to_call=0.0,
        stack=100.0,
        num_opponents=1,
        sims=100,
        rng=1,
    )
    assert abs(ev) < 1e-8


def test_duplicate_cards_raise_value_error():
    with pytest.raises(ValueError):
        monte_carlo_ev(
            hero_hand=["Ah", "Ah"],
            board=[],
            pot=10.0,
            to_call=5.0,
            stack=100.0,
            num_opponents=1,
            sims=100,
            rng=1,
        )


def test_invalid_card_string_raises():
    with pytest.raises(ValueError):
        monte_carlo_ev(
            hero_hand=["Xh", "Ah"],
            board=[],
            pot=10.0,
            to_call=5.0,
            stack=100.0,
            num_opponents=1,
            sims=100,
            rng=1,
        )
