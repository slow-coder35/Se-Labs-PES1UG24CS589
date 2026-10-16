# Lab 5: Static Code Analysis - Bank Account System

This project is the completed analysis and revision of `bank_account_system.py`.

## Run

```bash
python bank_account_system.py
```

The demonstration writes `backup.txt` as JSON in the current directory. Importing the module does not run the demonstration.

## Deliverables

- `bank_account_system.py`: revised bank account program.
- `issues.md`: findings, original line numbers, fixes, and before/after results.
- `reflection.md`: four reflection answers. The supplied handout refers to reflection questions but does not print them, so the answers follow its learning outcomes.
- `pylint_report_before.txt`, `bandit_report_before.txt`, `flake8_report_before.txt`: baseline tool output.
- `pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt`: final tool output.

This lab was added to the course repository in three commits: Bandit fixes with baseline reports, Pylint fixes, and Flake8 fixes with final reports. The final analysis result is Pylint 10.00/10, with no Bandit or Flake8 findings.
