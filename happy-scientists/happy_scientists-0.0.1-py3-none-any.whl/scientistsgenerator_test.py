from .scientistsgenerator import ScientistsGenerator as sg

def main_test():
    random_scientist = sg.generate_name
    print(random_scientist)
    

if __name__ == "__main__":
    main_test()