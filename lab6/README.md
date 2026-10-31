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

## Stage 2: branch coverage

```bash
coverage run --branch --source=ride_share_fare -m pytest -q BranchCoverageTest_ride_share_fare.py
coverage report -m --fail-under=90
coverage json -o reports/branch_coverage.json
```

Result: 52 tests pass; 37/37 statements and 26/26 branch outcomes covered (100%).
There are no missing or partial branches. The branch suite runs independently of
the code-coverage suite, with all expected values asserted.

The expanded cases cover both error exits; all cab allowances; subscriber versus
non-subscriber and SUV subscriber behavior; zero, included-limit and fractional
distances; city/non-city rates; exactly 20 versus over 20 extra kilometres; both
outcomes of the nested outstation surcharge; ordinary and wheelchair capacity
limits; excessive bags; and each scheduled/airport combination immediately above,
at and below the on-time and delayed cutoffs.

`coverage report` with `--branch` displays a combined line-and-branch percentage.
The JSON report separately verifies 26 covered branches out of 26, so branch-only
coverage is also 100%. Stage 1 already covers every line but misses the false
outcome of the nested `zone == "outstation"` surcharge decision (line 21): its
branch-only coverage is 25/26 (96.15%). The long city/other-zone cases in Stage 2
cover that missing outcome. This demonstrates why 100% line coverage alone does
not prove complete branch coverage.

Evidence: `screenshots/branch_coverage.png`, `reports/branch_coverage.txt`, and
`reports/branch_coverage.json`. Screenshots show actual terminal executions, and
only the completed stages have screenshots.

## Run all tests

```bash
pytest -q
```

`pytest.ini` discovers both handout-named deliverables as well as the two original
starter tests. Total: 65 passing tests. The application is unchanged; tests for
unknown zone strings and wheelchair bag handling document its existing behavior.
Coverage does not prove all input combinations or paths are correct, and
coverage.py does not separately measure each operand of a compound condition.

## Submission checklist

- `CodeCoverageTest_ride_share_fare.py`: code-coverage tests.
- `BranchCoverageTest_ride_share_fare.py`: branch-coverage tests.
- `screenshots/code_coverage.png`: terminal evidence above 90% line coverage.
- `screenshots/branch_coverage.png`: terminal evidence above 90% branch coverage.
- Two separate commits: first code-coverage tests/evidence, then branch tests/evidence.
