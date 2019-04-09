def function():
     number1=eval(input('Enter the number of squares opened: '))
     number2=eval(input('Enter the number of squares: '))
     n=1
     if number1==0 and number2==0:
          sum = 'input error'
          return sum
     elif (number2 % 2) == 0 and m==n/number2:
          if number1 < 0:
               sum = 'input error'
               return sum
          else:
               sum=pow(number1,m)
               return sum
     else:
          m=n/number2
          sum=pow(number1,m) 
          return sum 
while True:
     print(function())
