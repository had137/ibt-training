# Day 7: Addis Bank — The Account Registry
# Theme: Linear Structures, Big-O Notation, Stacks, and Hash Maps (Dicts)
# Deliverable: registry.py

from abc import ABC, abstractmethod


# =====================================================================
# 1. Observer Pattern & SRP: Alert Services
# =====================================================================
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass


class SMSAlert(Observer):
    def __init__(self, phone_number):
        self.phone_number = phone_number

    def update(self, message):
        print(f"📱 [SMS to {self.phone_number}]: {message}")


class AlertService:
    def __init__(self):
        self._observers = []

    def subscribe(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer):
        self._observers.remove(observer)

    def _notify(self, message):
        for observer in self._observers:
            observer.update(message)


# =====================================================================
# 2. Base Class: Account (with Transaction History Stack)
# =====================================================================
class Account(AlertService, ABC):
    def __init__(self, owner, account_number, balance=0.0):
        super().__init__()
        self.owner = owner
        self.account_number = account_number
        self.__balance = float(balance)
        # Transaction History Stack (LIFO: Last In, First Out)
        self.history_stack = []

    @property
    def balance(self):
        return self.__balance

    def _adjust_balance(self, amount):
        self.__balance += amount

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive!")
        self._adjust_balance(amount)
        # Push transaction to stack
        self.history_stack.append(("DEPOSIT", amount))
        
        msg = f"Deposited {amount:,.2f} ETB into Account {self.account_number}. Balance: {self.__balance:,.2f} ETB."
        print(msg)
        self._notify(msg)

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive!")
        if amount > self.__balance:
            raise ValueError("Insufficient funds!")
        self._adjust_balance(-amount)
        # Push transaction to stack
        self.history_stack.append(("WITHDRAW", amount))
        
        msg = f"Withdrew {amount:,.2f} ETB from Account {self.account_number}. Balance: {self.__balance:,.2f} ETB."
        print(msg)
        self._notify(msg)

    def undo_last(self):
        """Pops the most recent transaction from the history stack and reverts it."""
        if not self.history_stack:
            print("⚠️ No transactions to undo!")
            return

        # Pop from stack (LIFO)
        tx_type, amount = self.history_stack.pop()
        
        if tx_type == "DEPOSIT":
            self._adjust_balance(-amount)
            msg = f"↩️ Undid Deposit of {amount:,.2f} ETB on Account {self.account_number}."
        elif tx_type == "WITHDRAW":
            self._adjust_balance(amount)
            msg = f"↩️ Undid Withdrawal of {amount:,.2f} ETB on Account {self.account_number}."

        print(msg)
        self._notify(msg)

    def statement(self):
        print("\n=====================================")
        print("             ADDIS BANK              ")
        print("          ACCOUNT STATEMENT          ")
        print("=====================================")
        print(f"Account Owner:  {self.owner}")
        print(f"Account Number: {self.account_number}")
        print(f"Current Balance: {self.balance:,.2f} ETB")


# =====================================================================
# 3. Account Subclasses
# =====================================================================
class SavingsAccount(Account):
    def __init__(self, owner, account_number, balance=0.0, interest_rate=0.05):
        super().__init__(owner, account_number, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self.balance * self.interest_rate
        self.deposit(interest)

    def statement(self):
        super().statement()
        print(f"Account Type:    Savings Account")
        print(f"Interest Rate:   {self.interest_rate * 100}%")
        print("=====================================")


class CurrentAccount(Account):
    def __init__(self, owner, account_number, balance=0.0, overdraft_limit=1000.0):
        super().__init__(owner, account_number, balance)
        self.overdraft_limit = float(overdraft_limit)

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive!")
        if amount > (self.balance + self.overdraft_limit):
            raise ValueError(f"Overdraft Limit of {self.overdraft_limit:,.2f} ETB Exceeded!")
        self._adjust_balance(-amount)
        # Push transaction to stack
        self.history_stack.append(("WITHDRAW", amount))
        
        msg = f"Withdrew {amount:,.2f} ETB (Overdraft active) from Account {self.account_number}. Balance: {self.balance:,.2f} ETB."
        print(msg)
        self._notify(msg)

    def statement(self):
        super().statement()
        print(f"Account Type:    Current Account")
        print(f"Overdraft Limit: {self.overdraft_limit:,.2f} ETB")
        print("=====================================")


# =====================================================================
# 4. AccountFactory
# =====================================================================
class AccountFactory:
    @staticmethod
    def create(kind, owner, account_number, balance=0.0, **kwargs):
        kind_lower = kind.lower()
        if kind_lower == "savings":
            rate = kwargs.get("interest_rate", 0.05)
            return SavingsAccount(owner, account_number, balance, interest_rate=rate)
        elif kind_lower == "current":
            limit = kwargs.get("overdraft_limit", 1000.0)
            return CurrentAccount(owner, account_number, balance, overdraft_limit=limit)
        else:
            raise ValueError(f"Unknown account kind: {kind}")


# =====================================================================
# 5. Account Registry (O(1) Hash Table Lookup)
# =====================================================================
class AccountRegistry:
    """Stores accounts in a dictionary for O(1) constant-time lookup."""
    def __init__(self):
        self._accounts = {}  # Dictionary key: account_number, value: Account object

    def add(self, account):
        """Adds an account to the registry."""
        self._accounts[account.account_number] = account
        print(f"Registered Account {account.account_number} for {account.owner}.")

    def find(self, account_number):
        """O(1) lookup by account number."""
        return self._accounts.get(account_number, None)

    def list_all(self):
        """Lists all registered accounts ordered by account number."""
        print("\n--- All Registered Accounts ---")
        for acc_num in sorted(self._accounts.keys()):
            acc = self._accounts[acc_num]
            print(f"- [{acc_num}] Owner: {acc.owner} | Balance: {acc.balance:,.2f} ETB")


# --- Test Run: Registry & Undo Stack ---
if __name__ == "__main__":
    print("--- Day 7: Addis Bank Account Registry & Undo Stack ---\n")

    # 1. Initialize Registry
    registry = AccountRegistry()

    # 2. Create and Register Accounts via Factory
    acc1 = AccountFactory.create("savings", "Almaz", "SAV-101", 5000, interest_rate=0.06)
    acc2 = AccountFactory.create("current", "Kassa", "CUR-202", 1000, overdraft_limit=1500)

    registry.add(acc1)
    registry.add(acc2)

    # 3. Test O(1) Lookup
    print("\n--- Testing O(1) Lookup ---")
    found_acc = registry.find("SAV-101")
    if found_acc:
        print(f"Found account for: {found_acc.owner}")

    # 4. List all registered accounts
    registry.list_all()

    # 5. Test Stack & Undo Functionality
    print("\n--- Testing Transaction Stack & Undo ---")
    found_acc.deposit(2000)   # Balance -> 7000
    found_acc.withdraw(1500)  # Balance -> 5500
    
    print(f"Current Balance before undo: {found_acc.balance:,.2f} ETB")
    
    # Undo withdrawal
    found_acc.undo_last()     # Balance -> 7000
    print(f"Balance after 1st undo: {found_acc.balance:,.2f} ETB")
    
    # Undo deposit
    found_acc.undo_last()     # Balance -> 5000
    print(f"Balance after 2nd undo: {found_acc.balance:,.2f} ETB")