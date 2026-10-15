import json
FILENAME = "split_data.json"
#savedata
def save_data():
    data= {"people":people, "balances":balances}
    with open(FILENAME, "w") as file:
        json.dump(data, file,indent=4)
#loaddata
def load_data():
    try:
        with open(FILENAME,"r") as file:
            data =json.load(file)
        return data["people"],data["balances"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return [],{}

people ,balances =load_data()

def add_people():
    name=input("Enter name:").strip().lower()
    if name =="":
         print("Name cannot be empty")
         return
    if name in people:
        print ("Person already exits")
        return
    people.append(name)
    balances[name]=0;
    save_data()
    print("Person Added")
    

def split_expense():
#validations
    if len(people)<2:
        print("Add atleast 2 people first")
        return
    expense_name = input("Expense Name: ").strip()
    try:
        amount= float(input("Amount: "))
    except valueError:
        print("Enter valid amount")
        return
    if amount<=0:
        print("Amount must be Positive")
        return
    paid_by =  input("Paid by:").strip().lower()
    if paid_by not in people:
        print("Enter Valid Person")
        return
#choosing member

    print("---SPLIT BETWEEN---")
    for i,name in enumerate(people,start=1):
        print(f"{i}. {name}")

    members=[]
    select =input("Select people(eg:1 2 3..): ").split()
    for num in select:
         if not num.isdigit() or not 1<=int(num)<=len(people):
            print(f"{num}' is not a valid choice")
            return
         person = people[int(num)-1]
         if person not in members:
             members.append(person)
         if not members:
            print("Nobody Selected")
            return
    print(members)
#calculating
    share = (amount/len(members))
    print(f"Split equally: Rs.{share:.2f} each")
    msg=input("Confirm? (Y/N)").strip().lower()
    if msg!="y":
        print("Split Cancelled")
        return 
    balances[paid_by]+=amount
    for person in members:
         balances[person]-=share
    save_data()
    print(f"{expense_name} recorded")
    print(balances)

    
def view_balance():
    if not people:
        print("No people yet")
        return
    for name in people:
         bal=round(balances[name],2)
         if bal>0:
            print(f"{name.title()} gets back: Rs.{bal:.2f}")
         elif bal<0:
             print(f"{name.title()} owes Rs.{-bal:.2f}")
         else:
             print(f"{name.title()} is settled up")


while True:
    print(f"\n{"="*20}")
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
