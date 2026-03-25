# ------------------------------
# SMART EXPENSE MANAGER
# ------------------------------

import datetime

# ------------------------------
# AI-LIKE CATEGORY DETECTION
# ------------------------------
def auto_category(description):
    desc = description.lower()

    if any(word in desc for word in ["food", "burger", "pizza", "restaurant"]):
        return "Food"
    elif any(word in desc for word in ["uber", "bus", "train", "fuel"]):
        return "Travel"
    elif any(word in desc for word in ["movie", "netflix", "game"]):
        return "Entertainment"
    elif any(word in desc for word in ["shirt", "shopping", "clothes"]):
        return "Shopping"
    else:
        return "Others"


# ------------------------------
# FILE HANDLING
# ------------------------------
def load_expenses():
    expenses = []
    try:
        with open("expenses.txt", "r") as f:
            for line in f:
                amount, category, desc, date = line.strip().split("|")
                expenses.append({
                    "amount": float(amount),
                    "category": category,
                    "description": desc,
                    "date": date
                })
    except:
        pass
    return expenses


def save_expenses(expenses):
    with open("expenses.txt", "w") as f:
        for e in expenses:
            f.write(f"{e['amount']}|{e['category']}|{e['description']}|{e['date']}\n")


def load_budget():
    try:
        with open("budget.txt", "r") as f:
            return float(f.read())
    except:
        return 0.0


def save_budget(amount):
    with open("budget.txt", "w") as f:
        f.write(str(amount))


# ------------------------------
# FUNCTIONS
# ------------------------------

def add_expense():
    print("\n--- Add Expense ---")

    try:
        amount = float(input("Enter amount: "))
    except:
        print("Invalid amount!\n")
        return

    desc = input("Enter description: ")
    
    # AI category suggestion
    category = auto_category(desc)
    print(f"Suggested Category: {category}")

    user_choice = input("Do you want to change category? (y/n): ")
    if user_choice.lower() == "y":
        category = input("Enter category: ")

    date = input("Enter date (YYYY-MM-DD): ")

    expenses = load_expenses()

    expenses.append({
        "amount": amount,
        "category": category,
        "description": desc,
        "date": date
    })

    save_expenses(expenses)
    print("Expense added!\n")


def view_expenses():
    print("\n--- All Expenses ---")
    expenses = load_expenses()

    if not expenses:
        print("No expenses found.\n")
        return

    for e in expenses:
        print(f"{e['date']} | {e['category']} | {e['description']} | ₹{e['amount']}")
    print()

def monthly_summary():
    print("\n--- Monthly Summary ---")

    today = datetime.date.today()
    month = today.month
    year = today.year

    expenses = load_expenses()

    if not expenses:
        print("No expenses found.\n")
        return

    total = 0
    category_total = {}

    for e in expenses:
        try:
            y, m, d = map(int, e["date"].split("-"))
        except:
            print(f"Skipping invalid date entry: {e['date']}")
            continue

        if y == year and m == month:
            total += e["amount"]
            category_total[e["category"]] = category_total.get(e["category"], 0) + e["amount"]

    budget = load_budget()
    remaining = budget - total

    print(f"\nTotal spent: ₹{total}")
    print("\nCategory-wise:")

    for c, v in category_total.items():
        print(f"{c}: ₹{v}")

    print(f"\nBudget: ₹{budget}")
    print(f"Remaining: ₹{remaining}")

    # AI Insight
    if total > budget:
        print("⚠️ Warning: You have exceeded your budget!")
    elif total > 0.8 * budget:
        print("⚠️ Alert: You are close to your budget limit!")
    else:
        print("✅ Good spending control!")

    print()


def set_budget():
    print("\n--- Set Budget ---")
    try:
        b = float(input("Enter monthly budget: "))
        save_budget(b)
        print("Budget updated!\n")
    except:
        print("Invalid input!\n")


# ------------------------------
# MENU
# ------------------------------

def main():
    while True:
        print("===== EXPENSE MANAGER =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Monthly Summary")
        print("4. Set Budget")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            monthly_summary()
        elif choice == "4":
            set_budget()
        elif choice == "5":
            print("Bye!")
            break
        else:
            print("Invalid choice\n")


main()