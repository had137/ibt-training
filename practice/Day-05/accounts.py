
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
        print(f"Error Caught: {e}")

    try:
        print("Attempting to deposit a negative amount...")
        acc2.deposit(-150)
    except ValueError as e:
        print(f" Error Caught: {e}")

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
        print(f" Paid interest at {self.interest_rate * 100}%: +{interest:,.2f} ETB")

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