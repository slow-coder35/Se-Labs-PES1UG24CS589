# Reflection on static code analysis

The supplied handout asks for answers to reflection questions, but its three pages do not include the questions themselves. These four answers address the lab's stated learning outcomes.

## 1. What did each tool contribute?

Bandit highlighted security risks: MD5 for PINs, `eval`, shell execution, predictable random numbers, a hardcoded token, and swallowed exceptions. Pylint exposed maintainability problems such as the mutable default list, unused code, naming, and missing documentation. Flake8 caught layout and syntax-style issues. Together, the reports gave a useful checklist; the original program run also revealed the token printed to the terminal.

## 2. Which findings mattered most, and why?

The shell command and `eval` were the most urgent because caller-controlled input could run unintended commands or Python code. The MD5 PIN hash also mattered because PINs have a tiny search space. I fixed these before style warnings. I also removed the hardcoded token and changed temporary PIN generation to use `secrets`.

## 3. Did the tools find every problem?

No. The reports did not explain that negative deposits and withdrawals could alter balances in the wrong direction, or that importing the module ran the demo and wrote a file. Reviewing the code's behavior and testing edge cases caught those issues. Static analysis helps find suspicious patterns, but a human still has to decide the intended behavior.

## 4. How did the fixes improve the program, and what remains?

The final file passes all three tools: Pylint scores 10.00/10, and Bandit and Flake8 report no findings. The backup is now readable JSON, each account has its own transaction list, and invalid transactions return `False`. This is still a small in-memory demonstration, not a production bank system: balances use ordinary Python numbers, data is not stored in a database, and there is no authentication or concurrency control. A production version would need those features and a way to verify stored PIN digests.
