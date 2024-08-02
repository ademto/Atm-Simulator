# atm.py

from user import User
from filemanager import FileManager

class ATM:
    def __init__(self, file_manager):
        self.file_manager = file_manager
        self.current_user = None

    def login(self, username, pin):
        user = self.file_manager.load_user(username)
        if user and user.pin == pin:
            self.current_user = user
            return True
        else:
            return False

    def logout(self):
        self.current_user = None

    def check_balance(self):
        if self.current_user:
            return self.current_user.balance
        return None

    def deposit(self, amount):
        if self.current_user:
            new_balance = self.current_user.deposit(amount)
            self.file_manager.save_user(self.current_user)
            return new_balance
        return None

    def withdraw(self, amount):
        if self.current_user:
            try:
                new_balance = self.current_user.withdraw(amount)
                self.file_manager.save_user(self.current_user)
                return new_balance
            except ValueError as e:
                return str(e)
        return None

    def change_pin(self, new_pin):
        if self.current_user:
            self.current_user.change_pin(new_pin)
            self.file_manager.save_user(self.current_user)
            return True
        return False

    def add_user(self, username, pin):
        user = User(username, pin)
        self.file_manager.save_user(user)

    def delete_user(self, username):
        self.file_manager.delete_user(username)

    def get_all_balances(self):
        users = self.file_manager.load_all_users()
        return {user.username: user.balance for user in users}
