# This function will allow you to input some numbers and then find the median of them.
# Anther member in our team write this function too, but I want to know more about list and dict, so I also write it.


def median():
    count = dict()
    numbers = list()

    number = input("""Input numbers, divide different numbers by a space, when you finished, press "Enter" """)
    numbers = number.split()

    try:
        for num in numbers:
            float(num)
    except:
        print("You have to input numbers! Now let's start again.")
        median()

    length = len(numbers)
    if length % 2 == 1:
        medain_value = numbers[int((len(numbers) + 1) / 2) - 1]
        print("The median is ", medain_value)

    if length % 2 == 0:
        num = len(numbers) / 2
        num = int(num)
        medain_value = (float(numbers[num - 1]) + float(numbers[num])) / 2
        print("The median is ", medain_value)