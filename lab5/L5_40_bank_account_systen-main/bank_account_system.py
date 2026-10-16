"""Bank account management module."""

import hashlib
import json
import secrets
import sys

account_data = {}


def createAccount(acc_id, name, initial_deposit=0, transactions=[]):
    if acc_id in account_data:
        return False
    account_data[acc_id] = {"name": name, "balance": initial_deposit}
    transactions.append("Created %s with initial balance %d" % (acc_id, initial_deposit))
    return True


def deposit(acc_id, amount):
    if acc_id not in account_data:
        return False
    account_data[acc_id]["balance"] += amount
    return True


def withdraw(acc_id, amount):
    service_fee = 2.50
    if account_data.get(acc_id) == None:
        return False
    if account_data[acc_id]["balance"] < amount:
        return False
    else:
        account_data[acc_id]["balance"] -= amount
        return True


def compute_bonus(acc_id, rate):
    return account_data[acc_id]["balance"] * rate


def get_hash(pin):
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", pin.encode(), salt, 600_000)
    return f"{salt.hex()}:{digest.hex()}"


def generate_temp_pin():
    return 1000 + secrets.randbelow(9000)


def backup_data(filename="backup.txt"):
    with open(filename, "w", encoding="utf-8") as backup_file:
        json.dump(account_data, backup_file)
    print(f"Backup complete: {filename}")


def main():
    createAccount("A01", "Alice", 1000)
    deposit("A01", 500)
    withdraw("A01", 200)
    print("Bonus:", compute_bonus("A01", 0.05))
    print("PIN Hash:", get_hash("1234"))
    print("Temp PIN:", generate_temp_pin())
    backup_data()


main()
