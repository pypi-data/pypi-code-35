def Trigonometric_function():
    # This function will allow you to calculate the trigonometric function of this number
    number=list()
    while True:
        c = input("""Input a number. Then Press the Enter key """)
        if c == "done" and "Done" and "DONE":
            break
        #determine it's a number or not
        try:
            c = float(c)
        except:
            print("Please input a number!")
            continue
        import math
        print ("sin(c):",math.sin(c))
        print ("cos(c):",math.cos(c))
        print ("tan(c):",math.tan(c))
Trigonometric_function()