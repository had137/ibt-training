# Day 4: Addis Bank — Account Management System (Version 1)
# Introducing Object-Oriented Programming, Encapsulation, and Properties

class Account:
    def __init__(self, owner, account_number, balance=0.0):
        """
        Initializes an Addis Bank account with an owner name, account number,
        and an encapsulated private balance.
        """
        self.owner = owner
        self.account_number = account_number
        # Private attribute (encapsulated) to protect it from direct modification
        self.__balance = float(balance)

    @property
    def balance(self):
        """Getter property to securely read the balance without direct attribute access."""
        return self.__balance

    def deposit(self, amount):
        """Adds funds to the balance with validation."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive!")
        self.__balance += amount
        print(f"Deposited: {amount:,.2f} ETB into Account {self.account_number}")

    def withdraw(self, amount):
        """Deducts funds from the balance if validation passes."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive!")
        if amount > self.__balance:
            raise ValueError(f"Insufficient funds! Available balance: {self.__balance:,.2f} ETB")
        self.__balance -= amount
        print(f"Withdrew: {amount:,.2f} ETB from Account {self.account_number}")

    def statement(self):
        """Prints a formatted bank statement."""
        print("\n=====================================")
        print("             ADDIS BANK              ")
        print("          ACCOUNT STATEMENT          ")
        print("=====================================")
        print(f"Account Owner:  {self.owner}")
        print(f"Account Number: {self.account_number}")
        print(f"Current Balance: {self.__balance:,.2f} ETB")
        print("=====================================\n")


# --- Test Run: Executing Transactions ---
if __name__ == "__main__":
    print("Initializing Addis Bank Accounts...")
    
    # 1. Create two bank accounts
    acc1 = Account("Almaz", "CBE-1001", 1500)
    acc2 = Account("Kassa", "CBE-1002", 500)

    # 2. Run transactions on Account 1
    acc1.statement()
    acc1.deposit(500)
    acc1.withdraw(200)
    acc1.statement()

    # 3. Test Validation & Error Handling on Account 2
    acc2.statement()
    try:
        print("Attempting to withdraw more than the balance...")
        acc2.withdraw(1000)
    except ValueError as e:
        print(f"❌ Error Caught: {e}")

    try:
        print("Attempting to deposit a negative amount...")
        acc2.deposit(-150)
    except ValueError as e:
        print(f"❌ Error Caught: {e}")