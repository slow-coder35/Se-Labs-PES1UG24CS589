# Lab 6: Code and Branch Coverage - Ride Share Fare

Student: PES1UG24CS589

Source: https://github.com/SETAPESU26/L6_L7_40_ride_share_fare
Source commit: ee40b2b84e90255e47b16f56e8975da88a353f78

The application and original starter tests are copied unchanged from `Lab 6/`
in the assigned repository. Work is submitted in `lab6/` in the student's SE labs
repository as requested. The supplied handout is included for reference.

## Setup

Run from this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Initial measurements

Both original tests pass. Line coverage is 14/37 statements (38%).
The initial branch-enabled report gives 32% combined coverage; this is coverage.py's
combined statement-and-branch metric, not the branch-only percentage.
See `reports/initial_line_coverage.txt` and `reports/initial_branch_coverage.txt`.
Initial screenshots are deliberately omitted as required by the handout.

## Stage 1: code coverage

```bash
coverage run --source=ride_share_fare -m pytest -q CodeCoverageTest_ride_share_fare.py
coverage report -m --fail-under=90
```

Result: 11 tests pass; 37/37 executable statements covered (100%).
Tests cover invalid cab and distance errors, included and excess distances,
subscription allowance, outstation long-distance charges, capacity decisions,
and all three pickup statuses. Covering every line alone does not demonstrate
that all decision outcomes or boundary cases were tested.

Evidence: `screenshots/code_coverage.png`, `reports/code_coverage.txt`, and
`reports/code_coverage.json`. Coverage measures only `ride_share_fare.py`, so test
code does not inflate the application's reported coverage.
