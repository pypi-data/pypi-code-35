# This function will allow you to input some numbers and then find the average value of them.


def average():
    total = 0
    count = 0
    while True:
        num = input("""Input some numbers. When u finished, input "Done" """)
        # determine whether to break the loop
        if num == "done" and "Done" and "DONE":
            break
        # determine whether the input is valid
        try:
            num = float(num)
        except:
            print('Please input a number!')
            continue
        total = total + num
        count += 1
    print("The average value of the numbers above is: ", total / count)
