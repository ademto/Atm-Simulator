# gui.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from atm import ATM
from filemanager import FileManager
import matplotlib.pyplot as plt
import seaborn as sns


class ATM_GUI:
    def __init__(self, root, atm):
        self.root = root
        self.atm = atm

        self.root.title("ATM Simulator")
        self.center_window(400, 400)

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20, padx=20)

        self.create_login_screen()

    def center_window(self, width, height):
        """Center the window on the screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def create_login_screen(self):
        """Create the login screen UI."""
        self.clear_frame()

        tk.Label(self.main_frame, text="Username", font=('Helvetica', 14), fg='black').grid(row=0, column=0, pady=10, padx=10)
        self.username_entry = tk.Entry(self.main_frame, font=('Helvetica', 14))
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(self.main_frame, text="PIN", font=('Helvetica', 14), fg='black').grid(row=1, column=0, pady=10, padx=10)
        self.pin_entry = tk.Entry(self.main_frame, show="*", font=('Helvetica', 14))
        self.pin_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Button(self.main_frame, text="Login", command=self.login, bg='#4caf50', fg='black', font=('Helvetica', 14)).grid(row=2, columnspan=2, pady=20)

    def create_main_menu(self, is_admin=False):
        """Create the main menu UI."""
        self.clear_frame()

        

        if is_admin:
            tk.Button(self.main_frame, text="Add User", command=self.add_user, bg='#03a9f4', fg='black', font=('Helvetica', 14)).grid(row=5, columnspan=2, pady=10, padx=10)
            tk.Button(self.main_frame, text="Delete User", command=self.delete_user, bg='#03a9f4', fg='black', font=('Helvetica', 14)).grid(row=6, columnspan=2, pady=10, padx=10)
            tk.Button(self.main_frame, text="Plot All Balances", command=self.plot_all_balances, bg='#03a9f4', fg='black', font=('Helvetica', 14)).grid(row=7, columnspan=2, pady=10, padx=10)
            tk.Button(self.main_frame, text="Change PIN", command=self.change_pin, bg='#9c27b0', fg='black', font=('Helvetica', 14)).grid(row=3, columnspan=2, pady=10, padx=10)
            tk.Button(self.main_frame, text="Logout", command=self.logout, bg='#f44336', fg='black', font=('Helvetica', 14)).grid(row=4, columnspan=2, pady=20, padx=10)
        else:
            tk.Button(self.main_frame, text="Check Balance", command=self.check_balance, bg='#2196f3', fg='black', font=('Helvetica', 14)).grid(row=0, columnspan=2, pady=10, padx=10)
            tk.Button(self.main_frame, text="Deposit", command=self.deposit, bg='#4caf50', fg='black', font=('Helvetica', 14)).grid(row=1, columnspan=2, pady=10, padx=10)
            tk.Button(self.main_frame, text="Withdraw", command=self.withdraw, bg='#ff9800', fg='black', font=('Helvetica', 14)).grid(row=2, columnspan=2, pady=10, padx=10)
            tk.Button(self.main_frame, text="Change PIN", command=self.change_pin, bg='#9c27b0', fg='black', font=('Helvetica', 14)).grid(row=3, columnspan=2, pady=10, padx=10)
            tk.Button(self.main_frame, text="Logout", command=self.logout, bg='#f44336', fg='black', font=('Helvetica', 14)).grid(row=4, columnspan=2, pady=20, padx=10)
            tk.Button(self.main_frame, text="Plot My Balance", command=self.plot_my_balance, bg='#03a9f4', fg='black', font=('Helvetica', 14)).grid(row=8, columnspan=2, pady=10, padx=10)

    def login(self):
        """Handle user login."""
        username = self.username_entry.get()
        pin = self.pin_entry.get()
        if self.atm.login(username, pin):
            
            # print(is_admin = username == "SysAdmin")
            is_admin = username == "SysAdmin"
            self.create_main_menu(is_admin)
        else:
            messagebox.showerror("Error", "Invalid username or PIN")

    def logout(self):
        """Handle user logout."""
        self.atm.logout()
        self.create_login_screen()

    def check_balance(self):
        """Check the current user's balance."""
        balance = self.atm.check_balance()
        if balance is not None:
            messagebox.showinfo("Balance", f"Your balance is: ${balance:.2f}")
        else:
            messagebox.showerror("Error", "Failed to retrieve balance")

    def deposit(self):
        """Handle deposit transactions."""
        amount = self.get_amount("Deposit")
        if amount is not None:
            new_balance = self.atm.deposit(amount)
            if new_balance is not None:
                messagebox.showinfo("Deposit", f"Deposited ${amount:.2f}. New balance: ${new_balance:.2f}")
            else:
                messagebox.showerror("Error", "Failed to deposit amount")

    def withdraw(self):
        """Handle withdrawal transactions."""
        amount = self.get_amount("Withdraw")
        if amount is not None:
            result = self.atm.withdraw(amount)
            if isinstance(result, str):
                messagebox.showerror("Error", result)
            else:
                messagebox.showinfo("Withdraw", f"Withdrew ${amount:.2f}. New balance: ${result:.2f}")

    def change_pin(self):
        """Handle PIN change."""
        new_pin = self.get_new_pin()
        if new_pin is not None:
            success = self.atm.change_pin(new_pin)
            if success:
                messagebox.showinfo("Change PIN", "PIN changed successfully")
            else:
                messagebox.showerror("Error", "Failed to change PIN")

    def add_user(self):
        """Add a new user."""
        username = simpledialog.askstring("Add User", "Enter new username:")
        pin = simpledialog.askstring("Add User", "Enter new PIN:", show="*")
        if username and pin:
            self.atm.add_user(username, pin)
            messagebox.showinfo("Add User", f"User {username} added successfully")

    def delete_user(self):
        """Delete an existing user."""
        username = simpledialog.askstring("Delete User", "Enter username to delete:")
        if username:
            self.atm.delete_user(username)
            messagebox.showinfo("Delete User", f"User {username} deleted successfully")

    def plot_all_balances(self):
        """Plot all users' balances."""
        balances = self.atm.get_all_balances()
        usernames = list(balances.keys())
        values = list(balances.values())

        plt.figure(figsize=(10, 6))
        sns.barplot(x=usernames, y=values, palette="viridis")
        plt.xlabel('User')
        plt.ylabel('Balance')
        plt.title('All User Balances')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_my_balance(self):
        """Plot the current user's balance."""
        balance = self.atm.check_balance()
        if balance is not None:
            plt.figure(figsize=(6, 6))
            plt.pie([balance, 1], labels=[f'{self.atm.current_user.username}: ${balance:.2f}', ''], colors=['#4caf50', '#f0f0f0'], startangle=90, autopct='%1.1f%%')
            plt.title('My Balance')
            plt.show()
        else:
            messagebox.showerror("Error", "Failed to retrieve balance")

    def get_amount(self, transaction_type):
        """Get the transaction amount from the user."""
        amount_str = simpledialog.askstring(transaction_type, "Enter amount:")
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
            return amount
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Invalid amount")
            return None

    def get_new_pin(self):
        """Get a new PIN from the user."""
        new_pin = simpledialog.askstring("Change PIN", "Enter new PIN:", show="*")
        confirm_pin = simpledialog.askstring("Change PIN", "Confirm new PIN:", show="*")
        if new_pin != confirm_pin:
            messagebox.showerror("Error", "PINs do not match")
            return None
        return new_pin

    def clear_frame(self):
        """Clear all widgets from the frame."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()


def main():
    root = tk.Tk()
    file_manager = FileManager()
    atm = ATM(file_manager)
    ATM_GUI(root, atm)
    root.mainloop()


if __name__ == "__main__":
    main()
