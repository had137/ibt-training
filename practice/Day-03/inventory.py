# Day 3: Pharmacy Inventory Tracker

stock_file = "practice/Day-03/stock.txt"

# 1. Read stock.txt into a dictionary, inside a try/except block
stock = {}
try:
    with open(stock_file, "r") as f:
        for line in f:
            if line.strip():
                item, qty = line.strip().split(",")
                stock[item] = int(qty)
except FileNotFoundError:
    print("No stock file yet - starting with a default empty inventory!")

# 2. Function that increases or decreases an item's quantity
def adjust(item, amount):
    """Adjusts the quantity of a medication in stock."""
    stock[item] = stock.get(item, 0) + amount
    print(f"Adjusted {item} by {amount}. New quantity: {stock[item]}")

# Let's test the adjustment function (e.g., selling or restocking)
print("--- Updating Inventory ---")
adjust("Paracetamol", -5)   # Sold 5 Paracetamol
adjust("Amoxicillin", 10)   # Restocked 10 Amoxicillin
adjust("Insulin", 3)        # Added new item Insulin

# 3. Use a comprehension to find items below 10 (low stock)
low_stock = [item for item, qty in stock.items() if qty < 10]
print("\n--- Low Stock Alert (Below 10) ---")
if low_stock:
    for item in low_stock:
        print(f"Warning: {item} is low on stock! (Current: {stock[item]})")
else:
    print("All stock levels are healthy!")

# 4. Write the updated dictionary back to stock.txt so changes persist
with open(stock_file, "w") as f:
    for item, qty in stock.items():
        f.write(f"{item},{qty}\n")

print("\nInventory successfully saved to stock.txt!")