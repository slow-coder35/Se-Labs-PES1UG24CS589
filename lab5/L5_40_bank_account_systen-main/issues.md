# Static analysis findings and fixes

Line numbers refer to the original `bank_account_system.py`. Severity follows Bandit where available; other rows identify the reporting tool. All listed issues were fixed.

| Issue | Type | Line(s) | Description | Fix approach |
|---|---|---:|---|---|
| B324: MD5 PIN hash | Security - High | 44 | Fast, unsalted MD5 is unsuitable for a PIN verifier. | Use a random 16-byte salt and PBKDF2-HMAC-SHA256 with 600,000 iterations; return salt and digest together. |
| B605: shell command | Security - High | 55 | A caller-controlled filename was concatenated into `os.system`, allowing shell injection. | Remove the shell call and print the completion message directly. |
| B307: `eval` | Security - Medium | 39 | A supplied bonus expression could execute arbitrary Python code. | Accept a numeric rate instead of an expression and calculate the bonus directly. |
| B105: hardcoded token | Security - Low | 59, 67 | A secret-like administrator token was embedded in code and printed. | Remove the unused token and its output. |
| B311: predictable PIN | Security - Low | 48 | `random.randint` is unsuitable for a security PIN. | Generate the PIN with `secrets.randbelow`. |
| B110 / W0702 / E722: swallowed exception | Security / bug | 20-23 | Bare `except` silently hid all deposit failures. | Check account existence and amount explicitly; return a success flag. |
| W0102: mutable default | Bug | 11 | `transactions=[]` was shared between calls. | Use `None` as the default and make a fresh list per account. |
| F841: unused service fee | Bug | 27 | The declared fee was never charged, making the code misleading. | Remove it and document the withdrawal behavior. |
| E711 / C0121: `None` comparison | Style | 28 | `== None` did not follow Python's singleton convention. | Replace the check with direct account membership. |
| F401 / W0611: unused import | Style | 6 | `sys` was unused. | Remove the import. |
| E501 / W292: layout | Style | 15, 70 | A long line and a missing final newline violated style checks. | Wrap long expressions and normalize the file's formatting. |
| C0103 / C0116: naming and documentation | Quality | 11-58 | Camel-case function naming and missing docstrings reduced clarity. | Rename `createAccount` to `create_account` and document functions. |
| W1514 / R1732: file handling | Quality | 52-54 | The backup file was opened without an encoding or context manager. | Use `with open(..., encoding="utf-8")` and write JSON. |
| `main()` at import | Behavior | 70 | Importing the module ran the demonstration and wrote a backup. | Put the demonstration behind a `__main__` guard. |
| Invalid money amounts | Behavior | 19-34 | Negative deposits or withdrawals could corrupt balances. | Reject nonpositive transaction amounts and negative opening deposits. |

## Verification

| Check | Before | After |
|---|---:|---:|
| Pylint score | 5.62/10 | 10.00/10 |
| Bandit findings | 6 (2 high, 1 medium, 3 low) | 0 |
| Flake8 findings | 7 | 0 |

See the paired `*_report_before.txt` and final `*_report.txt` files for the tool output.
