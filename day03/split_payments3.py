import os
import psycopg2
from dotenv import load_dotenv
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


load_dotenv()

conn = psycopg2.connect(
    host=os.environ["DB_HOST"],
    port=os.environ["DB_PORT"],
    dbname=os.environ["DB_NAME"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS people(
        id       SERIAL PRIMARY KEY,
        name     TEXT NOT NULL UNIQUE,
        balance  NUMERIC(12,2) NOT NULL DEFAULT 0
    )
""")
conn.commit()

def add_people():
    name = input("Enter name: ").strip().lower()
    if name == "":
        print("Name cannot be empty")
        return
    try:
        cursor.execute("INSERT INTO people (name) VALUES (%s)", (name,))
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        print("Person already exists")
        return
    print("Person added!")

def split_expense():
    cursor.execute("SELECT name FROM people ORDER BY id")
    names = [row[0] for row in cursor.fetchall()]
    if len(names) < 2:
        print("Add at least 2 people first")
        return

    expense_name = input("Expense Name: ").strip()
    try:
        amount = Decimal(input("Amount: ").strip())
    except InvalidOperation:
        print("Enter valid amount")
        return
    if not amount.is_finite() or amount <= 0:
        print("Amount must be positive")
        return
    amount = amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if amount <= 0:
        print("Amount too small")
        return

    paid_by = input("Paid by: ").strip().lower()
    if paid_by not in names:
        print("Enter valid person")
        return
    print("---SPLIT BETWEEN---")
    for i, name in enumerate(names, start=1):
        print(f"{i}. {name}")

    members = []
    for num in input("Select people (eg. 1 2 3): ").split():
        if not num.isdigit() or not 1 <= int(num) <= len(names):
            print(f"{num} is not a valid choice")
            return
        person = names[int(num) - 1]
        if person not in members:
            members.append(person)
    if not members:
        print("Nobody selected")
        return
    share = (amount / len(members)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    total = share * len(members)
    print(f"Split equally: Rs.{share:.2f} each")
    if total != amount:
        print(f"(Rounded: Rs.{total:.2f} will be recorded instead of Rs.{amount:.2f})")
    answer = input("Confirm? (Y/N): ").strip().lower()
    if answer != "y":
        print("Split cancelled")
        return

    try:
        cursor.execute(
            "UPDATE people SET balance = balance + %s WHERE name = %s",
            (total, paid_by),
        )
        for person in members:
            cursor.execute(
                "UPDATE people SET balance = balance - %s WHERE name = %s",
                (share, person),
            )
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Database error, nothing was saved: {e}")
        return
    print(f"{expense_name} recorded")

def view_balance():
    cursor.execute("SELECT name, balance FROM people ORDER BY id")
    rows = cursor.fetchall()
    if not rows:
        print("No people yet")
        return
    for name, balance in rows:
        print()
        if balance > 0:
            print(f"{name.title()} gets back: Rs.{balance:.2f}")
        elif balance < 0:
            print(f"{name.title()} owes Rs.{-balance:.2f}")
        else:
            print(f"{name.title()} is settled up")

try:
    while True:
        print(f"\n{'=' * 20}")
        print("SPLIT PAYMENTS")
        print("=" * 20)
        print("\n1. Add people")
        print("2. Split Expense")
        print("3. View Balances")
        print("4. Exit")

        choice = input("Choose option: ").strip()
        if choice == "1":
            add_people()
        elif choice == "2":
            split_expense()
        elif choice == "3":
            view_balance()
        elif choice == "4":
            print("Exit")
            break
        else:
            print("Invalid option")
except KeyboardInterrupt:
    print("\nInterrupted")
finally:
    cursor.close()
    conn.close()




