expenses = []

print("💰 EXPENSE TRACKER")

while True:

    item = input("Expense name (or done): ")

    if item.lower() == "done":
        break

    amount = float(input("Amount: ₹"))

    expenses.append(amount)

total = sum(expenses)

print("\nTotal Expense: ₹", total)
