# user.py

class User:
    def __init__(self, username, pin, balance=0):
        self.username = username
        self.pin = pin
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        return self.balance

    def change_pin(self, new_pin):
        self.pin = new_pin
