from tabulate import tabulate

def print_menu(today):
    if today is None:
        print("Heute ist nicht.")
        return

    if today.meals is None:
        print("Ich habe heute leider kein Essen für dich.")
        return

    table = []
    for meal in today.meals:
        table.append([meal.name, '{:.2f}€'.format(meal.price.intern), '{:.2f}€'.format(meal.price.extern)])
    print(tabulate(table, headers=['Essen', 'Preis Intern', 'Preis Extern'], tablefmt='orgtbl'))
