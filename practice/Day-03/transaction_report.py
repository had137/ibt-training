# Day 3: TeleBirr Transaction Log Reader
import os

# Define file paths
input_file = "practice/Day-03/transactions.txt"
output_file = "practice/Day-03/report.txt"

# 2. Dictionary to map each customer to their total spend
customer_totals = {}

# 4. Wrap the file read in a try / except block for a missing file
try:
    # 1. Read transactions.txt line by line
    with open(input_file, "r") as file:
        for line in file:
            if not line.strip():
                continue
            # Split line by comma (name, amount)
            name, amount_str = line.strip().split(",")
            amount = float(amount_str)
            
            # Build and update the dictionary mapping
            if name in customer_totals:
                customer_totals[name] += amount
            else:
                customer_totals[name] = amount

    # 3. Sort each customer and total, highest spend first
    sorted_customers = sorted(customer_totals.items(), key=lambda item: item[1], reverse=True)

    # 5. Write the summary to report.txt
    with open(output_file, "w") as report:
        report.write("--- TELEBIRR TRANSACTION SUMMARY ---\n")
        print("--- TELEBIRR TRANSACTION SUMMARY ---") # Print to console too
        
        for name, total in sorted_customers:
            line_item = f"Customer: {name} | Total Spent: {total:.2f} ETB\n"
            report.write(line_item)
            print(line_item.strip())
            
    print(f"\nSuccess! Report beautifully compiled and saved to {output_file}")

except FileNotFoundError:
    print(f"Error: The transaction log file was not found at '{input_file}'. Please check the path.")