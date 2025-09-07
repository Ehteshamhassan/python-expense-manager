import sqlite3
import matplotlib.pyplot as plt

#Database Setup 
conn = sqlite3.connect("expenses.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS expenses
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              date TEXT,
              category TEXT,
              amount REAL)''')
conn.commit()

#Functions 
def add_expense(date, category, amount):
    c.execute("INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)", 
              (date, category, amount))
    conn.commit()
    print(">> Expense added successfully! <<")

def view_expenses():
    c.execute("SELECT * FROM expenses")
    rows = c.fetchall()         #Pull into py
    print("\n--- All Expenses ---")
    for row in rows:
        print(f"ID: {row[0]} | Date: {row[1]} | Category: {row[2]} | Amount: {row[3]}")

def delete_expense(expense_id):
    c.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    print("xX_Expense deleted successfully!_Xx")

def show_summary():
    c.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = c.fetchall()  

    if not data:
        print("Xx> No data to summarize <xX")
        return

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    print("\n--- Expense Summary ---")
    for cat, amt in data:
        print(f"{cat}: {amt}")

# pie chart
    plt.pie(amounts, labels=categories, autopct='%1.1f%%')
    plt.title("Expense Breakdown by Category")
    plt.show()

#Program 
def main():
    while True:
        print("\n===== Expense Tracker =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Show Summary (Charts)")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category (Food/Travel/Shopping/etc.): ")
            amount = float(input("Enter amount: "))
            add_expense(date, category, amount)

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            expense_id = int(input("Enter expense ID to delete: "))
            delete_expense(expense_id)

        elif choice == "4":
            show_summary()

        elif choice == "5":
            print("|| Exiting... ||")
            break
        else:
            print("Invalid choice, try again!")

    conn.close()

if __name__ == "__main__":
    main()
