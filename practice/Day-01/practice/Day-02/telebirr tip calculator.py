# Day 2: TeleBirr Tip Calculator
# Program to split a restaurant bill with friends, including a tip.

# 1. Store a bill total (ETB) and number of people in variables
total_bill = 1250.00  # Amount in Ethiopian Birr (ETB)
friends = ["Hadiya", "Abebe", "Aster", "Dawit"]
num_people = len(friends)

# 2. Write a function split_bill(total, people, tip_rate=0.10)
def split_bill(total, people, tip_rate=0.10):
    """
    Computes the per-person amount including the tip.
    """
    total_tip = total * tip_rate
    grand_total = total + total_tip
    per_person_share = grand_total / people
    return per_person_share

# 3. Use the function to compute the per-person amount
# Default tip rate is 10% (0.10)
share_amount = split_bill(total_bill, num_people, tip_rate=0.15)

print("--- TeleBirr Split Summary ---")
print(f"Original Bill: {total_bill} ETB")
print(f"Total Friends Splitting: {num_people}")
print(f"Each person owes: {share_amount:.2f} ETB\n")

# 4. Loop over a list of names and print each person's share
print("--- Sending TeleBirr Requests ---")
for friend in friends:
    print(f"Request sent to {friend}: Please pay {share_amount:.2f} ETB via TeleBirr.")