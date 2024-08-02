# filemanager.py

import os
from user import User

class FileManager:
    def __init__(self, directory='data'):
        self.directory = directory
        self.initial_setup_file = os.path.join(self.directory, "initial_setup_done.txt")
        os.makedirs(self.directory, exist_ok=True)
        self.initial_users = [
            User('User1', '1234', 1000),
            User('User2', '2222', 2000),
            User('User3', '3333', 3000),
            User('SysAdmin', '1357')
        ]
        self.setup_initial_users()

    def setup_initial_users(self):
        # Check if initial setup has already been done
        if not os.path.exists(self.initial_setup_file):
            for user in self.initial_users:
                if not os.path.exists(self.get_user_file(user.username)):
                    self.save_user(user)
            # Create the initial setup file to indicate that setup has been done
            with open(self.initial_setup_file, 'w') as file:
                file.write("Initial setup done")

    def get_user_file(self, username):
        return os.path.join(self.directory, f"{username}.txt")

    def save_user(self, user):
        with open(self.get_user_file(user.username), 'w') as file:
            file.write(f"{user.username},{user.pin},{user.balance}\n")

    def load_user(self, username):
        try:
            with open(self.get_user_file(username), 'r') as file:
                data = file.readline().strip().split(',')
                return User(data[0], data[1], float(data[2]))
        except FileNotFoundError:
            return None

    def delete_user(self, username):
        os.remove(self.get_user_file(username))

    def load_all_users(self):
        users = []
        for filename in os.listdir(self.directory):
            if filename.endswith('.txt') and filename != "initial_setup_done.txt":
                username, _ = os.path.splitext(filename)
                user = self.load_user(username)
                if user:
                    users.append(user)
        return users
