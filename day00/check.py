name="Rintu"
print("Hello",name)

num1=int(input("Enter first  number"))
num2=int(input("Enter second number"))
sum = num1+num2
print(sum)
for i in range(1,11):
    print(i,end=", ")
    
nums=[4,9,2,7]
largest=nums[0]
for n in nums:
    if n>largest:
        largest=n
print(largest)

def is_even(i):
    return i%2==0
print(is_even(3))
print(is_even(10))

persons={"name":"Asha","age":24}
print(persons["name"], "is",persons["age"],"years old")

w=input("enter a word")
vowels=['a','e','i','o','u','A','E','I','O','U']
count=0
for l in range(0,len(w)):
    if w[l] in vowels:
        count=count+1
print(count)


