import sqlite3
conn = sqlite3.connect("split_payments.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS people(
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        name     TEXT NOT NULL UNIQUE,
        balance  REAL NOT NULL DEFAULT 0 
    )
""")
conn.commit()

def add_people():
    name=input("Enter name:").strip().lower()
    if name =="":
         print("Name cannot be empty")
         return
    try:
        cursor.execute("INSERT INTO people(name) VALUES (?)",(name,))
        conn.commit()
    except sqlite3.IntegrityError:
        print ("Person already exists")
        return
    print("Person Added")
    
def split_expense():
    cursor.execute("SELECT name FROM people ORDER BY id")
    names = [row[0] for row in cursor.fetchall()]
    if len(names)<2:
        print("Add atleast 2 people first")
        return
    expense_name = input("Expense Name: ").strip()
    try:
        amount= float(input("Amount: "))
    except ValueError:
        print("Enter valid amount")
        return
    if amount<=0:
        print("Amount must be Positive")
        return
    paid_by =  input("Paid by:").strip().lower()
    if paid_by not in names:
        print("Enter Valid Person")
        return
    print("---SPLIT BETWEEN---")
    for i,name in enumerate(names,start=1):
        print(f"{i}. {name}")

    members=[]
    for num in input("Select people(eg. 1 2 3): ").split():
         if not num.isdigit() or not 1<=int(num)<=len(names):
            print(f"{num} is not a valid choice")
            return
         person = names[int(num)-1]
         if person not in members:
             members.append(person)
    if not members:
         print("Nobody Selected")
         return
    share = (amount/len(members))
    print(f"Split equally: Rs.{share:.2f} each")
    msg=input("Confirm? (Y/N)").strip().lower()
    if msg!="y":
        print("Split Cancelled")
        return
    cursor.execute("UPDATE people SET balance =balance+ ? WHERE name= ?",(amount,paid_by))
    for person in members:
         cursor.execute("UPDATE people SET balance =balance - ? WHERE name =?",(share, person))
    conn.commit()
    print(f"{expense_name} recorded")

def view_balance():
    cursor.execute("SELECT name,balance FROM people ORDER BY id")
    rows = cursor.fetchall()
    if not rows:
        print("No people yet")
        return
    for name,balance in rows:
         balance = round(balance ,2)
         if balance>0:
            print(f"{name.title()} gets back: Rs.{balance:.2f}")
         elif balance<0:
             print(f"{name.title()} owes Rs.{-balance:.2f}")
         else:
             print(f"{name.title()} is settled up")


while True:
    print(f"\n{'='*20}")
    print("SPLIT PAYMENTS")
    print("="*20)
    print("\n1. Add people")
    print("2. Split Expense")
    print("3. View Balances")
    print("4. Exit")

    choice=input("Choose option:")
    if choice=="1":
        add_people()
    elif choice=="2":
        split_expense()
    elif choice=="3":
        view_balance()
    elif choice=="4":
        print("Exit")
        break
    else:
        print("Invalid Option")
conn.close()
