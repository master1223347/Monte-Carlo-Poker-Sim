# Monte Carlo Poker Engine

A clean and minimal Monte Carlo poker simulator focused on estimating
equity and expected value (EV) for Texas Hold’em hands.

The project is designed to be small, explicit, and numerically correct.

---

## What this project does

- Simulates random poker outcomes using Monte Carlo sampling
- Estimates:
  - Equity (win probability with ties counted as half)
  - Expected Value (EV) given pot size and call cost
- Supports:
  - Any two card hero hand
  - Partial or complete community boards
  - Any number of opponents
- Uses a real hand evaluator via the treys library

---

## Core concepts

Monte Carlo simulation is used to approximate expectations by repeated
random sampling.

- Equity is the expected win rate at showdown
- EV is the expected money change if the hand goes to showdown after calling

Both are computed by simulating many possible completions of the hand.

---

## Project structure

project/
├── src/
│   ├── cards.py        Card and deck utilities
│   ├── state.py        PokerState definition and validation
│   ├── equity.py       Monte Carlo equity estimation
│   ├── ev.py           Monte Carlo EV estimation
│   └── __init__.py
│
├── scripts/
│   └── run_ev.py       Command line runner for simulations
│
├── tests/
│   ├── test_equity.py
│   └── test_ev.py
│
├── requirements.txt
├── .gitignore
└── README.md

---

## Installation

Install dependencies with:

    pip install -r requirements.txt

Required packages:
- treys for hand evaluation
- pytest for running tests

---

## Running tests

From the project root, run:

    pytest

Monte Carlo simulations use fixed random seeds in tests to keep results stable.

---

## Running a simulation

Example usage:

    python scripts/run_ev.py "Ah As" --pot 10 --to_call 5 --num_opponents 1 --sims 5000 --seed 42

The script prints:
- The parsed poker state
- Estimated equity
- Estimated EV
- Timing information

---

## Interpreting results

Equity:
- Probability of winning at showdown
- Ties count as half a win

EV:
- Average money gained or lost if you call now
- Calculated as expected payoff minus the call cost
- Assumes no further betting

Positive EV indicates a profitable call in expectation.

---

## Disclaimer

This software is for educational and analytical purposes.
Poker involves risk and variance.

No guarantees are implied.