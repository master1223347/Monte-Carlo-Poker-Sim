# tests/test_equity.py
# pytest tests for the monte carlo equity engine
from src.equity import monte_carlo_equity

import sys
from pathlib import Path
import pytest

# ensure project root is importable so we can import src as a package
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))




def test_aa_preflop_has_high_equity():
    # AA vs one random opponent should be very strong
    eq = monte_carlo_equity(hero_hand=["As", "Ah"], board=[], num_opponents=1, sims=3000, rng=42)
    assert 0.8 < eq < 1.0


def test_equity_in_range_multiple_opponents():
    # Equity must always be between 0 and 1 even with multiple opponents
    eq = monte_carlo_equity(hero_hand=["As", "Ah"], board=["Ks", "Qh", "2c"], num_opponents=2, sims=2000, rng=123)
    assert 0.0 <= eq <= 1.0


def test_duplicate_cards_raise_value_error():
    # Duplicate card in hero hand should raise an error
    with pytest.raises(ValueError):
        monte_carlo_equity(hero_hand=["Ah", "Ah"], board=[], num_opponents=1, sims=100, rng=1)


def test_invalid_card_string_raises():
    # Invalid card format should raise an error
    with pytest.raises(ValueError):
        monte_carlo_equity(hero_hand=["Xh", "Ah"], board=[], num_opponents=1, sims=100, rng=1)
