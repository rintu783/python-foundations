amnt=int(input("Enter the bill amount"))
tip_percent=int(input("Enter tip percent"))
num=int(input("enter the number of people"))
tip=(amnt*tip_percent)/100
total=amnt+tip
each_pays=total/num
print(f"Tip:{tip:.2f}")
print(f"Total:{total:.2f}")
print(f"Each pays:{each_pays:.2f}")

