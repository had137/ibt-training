# Day 9: Addis Bank — Trees & Graphs (Branch Hierarchy & Transfer Graph)
# Theme: Trees (Hierarchy), Graph Traversal (BFS), and Recursion
from abc import ABC, abstractmethod
from collections import deque
# 1. Observer Pattern & Alert Services
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass
class SMSAlert(Observer):
    def __init__(self, phone_number):
        self.phone_number = phone_number

    def update(self, message):
        print(f" [SMS to {self.phone_number}]: {message}")


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

# 2. Base Class: Account
class Account(AlertService, ABC):
    def __init__(self, owner, account_number, balance=0.0):
        super().__init__()
        self.owner = owner
        self.account_number = account_number
        self.__balance = float(balance)
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
            msg = f"Undid Deposit of {amount:,.2f} ETB on Account {self.account_number}."
        elif tx_type == "WITHDRAW":
            self._adjust_balance(amount)
            msg = f"Undid Withdrawal of {amount:,.2f} ETB on Account {self.account_number}."

        print(msg)
        self._notify(msg)

    def total_transactions(self, index=0):
        if index >= len(self.history_stack):
            return 0.0
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
# 5. Account Registry
class AccountRegistry:
    def __init__(self):
        self._accounts = {}

    def add(self, account):
        self._accounts[account.account_number] = account

    def find(self, account_number):
        return self._accounts.get(account_number, None)

    def find_by_number(self, account_number):
        sorted_accounts = sorted(self._accounts.values(), key=lambda acc: acc.account_number)
        low, high = 0, len(sorted_accounts) - 1
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
        return sorted(self._accounts.values(), key=lambda acc: acc.balance, reverse=True)[:n]
# 6. Tree Structure: Branch Hierarchy & Recursive Total Balance
class BranchNode:
    """Represents a node in the bank's organizational tree (Head Office -> Regions -> Branches)."""
    def __init__(self, name):
        self.name = name
        self.accounts = []      # List of Account objects in this branch
        self.children = []      # List of sub-branches (regions or local branches)

    def add_child(self, child_node):
        self.children.append(child_node)

    def add_account(self, account):
        self.accounts.append(account)

    def total_balance(self):
        """Recursively calculates total balance across this node and all sub-branches."""
        # Sum direct account balances at this node
        direct_total = sum(acc.balance for acc in self.accounts)
        
        # Recursive step: sum total_balance of all child nodes
        children_total = sum(child.total_balance() for child in self.children)
        
        return direct_total + children_total
# 7. Graph Structure: Transfer Network & Breadth-First Search (BFS)
class TransferGraph:
    """Graph modeling inter-branch/account transaction transfer channels."""
    def __init__(self):
        self.adj_list = {}  # Adjacency list dictionary

    def add_edge(self, u, v):
        """Adds a directed transfer path from node u to node v."""
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list:
            self.adj_list[v] = []
        self.adj_list[u].append(v)

    def bfs(self, start_node):
        """Breadth-First Search to find all reachable nodes/branches from start_node."""
        visited = set()
        queue = deque([start_node])
        reachable = []

        visited.add(start_node)

        while queue:
            curr = queue.popleft()
            reachable.append(curr)

            for neighbor in self.adj_list.get(curr, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return reachable
# --- Test Run: Day 9 Requirements ---
if __name__ == "__main__":
    print("--- Day 9: Addis Bank Trees & Transfer Graph ---\n")

    # 1. Build Branch Tree (Head Office -> Regions -> Branches)
    head_office = BranchNode("Head Office (Addis Ababa)")
    
    region_north = BranchNode("Northern Region")
    region_south = BranchNode("Southern Region")
    
    branch_cbe1 = BranchNode("CBE-1 (Bole Branch)")
    branch_cbe2 = BranchNode("CBE-2 (Piazza Branch)")
    branch_hawassa = BranchNode("CBE-3 (Hawassa Branch)")

    # Construct Tree Hierarchy
    head_office.add_child(region_north)
    head_office.add_child(region_south)
    
    region_north.add_child(branch_cbe1)
    region_north.add_child(branch_cbe2)
    region_south.add_child(branch_hawassa)

    # Populate accounts into branches
    acc1 = AccountFactory.create("savings", "Almaz", "SAV-101", 5000)
    acc2 = AccountFactory.create("current", "Kassa", "CUR-202", 12000)
    acc3 = AccountFactory.create("savings", "Bethlehem", "SAV-103", 8500)

    branch_cbe1.add_account(acc1)
    branch_cbe2.add_account(acc2)
    branch_hawassa.add_account(acc3)

    # 2. Test Recursive Branch Total
    print("--- Recursive Branch Totals ---")
    print(f"CBE-1 Branch Total: {branch_cbe1.total_balance():,.2f} ETB")
    print(f"Northern Region Total: {region_north.total_balance():,.2f} ETB")
    print(f"Entire Bank Total (Head Office): {head_office.total_balance():,.2f} ETB\n")

    # 3. Build Transfer Graph & Run BFS
    graph = TransferGraph()
    graph.add_edge("CBE-1", "CBE-2")
    graph.add_edge("CBE-1", "CBE-3")
    graph.add_edge("CBE-2", "CBE-4")
    graph.add_edge("CBE-3", "CBE-5")

    start_branch = "CBE-1"
    reachable_branches = graph.bfs(start_branch)

    print("--- Transfer Graph Breadth-First Search (BFS) ---")
    print(f"Nodes reachable from {start_branch} via BFS transfer network:")
    print("->".join(reachable_branches))