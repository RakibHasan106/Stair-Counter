def Factorial(n):
     if n == 0 or n == 1:
         return 1
     else:
         result = n
         for i in range(n-1, 1, -1):      # loop runs from (n-1) to 1
             result = result * i
         return result

 #Driver Code
num = int(input("Enter a number to calculate its factorial: "))
if num < 0 :
    print("Factorial is not defined for negative numbers")
else:
    print("Factorial of", num, "is", Factorial(num))