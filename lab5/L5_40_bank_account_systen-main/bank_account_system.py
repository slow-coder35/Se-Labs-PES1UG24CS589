"""Manage a small in-memory bank account ledger."""

import hashlib
import json
import secrets

account_data = {}


def create_account(acc_id, name, initial_deposit=0, transactions=None):
    """Create an account and record its opening transaction."""
    if acc_id in account_data or initial_deposit < 0:
        return False
    if transactions is None:
        transactions = []
    transactions.append(
        f"Created {acc_id} with initial balance {initial_deposit}"
    )
    account_data[acc_id] = {
        "name": name,
        "balance": initial_deposit,
        "transactions": transactions,
    }
    return True


def deposit(acc_id, amount):
    """Deposit a positive amount into an existing account."""
    if acc_id not in account_data or amount <= 0:
        return False
    account_data[acc_id]["balance"] += amount
    account_data[acc_id]["transactions"].append(f"Deposited {amount}")
    return True


def withdraw(acc_id, amount):
    """Withdraw a positive amount if the account has enough funds."""
    if acc_id not in account_data or amount <= 0:
        return False
    if account_data[acc_id]["balance"] < amount:
        return False
    account_data[acc_id]["balance"] -= amount
    account_data[acc_id]["transactions"].append(f"Withdrew {amount}")
    return True


def compute_bonus(acc_id, rate):
    """Calculate a bonus from a rate between zero and one."""
    if not 0 <= rate <= 1:
        raise ValueError(
            "Bonus rate must be between zero and one, inclusive, "
            "for this promotion"
        )
    return account_data[acc_id]["balance"] * rate


def get_hash(pin):
    """Return a salted PBKDF2 digest suitable for storing a PIN verifier."""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", pin.encode(), salt, 600_000)
    return f"{salt.hex()}:{digest.hex()}"


def generate_temp_pin():
    """Generate an unpredictable four-digit temporary PIN."""
    return 1000 + secrets.randbelow(9000)


def backup_data(filename="backup.txt"):
    """Write the account ledger as UTF-8 JSON."""
    with open(filename, "w", encoding="utf-8") as backup_file:
        json.dump(account_data, backup_file, indent=2)
    print(f"Backup complete: {filename}")


def main():
    """Run a short demonstration of account operations."""
    create_account("A01", "Alice", 1000)
    deposit("A01", 500)
    withdraw("A01", 200)
    print("Bonus:", compute_bonus("A01", 0.05))
    print("PIN Hash:", get_hash("1234"))
    print("Temp PIN:", generate_temp_pin())
    backup_data()


if __name__ == "__main__":
    main()
