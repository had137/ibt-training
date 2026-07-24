# Day 5: Addis Bank — The Account Family
# Grown from Day 4's Account class with Inheritance & Polymorphism

class Account:
    def __init__(self, owner, account_number, balance=0.0):
        self.owner = owner
        self.account_number = account_number
        self.__balance = float(balance)

    @property
    def balance(self):
        return self.__balance

    def _adjust_balance(self, amount):
        """Internal helper to allow child classes to adjust balance safely."""
        self.__balance += amount

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive!")
        self._adjust_balance(amount)
        print(f"Deposited {amount:,.2f} ETB into account {self.account_number}.")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive!")
        if amount > self.__balance:
            raise ValueError("Insufficient funds!")
        self._adjust_balance(-amount)
        print(f"Withdrew {amount:,.2f} ETB from account {self.account_number}.")

    def statement(self):
        print("\n=====================================")
        print("             ADDIS BANK              ")
        print("          ACCOUNT STATEMENT          ")
        print("=====================================")
        print(f"Account Owner:  {self.owner}")
        print(f"Account Number: {self.account_number}")
        print(f"Current Balance: {self.__balance:,.2f} ETB")


# ==========================================
# Day 5 Growth: Inheritance & Specialization
# ==========================================

# 1. Savings Account (Grows on top of Account)
class SavingsAccount(Account):
    def __init__(self, owner, account_number, balance=0.0, interest_rate=0.05):
        super().__init__(owner, account_number, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        """Calculates interest and deposits it directly."""
        interest = self.balance * self.interest_rate
        self.deposit(interest)
        print(f"Paid interest at {self.interest_rate * 100}%: +{interest:,.2f} ETB")

    # Override statement() to identify as Savings
    def statement(self):
        super().statement()
        print(f"Account Type:    Savings Account")
        print(f"Interest Rate:   {self.interest_rate * 100}%")
        print("=====================================")


# 2. Current Account (Grows on top of Account)
class CurrentAccount(Account):
    def __init__(self, owner, account_number, balance=0.0, overdraft_limit=1000.0):
        super().__init__(owner, account_number, balance)
        self.overdraft_limit = float(overdraft_limit)

    # Override withdraw() to support overdraft
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive!")
        if amount > (self.balance + self.overdraft_limit):
            raise ValueError(f"Overdraft Limit of {self.overdraft_limit:,.2f} ETB Exceeded!")
        self._adjust_balance(-amount)
        print(f"Withdrew {amount:,.2f} ETB (Overdraft active) from account {self.account_number}.")

    # Override statement() to identify as Current
    def statement(self):
        super().statement()
        print(f"Account Type:    Current Account")
        print(f"Overdraft Limit: {self.overdraft_limit:,.2f} ETB")
        print("=====================================")


# --- Test Run: Polymorphism in Action ---
if __name__ == "__main__":
    print("--- Running Day 5 Addis Bank Program ---")
    
    # Create the account family
    savings = SavingsAccount("Almaz", "SAV-1001", 5000, interest_rate=0.06)
    current = CurrentAccount("Kassa", "CUR-2002", 300, overdraft_limit=1500)

    # Perform unique operations
    savings.add_interest()
    current.withdraw(1000) # Exceeds balance, utilizes overdraft!

    # Polymorphic loop: Loop through a mixed list and print statements
    accounts_list = [savings, current]
    
    print("\n--- Printing Statements via Polymorphism ---")
    for acc in accounts_list:
        acc.statement()