num1 = int(input("Enter first num1 "))
num2 = int(input("Enter second num2 "))
print("1:Addition 2:subtraction 3:multiplication 4:division ")

operation = int(input("Enter your choice"))
sum = 0

if operation == 1:
    sum=num1+num2
elif operation == 2:
    sum= num1-num2
elif operation == 3:
    sum = num1 * num2
elif operation == 4:
    sum = num1 / num2
else:
    print("wrong choice")

print(sum)