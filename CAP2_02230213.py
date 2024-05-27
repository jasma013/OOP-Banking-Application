#JASMA TAMANG
#STUDENT NUMBER: 02230213
#BE. INSTRUMENTATION AND CONTROL ENGINEERING FIRST YEAR
#CSF101-CAP2
#OOP-BANKING-APPLICATION

#REFERENCES







import random
import json

class Account:
    def __init__(self, account_number, balance, account_type, password):
        self.account_number = account_number
        self.balance = balance
        self.account_type = account_type
        self.password = password

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        else:
            return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        else:
            return False

    def validate_password(self, password):
        return self.password == password

    def transfer_funds(self, amount, recipient_account):
        if 0 < amount <= self.balance:
            self.balance -= amount
            recipient_account.deposit(amount)
            return True
        else:
            return False

class Bank:
    def __init__(self):
        self.accounts = {}
        self.load_accounts()

    def open_account(self):
        account_number = random.randint(1000000, 9999999)
        while account_number in self.accounts:
            account_number = random.randint(1000000, 9999999)

        account_type = input("Enter account type (Personal/Business): ").strip().capitalize()
        password = "BoT2024"  # Default password set to "BoT2024"

        account = Account(account_number, 0, account_type, password)
        self.accounts[account_number] = account.__dict__
        self.save_accounts()
        return account_number

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]
            self.save_accounts()
            return True
        else:
            return False

    def load_accounts(self):
        try:
            with open("accounts.txt", "r") as file:
                self.accounts = json.load(file)
        except FileNotFoundError:
            pass

    def save_accounts(self):
        with open("accounts.txt", "w") as file:
            json.dump(self.accounts, file)

def main():
    bank = Bank()
    while True:
        print("\nBank of Technologist")
        print("1. Open Account")
        print("2. Login to your account")
        print("3. Transfer Funds")
        print("4. Delete Account")
        print("5. Close the session")
        choice = input("Please provide your selection: ").strip()

        if choice == '1':
            account_number = bank.open_account()
            print(f"Account created successfully. Your account number is {account_number}.")
            print("Do not share your account number and password to maintain security.")

        elif choice == '2':
            try:
                account_number = int(input("Provide your account number: ").strip())
            except ValueError:
                print("Invalid account number format.")
                continue
            account_info = bank.get_account(account_number)
            if account_info:
                default_password = "BoT2024"  # Default password set to "BoT2024"
                password = input(f"Enter your password (default password is '{default_password}' if not changed): ").strip()
                if account_info["password"] == password:
                    print(f"Logged in successfully. Account type: {account_info['account_type']}")
                    while True:
                        print("\n1. Check my balance")
                        print("2. Deposit cash")
                        print("3. Withdraw cash")
                        print("4. Close session")
                        option = input("Please provide your selection: ").strip()

                        if option == '1':
                            print(f"Your current balance is:Nu. {account_info['balance']}")
                        elif option == '2':
                            try:
                                amount = float(input("Enter the  amount to deposit: ").strip())
                            except ValueError:
                                print("Invalid amount format.Please provide in numbers.")
                                continue
                            account = Account(account_number, account_info['balance'], account_info['account_type'], password)
                            if account.deposit(amount):
                                print("Amount successfully deposited.")
                                bank.accounts[account_number]["balance"] = account.balance
                                bank.save_accounts()
                            else:
                                print("Invalid amount.")
                        elif option == '3':
                            try:
                                amount = float(input("Enter the amount to withdraw: ").strip())
                            except ValueError:
                                print("Invalid amount format.Please provide in numbers.")
                                continue
                            account = Account(account_number, account_info['balance'], account_info['account_type'], password)
                            if account.withdraw(amount):
                                print("Amount successfully withdrawed.")
                                bank.accounts[account_number]["balance"] = account.balance
                                bank.save_accounts()
                            else:
                                print("Insufficient fund or invalid amount.")
                        elif option == '4':
                            print("Session closed successfully.")
                            break
                        else:
                            print("Invalid choice.")
                else:
                    print("Invalid password.")
            else:
                print("Sorry. Account not found.\n Check your password.")

        elif choice == '3':
            try:
                sender_account_number = int(input("Enter your account number: ").strip())
                recipient_account_number = int(input("Enter recipient's account number: ").strip())
                amount = float(input("Enter the amount to transfer: ").strip())
            except ValueError:
                print("Invalid input format.")
                continue

            sender_info = bank.get_account(sender_account_number)
            recipient_info = bank.get_account(recipient_account_number)

            if sender_info and recipient_info:
                sender_password = input("Enter your password: ").strip()
                if sender_info["password"] == sender_password:
                    sender_account = Account(sender_account_number, sender_info['balance'], sender_info['account_type'], sender_password)
                    recipient_account = Account(recipient_account_number, recipient_info['balance'], recipient_info['account_type'], recipient_info['password'])

                    if sender_account.transfer_funds(amount, recipient_account):
                        print("Funds transferred successfully.")
                        bank.accounts[sender_account_number]["balance"] = sender_account.balance
                        bank.accounts[recipient_account_number]["balance"] = recipient_account.balance
                        bank.save_accounts()
                    else:
                        print("Insufficient fund or invalid amount.")
                else:
                    print("Invalid password.")
            else:
                print("One or both accounts does not exist. Please check your account number.")

        elif choice == '4':
            try:
                account_number = int(input("Enter the  account number to delete: ").strip())
            except ValueError:
                print("Invalid account number format.Please provide in numbers.")
                continue
            if bank.delete_account(account_number):
                print("Account deleted successfully.")
            else:
                print("Account not found.")

        elif choice == '5':
            print("Session closed. Thank you for choosing Bank Of Technologist. Visit us again.")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
