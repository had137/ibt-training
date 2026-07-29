# Day 8: Addis Bank — Sort & Search the Registry
# Theme: Searching, Sorting (Binary Search, Lambdas) & Recursion
from abc import ABC, abstractmethod
# 1. Observer Pattern & Alert Services
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass
class SMSAlert(Observer):
    def __init__(self, phone_number):
        self.phone_number = phone_number
    def update(self, message):
        print(f"[SMS to {self.phone_number}]: {message}")
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

# 2. Base Class: Account (with Recursive Transaction Total)
class Account(AlertService, ABC):
    def __init__(self, owner, account_number, balance=0.0):
        super().__init__()
        self.owner = owner
        self.account_number = account_number
        self.__balance = float(balance)
        self.history_stack = []  # Stack of tuples: ("DEPOSIT", amount) or ("WITHDRAW", amount)

    @property
    def balance(self):
        return self.__balance

    def _adjust_balance(self, amount):
        self.__balance += amount

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive!")
        self._adjust_balance(amount)
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
        self.history_stack.append(("WITHDRAW", amount))
        msg = f"Withdrew {amount:,.2f} ETB from Account {self.account_number}. Balance: {self.__balance:,.2f} ETB."
        print(msg)
        self._notify(msg)

    def undo_last(self):
        if not self.history_stack:
            print(" No transactions to undo!")
            return

        tx_type, amount = self.history_stack.pop()
        if tx_type == "DEPOSIT":
            self._adjust_balance(-amount)
            msg = f" Undid Deposit of {amount:,.2f} ETB on Account {self.account_number}."
        elif tx_type == "WITHDRAW":
            self._adjust_balance(amount)
            msg = f"Undid Withdrawal of {amount:,.2f} ETB on Account {self.account_number}."

        print(msg)
        self._notify(msg)

    def total_transactions(self, index=0):
        """Recursively calculates the sum of all transaction amounts in history_stack."""
        # Base case: when index reaches the end of history_stack
        if index >= len(self.history_stack):
            return 0.0 
        # Recursive step: current amount + total of remaining transactions
        _, amount = self.history_stack[index]
        return amount + self.total_transactions(index + 1)

    def statement(self):
        print("\n=====================================")
        print("             ADDIS BANK              ")
        print("          ACCOUNT STATEMENT          ")
        print("=====================================")
        print(f"Account Owner:  {self.owner}")
        print(f"Account Number: {self.account_number}")
        print(f"Current Balance: {self.balance:,.2f} ETB")
# 3. Account Subclasses
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
        self.history_stack.append(("WITHDRAW", amount))
        msg = f"Withdrew {amount:,.2f} ETB (Overdraft active) from Account {self.account_number}. Balance: {self.balance:,.2f} ETB."
        print(msg)
        self._notify(msg)

    def statement(self):
        super().statement()
        print(f"Account Type:    Current Account")
        print(f"Overdraft Limit: {self.overdraft_limit:,.2f} ETB")
        print("=====================================")
# 4. AccountFactory
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
# 5. Account Registry (Searching & Sorting)
class AccountRegistry:
    def __init__(self):
        self._accounts = {}

    def add(self, account):
        self._accounts[account.account_number] = account
        print(f"Registered Account {account.account_number} for {account.owner}.")

    def find(self, account_number):
        """O(1) lookup using dict."""
        return self._accounts.get(account_number, None)

    def find_by_number(self, account_number):
        """Binary Search O(log n) implementation on sorted list of accounts."""
        # Sort accounts by account number for binary search
        sorted_accounts = sorted(self._accounts.values(), key=lambda acc: acc.account_number)
        
        low = 0
        high = len(sorted_accounts) - 1
        
        while low <= high:
            mid = (low + high) // 2
            mid_acc_num = sorted_accounts[mid].account_number
            
            if mid_acc_num == account_number:
                return sorted_accounts[mid]
            elif mid_acc_num < account_number:
                low = mid + 1
            else:
                high = mid - 1
                
        return None

    def top_by_balance(self, n=3):
        """Returns top n accounts sorted by balance descending using lambda."""
        sorted_accounts = sorted(self._accounts.values(), key=lambda acc: acc.balance, reverse=True)
        return sorted_accounts[:n]

    def list_all(self):
        print("\n--- All Registered Accounts ---")
        for acc_num in sorted(self._accounts.keys()):
            acc = self._accounts[acc_num]
            print(f"- [{acc_num}] Owner: {acc.owner} | Balance: {acc.balance:,.2f} ETB")


# --- Test Run: Day 8 Exercises ---
if __name__ == "__main__":
    print("--- Day 8: Addis Bank Search, Sort & Recursion ---\n")

    registry = AccountRegistry()

    # Populate sample data
    acc1 = AccountFactory.create("savings", "Almaz", "SAV-101", 5000)
    acc2 = AccountFactory.create("current", "Kassa", "CUR-202", 12000)
    acc3 = AccountFactory.create("savings", "Bethlehem", "SAV-103", 8500)
    acc4 = AccountFactory.create("current", "Dawit", "CUR-204", 3000)

    for acc in [acc1, acc2, acc3, acc4]:
        registry.add(acc)

    # 1. Test Binary Search O(log n)
    print("\n--- Testing Binary Search (find_by_number) ---")
    target_number = "SAV-103"
    result = registry.find_by_number(target_number)
    if result:
        print(f"Binary Search Found: {result.owner} (Account: {result.account_number})")
    else:
        print(f"Account {target_number} not found.")

    # 2. Test Leaderboard (top_by_balance with lambda)
    print("\n--- Testing Leaderboard (top_by_balance) ---")
    leaderboard = registry.top_by_balance(3)
    for rank, acc in enumerate(leaderboard, 1):
        print(f"Rank {rank}: {acc.owner} ({acc.account_number}) - Balance: {acc.balance:,.2f} ETB")

    # 3. Test Recursive total_transactions()
    print("\n--- Testing Recursive Total Transactions ---")
    acc1.deposit(1000)
    acc1.withdraw(500)
    acc1.deposit(200)

    rec_total = acc1.total_transactions()
    print(f" Recursive sum of transaction amounts for {acc1.owner}: {rec_total:,.2f} ETB")